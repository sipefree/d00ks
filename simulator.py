##########################################################################
# This file is part of d00ks.
# 
# d00ks is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
# 
# d00ks is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
# 
# You should have received a copy of the GNU General Public License
# along with d00ks.  If not, see <http://www.gnu.org/licenses/>.
##########################################################################

"""
This file represents the actual simulator itself.

It is rather simple, containing methods for stepping
through code.
"""

import cond
import instruction
import register
import memory
import promise
import pprint

class Area(object):
	"""Represents an assembler AREA directive"""
	def __init__(self, label, attrs):
		self.label = label
		self.attrs = attrs
	def __repr__(self):
		return "AREA %s %s"%(self.label, ",".join(self.attrs))
		
class Breakpoint(Exception):
	pass
		

class Program(object):
	"""Represents an ARM program."""
	def __init__(self):
		self.code = []
		self.registers = register.Registers()
		self.memory = memory.Memory(4096)
		self.registers.memory = self.memory
	
	def compile(self, tuples):
		"""
		This method takes a list of tuples in the format:
		(label, instruction)
		
		Where label is an optional string that will cause the
		address of instruction to be placed in the symbol table
		under that label.
		
		The instruction itself comes from the 'command' part of
		the parser. It can be an ARM instruction like MOV, or
		a directive like AREA or DCB.
		"""
		start_s = 0
		code_s = 1
		data_s = 2
		mode = start_s
		
		code_woffset = 0
		data_boffset = 0xA1000000
		
		self.code = []
		
		self.breakpoints = []
				
		
		for (label,line) in tuples:
			if line == None:
				if mode == code_s:
					self.registers.symbol_insert(label, codewoffset)
				elif mode == data_s:
					self.registers.symbol_insert(label, data_boffset)
				else:
					raise SyntaxError("Label " + label + " used but not in CODE or DATA mode!")
				continue
			if type(line) == Area:
				if "CODE" in line.attrs:
					if "DATA" in line.attrs:
						raise SyntaxError("AREA %s cannot have both CODE and DATA attrs!"%line.label)
					mode = code_s
				elif "DATA" in line.attrs:
					# word align please
					while True:
						if data_boffset & 0x3:
							data_boffset += 1
						else:
							break
					mode = data_s
				continue
			if mode == code_s:
				if isinstance(line, instruction.Instruction):
					self.code.append(line)
					if label:
						self.registers.symbol_insert(label, code_woffset)
						line.label = label
					code_woffset += 1
			elif mode == data_s:
				if isinstance(line, memory.Store):
					if label:
						self.registers.symbol_insert(label, data_boffset)
					line.store(self.memory, data_boffset)
					data_boffset += line.size()
		self.breakpoints.append(code_woffset - 1)
					
	
	def start(self):
		"""
		Resets the registers, and by proxy, the program counter.
		"""
		self.registers = register.Registers()
	
	def cursym(self):
		"""
		Returns the symbol closes to the current PC. Debug mode only.
		"""
		ans = "{program}"
		for i in xrange(self.registers[self.registers.PC], -1, -1):
			line = self.code[i]
			#print "trying %s %s"%(line.label if line.label != "" else "", line)
			if line.label != "":
				ans = line.label
				num = i
				break
		return ans

	@promise.sensible()
	def step(self):
		"""
		Steps through one instruction.
		
		"""
		if self.registers[self.registers.PC] in self.breakpoints:
			raise Breakpoint()
	
		# fetch/decode
		instr = self.code[self.registers[self.registers.PC]]
		
		# execute
		self.registers[self.registers.PC] += 1
		instr.execute(self.registers)

	@promise.sensible()
	def step_debug(self):
		"""
		Steps through one instruction.
		
		"""
		# fetch/decode
		instr = self.code[self.registers[self.registers.PC]]
		
		# execute
		self.registers[self.registers.PC] += 1
		instr.execute(self.registers)
		if len(self.registers.changed) > 1:
			self.registers.p()
			self.registers.set_clean()
	
	def run(self):
		"""
		Continues until breakpoint.
		
		"""
		try:
			while True:
				self.step()
		except:
			print "Breakpoint detected!"
			print str(self.code[self.registers[self.registers.PC]])
			self.debug()
			
	def debug(self):
		# simple repl
		lastcmd = 's'
		while True:
			print ">> " + str(self.code[self.registers[self.registers.PC]])
			sym = self.cursym()
			num = self.registers.symbol_table[sym] if sym != "{program}" else 0
			try:
				cmd = raw_input("0x%X <%s + 0x%X>: "%(self.registers[self.registers.PC], sym, self.registers[self.registers.PC] - num))
			except Exception, e:
				print "\nQuitting."
				exit(1)
			if cmd == "": cmd = lastcmd
			lastcmd = cmd
			if cmd == "s":
				self.step_debug()
			elif cmd == "q":
				break
			elif cmd == "p":
				self.registers.p()
			elif cmd == "m":
				self.memory.debug()
			elif cmd == "mb":
				self.memory.debug_char()
			elif cmd == "c":
				self.run()
			elif cmd == "t":
				for sym in self.registers.symbol_table:
					print sym + ": " + hex(self.registers.symbol_table[sym])
	
