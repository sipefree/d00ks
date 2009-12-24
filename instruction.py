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
This file represents each instruction and everything that
an instruction needs to execute.
"""


from ctypes import c_uint
import simulator

class argument(object):
	"""
	In ARM, arguments to instructions are usually either
	registers or immediate values. This is an abstraction
	of each of those which no matter which of these the
	argument is, will return the correct value.
	
	It stores a value and isregister. If it's not a register
	argument, then value is returned. If it is, then the value
	of that register is returned.
	
	Registers are passed to the get() function regardless,
	as the instruction doesn't care which type it is,
	only the value.
	"""
	def __init__(self, isregister, value):
		self.isregister = isregister
		self.value = value
	def get(self, registers):
		return registers[self.value] if self.isregister else self.value
		
	def value(self):
		return self.value
		
	def __str__(self):
		if self.isregister:
			return "R%i"%self.value
		else:
			return "#0x%X"%self.value


# helpers for each of the registers, useful
# for debugging purposes
R0 = argument(True, 0)
R1 = argument(True, 1)
R2 = argument(True, 2)
R3 = argument(True, 3)
R4 = argument(True, 4)
R5 = argument(True, 5)
R6 = argument(True, 6)
R7 = argument(True, 7)
R8 = argument(True, 8)
R9 = argument(True, 9)
R10 = argument(True, 10)
R11 = argument(True, 11)
R12 = argument(True, 12)
R13 = argument(True, 13)
R14 = argument(True, 14)
R15 = argument(True, 15)

def reg(i):
	'Helper function for creating arguments'
	return argument(True, i)

def num(i):
	'Helper function for creating arguments'
	return argument(False, i)
	
class target(object):
	"""
	Certain things can be loaded from either symbol locations
	in memory, or as direct constant value. This class
	abstracts those two distinctions, similar to argument.
	
	The registers provide access to the symbol table, for
	convinience.
	"""
	def __init__(self, islabel, value):
		self.islabel = islabel
		self.value = value
	
	def get(self, registers):
		return registers.symbol_abs(self.value) if self.islabel else self.value
	
	def __str__(self):
		return "=%s"%(self.value if self.islabel else "%X"%self.value)

class branchtarget(target):
	"""
	The branch (B) instruction uses targets but the syntax doesn't
	use the = sign. This is just for pretty printing.
	"""
	def __str__(self):
		return "%s"%(self.value if self.islabel else "%X"%self.value)


def label(lab):
	'Helper function for creating targets'
	return target(True, lab)

def immediate(num):
	'Helper function for creating targets'
	return target(False, num)

class addrmode(object):
	'''Just a register'''
	def __init__(self, rn):
		self.rn = rn
	def __repr__(self):
		return str(self)
	def get(registers):
		return registers[self.rn]
	def __str__(self):
		return "[R%i]"%self.rn

class addrmode_immoffset(addrmode):
	'''Immediate offset'''
	def __init__(self, rn, shifter):
		self.rn = rn
		self.shifter = shifter
	def get(registers):
		return registers[self.rn] + shifter.apply(registers)
	def __str__(self):
		return "[R%i, %s]"%(self.rn, self.shifter)

class addrmode_preindexed(addrmode):
	'''Pre-indexed register'''
	def __init__(self, rn, shifter):
		self.rn = rn
		self.shifter = shifter
	def get(registers):
		registers[self.rn] += shifter.apply(registers)
		return registers[self.rn]
	def __str__(self):
		return "[R%i, %s]!"%(self.rn, self.shifter)
	
class addrmode_postindexed(addrmode):
	'''Post-indexed register'''
	def __init__(self, rn, shifter):
		self.rn = rn
		self.shifter = shifter
	def get(registers):
		val = registers[self.rn]
		registers[self.rn] += shifter.apply(registers)
		return val
	def __str__(self):
		return "[R%i], %s"%(self.rn, self.shifter)
		

class shifter(object):
	"""
	In ARM, the last argument for many instructions can be
	a so-called shifter operand. This can either be just
	a value, a register, or a value/register with a bit-shift
	by a constant amount, or a value/register with a bit shift
	by the value of another register.
	
	This class abstracts those. Each of the different type
	of shifter subclasses this class, using the argument()
	class to make dealing with constant values or register
	values easy. This basic class just has a value or a
	register, kept in an argument object.
	"""
	def __init__(self, rm):
		super(shifter, self).__init__()
		self.rm = rm
		
	def apply(self, registers, flags=False):
		return self.rm.get(registers)
	
	def __str__(self):
		return str(self.rm)

class ASR(shifter):
	"""
	rm, ASR <val>
	
	Arithmetic shift right. Shifts right by <val> but
	expanding the most significant bit.
	
	This allows for signed division by 2.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg

	def __str__(self):
		return "%s, ASR %s"%(str(self.rm), str(self.arg))

	def apply(self, registers, flags=False):
		"""Applies an LSR of amount value to the register"""
		val = min(self.arg.get(registers), 32)
		# is the MSB 1?
		if self.rm.get(registers) & (1 << 31):
			# make a mask of 1s to extend the bits with
			fill = 0xFFFFFFFF << (32 - val)
			# shorten to 32 bits
			fill = fill & 0xFFFFFFFF
		else:
			fill = 0x0
		tmp = self.rm.get(registers) >> val
		# extend MSBs
		tmp = tmp | fill
		retval = tmp & 0xFFFFFFFF
		if flags:
			registers.flag_set(registers.C, (self.rm.get(registers) >> (val-1)) & 1)
		return retval

class LSL(shifter):
	"""
	rm, LSL <val>
	
	Logical shift left. Shifts contents left by <val>.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg
	
	def __str__(self):
		return "%s, LSL %s"%(str(self.rm), str(self.arg))
	
	def apply(self, registers, flags=False):
		"""Applies an LSL of amount value to the register"""
		val = min(self.arg.get(registers), 32)
		tmp = self.rm.get(registers) << val
		retval = tmp & 0xFFFFFFFF
		if flags:
			registers.flag_set(registers.C, tmp & (1 << 32))
		return retval

class LSR(shifter):
	"""
	rm, LSR <val>
	
	Logical shift right.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg

	def __str__(self):
		return "%s, LSR %s"%(str(self.rm), str(self.arg))

	def apply(self, registers, flags=False):
		"""Applies an LSR of amount value to the register"""
		val = min(self.arg.get(registers), 32)
		tmp = self.rm.get(registers) >> val
		retval = tmp & 0xFFFFFFFF
		if flags:
			registers.flag_set(registers.C, (self.rm.get(registers) >> (val-1)) & 1)
		return retval

class ROR(shifter):
	"""
	rm, ROR <val>
	
	Rotate bits right. Anything that comes off the right,
	goes back in on the left.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg

	def __str__(self):
		return "%s, ROR %s"%(str(self.rm), str(self.arg))

	def apply(self, registers, flags=False):
		"""Applies an ROR of amount value to the register"""
		val = min(self.arg.get(registers), 32)
		# select the bits that will be shifted out
		fill = 0xFFFFFFFF >> (32 - val)
		fill = fill & self.rm.get(registers)
		# shift them to the new position
		fill = fill << (32 - val)
		# do the rotate
		tmp = self.rm.get(registers) >> val
		retval = tmp & 0xFFFFFFFF
		# merge in the bits that were wrapped
		retval = retval | fill
		if flags:
			registers.flag_set(registers.C, (self.rm.get(registers) >> (val-1)) & 1)
		return retval

class RRX(shifter):
	"""
	rm, ROR <val>
	
	33-bit rotate right, using the C flag as the 33rd bit.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg

	def __str__(self):
		return "%s, RRX %s"%(str(self.rm), str(self.arg))

	def apply(self, registers, flags=False):
		"""Applies an RRX of amount value to the register"""
		# i cant think of any better way to do this than 1 shift at a time
		val = min(self.arg.get(registers))
		tmp = self.rm.get(registers)
		for i in range(0, val):
			# get carry bit in right position
			c = (1 << 31) if registers.flag_get(registers.C) else 0
			# get the next value of the carry bit
			new_c = tmp & 1
			# perform shift
			tmp = tmp >> 1
			# merge carry bit
			tmp = tmp | c
			# save new carry bit
			registers.flag_set(registers.C, new_c)
		return tmp
		

class instruction(object):
	"""
	Abstract class representing an instruction.
	
	The default constructor takes arguments that are standard
	for many instructions. Instructions that don't take these
	arguments should override this method.
	
	The class also contains some helper functions for determining
	carry and overflow and signedness.
	"""
	def __init__(self, cond, s, rd, rn,  shifter_operand):
		super(instruction, self).__init__()
		self.cond = cond
		self.s = s
		self.rn = rn
		self.rd = rd
		self.shifter_operand = shifter_operand
	
	def __str__(self):
		return "_UNKNOWN_INSTR_%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
		
	def signed_pos(self, value):
		'Is the value positive?'
		return not (value & (1 << 31))
	
	def signed_neg(self, value):
		'Is the value negative'
		return value & (1 << 31)
	
	def sign(self, value):
		'What is the sign of value?'
		ans = 1 if self.signed_pos(value) else -1
		return 0 if value == 0 else ans
		
	def carry_from(self, value):
		'Is there carry in a 33 bit value?'
		return 1 if value & (1 << 32) else 0
	
	def overflow_from(self, rn, rm, value):
		"""
		Overflow occurs when the sign of the operands was
		the same but the result of the computation has caused
		the sign to change.
		"""
		if self.sign(rn) == self.sign(rm):
			return self.sign(rn) != self.sign(value)
		else:
			return False
	
	def twos_compliment(self, value):
		'Returns twos compliment of a value'
		return ((~value) + 1) & 0xFFFFFFFF
	
	def execute(self, registers):
		pass
	
	def __repr__(self):
		return str(self)
		
class ADC(instruction):
	"""
	ADC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Add with carry. Adds two values and accumulates it with
	the current value of the carry bit.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			tmp = rm + self.rn.get(registers) + (1 if registers.flag_get(registers.C) else 0)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, self.carry_from(tmp))
				registers.flag_set(registers.V, self.overflow_from(rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "ADC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
				
class ADD(instruction):
	"""
	ADD{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Adds two values.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			tmp = rm + self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, self.carry_from(tmp))
				registers.flag_set(registers.V, self.overflow_from(rm, self.rn.get(registers), tmp))
	def __str__(self):
		return "ADD%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
		

class AND(instruction):
	"""
	AND{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Calculates binary AND of two values.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers, flags = self.s)
			tmp = rm & self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "AND%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class B(instruction):
	"""
	B{L}{cond} <target_address>
	
	Branch to target.
	"""
	def __init__(self, link, cond, target):
		self.link = link
		self.cond = cond
		self.target = target
	
	def execute(self, registers):
		if self.cond(registers):
			if self.link:
				registers[registers.LR] = registers[registers.PC]+1
			registers[registers.PC] = self.target.get(registers)

	def __str__(self):
		return "B%s %s"%\
			("L" if self.link else "", str(self.target))
	
class BIC(instruction):
	"""
	BIC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Clear the bits specified by shifter_operand in Rn.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers, flags = self.s)
			print "rm: 0x%X"%rm
			neg = ~rm & 0xFFFFFFFF
			print "~rm: 0x%X"%neg
			tmp = self.rn.get(registers) & neg
			print "tmp: 0x%X"%tmp
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "BIC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class BKPT(instruction):
	def __init__(self):
		pass
	def execute(self, registers):
		raise simulator.Breakpoint()

class BX(B):
	pass

class CMN(instruction):
	"""
	CMN{cond} Rn, <shifter_operand>
	
	Compare negative.
	"""
	def __init__(self, cond, rn, shifter_operand):
		super(instruction, self).__init__()
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand

	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			alu_out = self.rn.get(registers) + rm
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode
			registers.flag_set(registers.C, self.carry_from(alu_out))
			registers.flag_set(registers.V, self.overflow_from(self.rn.get(registers), rm, alu_out))

	def __str__(self):
		return "CMN%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))

class CMP(instruction):
	"""
	CMP{cond} <Rn>, <shifter_operand>
	
	Compare.
	"""
	def __init__(self, cond, rn, shifter_operand):
		super(instruction, self).__init__()
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand
	
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			alu_out = self.rn.get(registers) - rm
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode
			registers.flag_set(registers.C, alu_out >= 0)
			registers.flag_set(registers.V, self.overflow_from(self.rn.get(registers), rm, alu_out))
			
	def __str__(self):
		return "CMP%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))
	
class EOR(instruction):
	"""
	EOR{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Exclusive-OR
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers, flags = self.s)
			tmp = rm ^ self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "EOR%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class LDM(instruction):
	pass

class LDR(instruction):
	pass
	
class LDRB(instruction):
	pass

class LDRH(instruction):
	pass

class LDSB(instruction):
	pass

class LDSH(instruction):
	pass

class MLA(instruction):
	"""
	MLA{cond}{S} <Rd>, <Rm>, <Rs>, <Rn>
	
	Multiply and accumulate.
	"""
	def __init__(self, cond, s, rd, rm, rs, rn):
		self.cond = cond
		self.s = s
		self.rd = rd
		self.rn = rn
		self.rm = rm
		self.rs = rs
	
	def execute(self, registers):
		if self.cond(registers):
			tmp = (self.rm.get(registers) * self.rs.get(registers) + self.rn.get(registers))
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)

	def __str__(self):
		return "MLA%s%s R%i, %s, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rm), str(self.rs), str(self.rn))

class MOV(instruction):
	"""
	MOV{cond}{S} <Rd>, <shifter_operand>
	
	Move.
	"""
	def __init__(self, cond, s, rd, shifter_operand):
		self.cond = cond
		self.s = s
		self.rd = rd
		self.shifter_operand = shifter_operand
	def execute(self, registers):
		if self.cond(registers):
			registers[self.rd] = self.shifter_operand.apply(registers, flags=self.s)
			if self.s:
				registers.flag_set(registers.N, registers[self.rd] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "MOV%s%s R%i, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.shifter_operand))

class MRS(instruction):
	pass

class MSR(instruction):
	pass

class MUL(instruction):
	"""
	MUL{cond}{S} <Rd>, <Rm>, <Rs>
	
	Multiply.
	"""
	def __init__(self, cond, s, rd, rm, rs):
		self.cond = cond
		self.s = s
		self.rd = rd
		self.rm = rm
		self.rs = rs
	
	def execute(self, registers):
		if self.cond(registers):
			registers[self.rd] = self.rm.get(registers) * self.rs.get(registers)
			if self.s:
				registers.flag_set(registers.N, registers[self.rd] & (1 << 31))
				registers.flag_set(registers.N, registers[self.rd] == 0)

	def __str__(self):
		return "EOR%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rm), str(self.rs))

class MVN(instruction):
	"""
	MVN{cond}{S} <Rd>, <shifter_operand>
	
	Move negative.
	"""
	def __init__(self, cond, s, rd, shifter_operand):
		self.cond = cond
		self.s = s
		self.rd = rd
		self.shifter_operand = shifter_operand
	def execute(self, registers):
		if self.cond(registers):
			registers[self.rd] = ~self.shifter_operand.apply(registers, flags=self.s)
			if self.s:
				registers.flag_set(registers.N, registers[self.rd] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "MVN%s%s R%i, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.shifter_operand))

class ORR(instruction):
	"""
	ORR{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Binary-OR.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers, flags = self.s)
			tmp = rm | self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "ORR%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class RSB(instruction):
	"""
	RSB{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Reverse subtract.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			tmp = rm - self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, self.carry_from(tmp))
				registers.flag_set(registers.V, self.overflow_from(rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "RSB%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class RSC(instruction):
	"""
	RSC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Reverse subtract with carry.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			tmp = rm - self.rn.get(registers) - (0 if registers.flag_get(registers.C) else 1)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, registers[self.rd] >= 0)
				registers.flag_set(registers.V, self.overflow_from(rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "RSC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class SBC(instruction):
	"""
	SBC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Subtract with carry.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			tmp = self.rn.get(registers) - rm - (0 if registers.flag_get(registers.C) else 1)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, registers[self.rd] >= 0)
				registers.flag_set(registers.V, self.overflow_from(rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "SBC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class SMLAL(instruction):
	"""
	SMLAL{cond}{S} <RdLo>, <RdHi>, <Rm>, <Rs>
	
	Signed multiply long with accumulate.
	"""
	def __init__(self, cond, s, rdlo, rdhi, rm, rs):
		self.cond = cond
		self.s = s
		self.rdlo = rdlo
		self.rdhi = rdhi
		self.rm = rm
		self.rs = rs

	def execute(self, registers):
		if self.cond(registers):
			registers[self.rdlo] = ((self.rm.get(registers) * self.rs.get(registers)) & 0xFFFFFFFF)\
				+ registers[self.rdlo]
			registers[self.rdhi] = (((self.rm.get(registers) * self.rs.get(registers)) >> 31) & 0xFFFFFFFF)\
				+ registers[self.rdhi] + self.carry_from(self.rm.get(registers) * self.rs.get(registers))
			if self.s:
				registers.flag_set(registers.N, registers[self.rdhi] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rdlo] == 0 and registers[self.rdhi] == 0)

	def __str__(self):
		return "SMLAL%s%s R%i, R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rdlo, self.rdhi, str(self.rm), str(self.rs))

class SMULL(instruction):
	"""
	SMULL{cond}{S} <RdLo>, <RdHi>, <Rm>, <Rs>
	
	Signed multiply long.
	"""
	def __init__(self, cond, s, rdlo, rdhi, rm, rs):
		self.cond = cond
		self.s = s
		self.rdlo = rdlo
		self.rdhi = rdhi
		self.rm = rm
		self.rs = rs

	def execute(self, registers):
		if self.cond(registers):
			registers[self.rdlo] = ((self.rm.get(registers) * self.rs.get(registers)) & 0xFFFFFFFF)
			registers[self.rdhi] = (((self.rm.get(registers) * self.rs.get(registers)) >> 31) & 0xFFFFFFFF)
			if self.s:
				registers.flag_set(registers.N, registers[self.rdhi] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rdlo] == 0 and registers[self.rdhi] == 0)

	def __str__(self):
		return "SMULL%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rdlo, self.rdhi, str(self.rm), str(self.rs))

class STM(instruction):
	pass

class STR(instruction):
	pass

class STRB(instruction):
	pass

class STRH(instruction):
	pass

class SUB(instruction):
	"""
	SUB{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Subtract.
	"""
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers)
			tmp = self.rn.get(registers) - rm
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, tmp >= 0)
				registers.flag_set(registers.V, self.overflow_from(rm, self.rn.get(registers), tmp))
				
	def __str__(self):
		return "SUB%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
				
class SWP(instruction):
	pass

class SWPB(instruction):
	pass

class TEQ(instruction):
	"""
	TEQ{cond} <Rn>, <shifter_operand>
	
	Compare using EOR.
	"""
	def __init__(self, cond, rn, shifter_operand):
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand

	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers, flags=True)
			alu_out = rm ^ self.rn.get(registers)
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode

	def __str__(self):
		return "TEQ%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))

class TST(instruction):
	"""
	TST{cond} <Rn>, <shifter_operand>
	
	Compare using AND.
	"""
	def __init__(self, cond, rn, shifter_operand):
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand

	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.apply(registers, flags=True)
			alu_out = rm & self.rn.get(registers)
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode
			
	def __str__(self):
		return "TST%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))

class UMLAL(instruction):
	"""
	UMLAL{cond}{S} <RdLo>, <RdHi>, <Rm>, <Rs>
	
	Unsigned multiply long with accumulate.
	"""
	def __init__(self, cond, s, rdlo, rdhi, rm, rs):
		self.cond = cond
		self.s = s
		self.rdlo = rdlo
		self.rdhi = rdhi
		self.rm = rm
		self.rs = rs

	def execute(self, registers):
		# FIXME: difference between this and UMLAL?
		if self.cond(registers):
			registers[self.rdlo] = ((self.rm.get(registers) * self.rs.get(registers)) & 0xFFFFFFFF)\
				+ registers[self.rdlo]
			registers[self.rdhi] = (((self.rm.get(registers) * self.rs.get(registers)) >> 31) & 0xFFFFFFFF)\
				+ registers[self.rdhi] + self.carry_from(self.rm.get(registers) * self.rs.get(registers))
			if self.s:
				registers.flag_set(registers.N, registers[self.rdhi] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rdlo] == 0 and registers[self.rdhi] == 0)
				
		def __str__(self):
			return "UMLAL%s%s R%i, %s, %s"%\
				(self.cond.__name__, "S" if self.s else "", self.rdlo, self.rdhi, str(self.rm), str(self.rs))

class UMULL(instruction):
	"""
	UMULL{cond}{S} <RdLo>, <RdHi>, <Rm>, <Rs>
	
	Unsigned multiply long.
	"""
	def __init__(self, cond, s, rdlo, rdhi, rm, rs):
		self.cond = cond
		self.s = s
		self.rdlo = rdlo
		self.rdhi = rdhi
		self.rm = rm
		self.rs = rs

	def execute(self, registers):
		if self.cond(registers):
			registers[self.rdlo] = ((self.rm.get(registers) * self.rs.get(registers)) & 0xFFFFFFFF)
			registers[self.rdhi] = (((self.rm.get(registers) * self.rs.get(registers)) >> 31) & 0xFFFFFFFF)
			if self.s:
				registers.flag_set(registers.N, registers[self.rdhi] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rdlo] == 0 and registers[self.rdhi] == 0)

	def __str__(self):
		return "UMULL%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rdlo, self.rdhi, str(self.rm), str(self.rs))

