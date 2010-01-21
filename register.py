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
Represents the registers in the ARM simulator.

It also stores the symbol table, for easy lookup.
"""
import promise

class Registers(object):
	"""
	This registers object is passed around. It contains
	the registers, stored as a python list, and functions
	for dealing with them.
	
	It implements the magic methods __getitem__ and __setitem__
	to make access and setting easy.
	
	Symbols are stored as a python dict.
	
	The class also stores some bit masks pointing to the
	location of various flags in the CPSR etc.
	"""
	def __init__(self):
		self.regs = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
		self.LR = 14
		self.PC = 15
		self.CPSR = 16
		
		self.N = 0x80000000
		self.Z = 0x40000000
		self.C = 0x20000000
		self.V = 0x10000000
		self.J = 0x02000000
		self.E = 0x00000200
		self.A = 0x00000100
		self.I = 0x00000080
		self.F = 0x00000040
		self.T = 0x00000020
		
		self.symbol_table = {}
		
		self.changed = []
		
		self.memory = None
	
	@promise.sensible()
	@promise.pure()
	def __getitem__(self, key):
		return self.regs[key]
	
	@promise.sensible()
	def __setitem__(self, key, value):
		value = value & 0xFFFFFFFF
		if self.regs[key] != value:
			self.regs[key] = value
			self.changed.append(key)
	
	@promise.sensible()
	def symbol_insert(self, key, index):
		# TODO: symbol already exists error
		self.symbol_table[key] = index
	
	@promise.sensible()
	def symbol_abs(self, value):
		return self.symbol_table[value]
		
	@promise.sensible()
	def flag_set(self, flag, value):
		if value:
			self.regs[self.CPSR] |= flag
		else:
			self.regs[self.CPSR] &= (~flag)
	
	@promise.sensible()
	@promise.pure()
	def flag_get(self, flag):
		return 1 if self.regs[self.CPSR] & flag else 0
	
	@promise.sensible()
	def set_clean(self):
		self.changed = []
	
	def p(self):
		'Prints the contents of the registers'
		ret = "registers {\n"
		for i in range(0, len(self.regs)):
			ret += "%s	R%i = 0x%08X = %d%s\n"%\
				("*" if i in self.changed else " ",\
				i, self.regs[i], self.regs[i],\
				" = '%c'"%chr(self.regs[i]) if self.regs[i] in range(32, 128) else "")
		ret += "} "
		ret += "N = %i, Z = %i, C = %i, V = %i"%(int(self.flag_get(self.N)), int(self.flag_get(self.Z)), int(self.flag_get(self.C)), int(self.flag_get(self.V)))
		print ret