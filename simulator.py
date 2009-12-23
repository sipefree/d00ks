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
		

class program(object):
	"""Represents an ARM program."""
	def __init__(self):
		super(program, self).__init__()
		self.code = []
		self.registers = register.registers()
		self.memory = memory.memory(1024)
	
	def compile(self, tuples):
		start_s = 0
		code_s = 1
		data_s = 2
		mode = start_s
		
		code_woffset = 0
		data_boffset = 0xA1000000
		
		self.code = []
		
		
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
		self.memory.debug()
					
	
	def add_instr(self, instruction):
		self.code.append(instruction)
	
	def start(self):
		self.registers = register.registers()

	def step(self):
		# fetch/decode
		instr = self.code[self.registers[self.registers.PC]]
		print str(instr)
		
		# execute
		self.registers[self.registers.PC] += 1
		instr.execute(self.registers)
		if self.registers.changed != [15]:
			self.registers.p()
		self.registers.set_clean()
			
	def debug(self):
		# simple repl
		lastcmd = 's'
		while True:
			cmd = raw_input("%i> "%(self.registers[self.registers.PC]))
			if cmd == "": cmd = lastcmd
			lastcmd = cmd
			if cmd == "s":
				self.step()
			elif cmd == "q":
				break
			elif cmd == "p":
				self.registers.p()
	