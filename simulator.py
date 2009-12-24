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

class area(object):
	"""Represents an assembler AREA directive"""
	def __init__(self, label, attrs):
		self.label = label
		self.attrs = attrs
	def __repr__(self):
		return "AREA %s %s"%(self.label, ",".join(self.attrs))
		
class Breakpoint(Exception):
	pass
		

class program(object):
	"""Represents an ARM program."""
	def __init__(self):
		super(program, self).__init__()
		self.code = []
		self.registers = register.registers()
		self.memory = memory.memory(1024)
	
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
			if type(line) == area:
				if "CODE" in line.attrs:
					if "DATA" in line.attrs:
						raise SyntaxError("AREA %s cannot have both CODE and DATA attrs!"%line.label)
					mode = code_s
				elif "DATA" in line.attrs:
					mode = data_s
				continue
			if mode == code_s:
				if isinstance(line, instruction.instruction):
					self.code.append(line)
					if label:
						self.registers.symbol_insert(label, code_woffset)
					code_woffset += 1
			elif mode == data_s:
				if isinstance(line, memory.store):
					if label:
						self.registers.symbol_insert(label, data_boffset)
					line.store(self.memory, data_boffset)
					data_boffset += line.size()
		self.breakpoints.append(code_woffset - 1)
					
	
	def start(self):
		"""
		Resets the registers, and by proxy, the program counter.
		"""
		self.registers = register.registers()

	def step(self, debug=False, breaks=False):
		"""
		Steps through one instruction.
		
		"""
		# catch breakpoint
		if breaks:
			if self.registers[self.registers.PC] in self.breakpoints:
				raise Breakpoint()
		
		# fetch/decode
		instr = self.code[self.registers[self.registers.PC]]
		if debug:
			print str(instr)
		
		# execute
		self.registers[self.registers.PC] += 1
		instr.execute(self.registers)
		if self.registers.changed != [15] and debug:
			self.registers.p()
			self.registers.set_clean()
	
	def run(self):
		"""
		Continues until breakpoint.
		
		"""
		try:
			while True:
				self.step(breaks=True)
		except:
			print "Breakpoint detected!"
			print str(self.code[self.registers[self.registers.PC]])
			self.debug()
			
	def debug(self):
		# simple repl
		lastcmd = 's'
		while True:
			cmd = raw_input("%i> "%(self.registers[self.registers.PC]))
			if cmd == "": cmd = lastcmd
			lastcmd = cmd
			if cmd == "s":
				self.step(debug=True)
			elif cmd == "q":
				break
			elif cmd == "p":
				self.registers.p()
			elif cmd == "m":
				self.memory.debug()
			elif cmd == "c":
				self.run()
	