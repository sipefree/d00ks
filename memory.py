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
This file contains classes for dealing with memory
in the ARM simulator.
"""


from ctypes import *
import struct

class MemoryError(Exception):
	pass

class Store(object):
	def __repr__(self):
		return str(self)

class DCB(Store):
	"""Represents a DCB operation"""
	def __init__(self, dcb_list):
		super(DCB, self).__init__()
		self.bytes = ""
		for item in dcb_list:
			if type(item) == str:
				for char in item:
					self.bytes += char
			elif type(item) == int:
				char = c_ubyte(item)
				char = chr(char.value)
				self.bytes += char
	
	def size(self):
		return len(self.bytes)
	
	def store(self, mem, addr):
		for byte in self.bytes:
			byte = ord(byte)
			mem.strb(addr, byte)
			addr += 1
	def __str__(self):
		return "DCB " + repr(self.bytes)

class SPACE(Store):
	"""Represents a SPACE operation"""
	def __init__(self, length):
		super(SPACE, self).__init__()
		self.length = length
	def size(self):
		return self.length
	def store(self, mem, addr):
		pass

class Memory(object):
	"""
	Represents the RAM of a program.
	
	Memory is stored using a byte buffer created
	by the python ctypes module.
	"""
	def __init__(self, size=1024):
		super(Memory, self).__init__()
		self.size = size
		self.buffer = create_string_buffer(size)
		self.startaddr = 0xA1000000
		self.debugmode = False
		self.debug_clean()
	
	def set_debugmode(self, boolean):
		self.debugmode = boolean
	
	def debug_clean(self):
		self.readaccesses = []
		self.writeaccesses = []
	
	def debug(self):
		"""
		Prints the contents of memory.
		"""
		buf = ""
		for i in range(self.startaddr, self.startaddr + self.size):
			if i % 32 == 0:
				buf += "\n0x%X:"%i
			if i % 4 == 0:
				buf += " "
			addr = (i - (i%4)) + (4 - (i % 4) - 1)
			buf += "%02X"%self.ldrb(addr)
		print buf
	
	def realaddr(self, addr):
		"""
		Calculates the offset in the byte buffer
		from a virtual address.
		"""
		real = addr - self.startaddr
		if real >= self.size:
			raise MemoryError("Out of bounds access at %i"%addr)
		return real
	
	def strb(self, addr, byte):
		"""Store byte"""
		byte = c_uint(byte)
		byte = byte.value & 0xFF
		addr = self.realaddr(addr)
		struct.pack_into("B", self.buffer, addr, byte)
		if self.debugmode:
			self.writeaccesses.append(addr)
	
	def strh(self, addr, hw):
		"""Store halfword"""
		if addr % 2 != 0:
			raise MemoryError("Halfword stores must be halfword-aligned!")
		hw = c_ushort(hw)
		hw = hw.value & 0xFFFF
		addr = self.realaddr(addr)
		struct.pack_into("H", self.buffer, addr, hw)
		if self.debugmode:
			self.writeaccesses.append(addr)
			self.writeaccesses.append(addr+1)
		
	def strw(self, addr, word):
		"""Store word"""
		if addr % 4 != 0:
			raise MemoryError("Word stores must be word-aligned!")
		word = c_uint(word)
		word = word.value & 0xFFFFFFFF
		addr = self.realaddr(addr)
		struct.pack_into("I", self.buffer, addr, word)
		if self.debugmode:
			self.writeaccesses.append(addr)
			self.writeaccesses.append(addr+1)
			self.writeaccesses.append(addr+2)
			self.writeaccesses.append(addr+3)
		
	
	def ldrb(self, addr):
		"""Load byte"""
		addr = self.realaddr(addr)
		(val,) = struct.unpack_from("B", self.buffer, addr)
		if self.debugmode:
			self.readaccesses.append(addr)
		return val
	
	def ldrh(self, addr):
		"""Load halfword"""
		if addr % 2 != 0:
			raise MemoryError("Halfword reads must be halfword-aligned!")
		addr = self.realaddr(addr)
		(val,) = struct.unpack_from("H", self.buffer, addr)
		if self.debugmode:
			self.readaccesses.append(addr)
			self.readaccesses.append(addr+1)
		return val
	
	def ldrw(self, addr):
		"""Load word"""
		if addr % 4 != 0:
			raise MemoryError("Word stores must be word-aligned!")
		addr = self.realaddr(addr)
		(val,) = struct.unpack_from("I", self.buffer, addr)
		if self.debugmode:
			self.readaccesses.append(addr)
			self.readaccesses.append(addr+1)
			self.readaccesses.append(addr+2)
			self.readaccesses.append(addr+3)
		return val
	
	def range_to_list(self, addr, length):
		"""Return a range of memory as a list of bytes"""
		return [self.ldrb(x) for x in range(addr, length)]

