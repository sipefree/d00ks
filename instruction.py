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
import promise

class Argument(object):
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
	
	@promise.sensible()
	@promise.pure()
	def get(self, registers):
		return registers[self.value] if self.isregister else self.value
	
	@promise.sensible()
	@promise.pure()
	def value(self):
		return self.value
	
	@promise.sensible()
	@promise.pure()	
	def __str__(self):
		if self.isregister:
			return "R%i"%self.value
		else:
			return "#0x%X"%self.value


# helpers for each of the registers, useful
# for debugging purposes
R0 = Argument(True, 0)
R1 = Argument(True, 1)
R2 = Argument(True, 2)
R3 = Argument(True, 3)
R4 = Argument(True, 4)
R5 = Argument(True, 5)
R6 = Argument(True, 6)
R7 = Argument(True, 7)
R8 = Argument(True, 8)
R9 = Argument(True, 9)
R10 = Argument(True, 10)
R11 = Argument(True, 11)
R12 = Argument(True, 12)
R13 = Argument(True, 13)
R14 = Argument(True, 14)
R15 = Argument(True, 15)

@promise.sensible()
@promise.pure()
def reg(i):
	'Helper function for creating arguments'
	return Argument(True, i)

@promise.sensible()
@promise.pure()
def num(i):
	'Helper function for creating arguments'
	return Argument(False, i)
	
class Target(object):
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

	@promise.sensible()
	@promise.pure()
	def get(self, registers):
		return registers.symbol_abs(self.value) if self.islabel else self.value

	@promise.sensible()
	@promise.pure()
	def __str__(self):
		return "=%s"%(self.value if self.islabel else "%X"%self.value)

class BranchTarget(Target):
	"""
	The branch (B) instruction uses targets but the syntax doesn't
	use the = sign. This is just for pretty printing.
	"""
	def __str__(self):
		return "%s"%(self.value if self.islabel else "%X"%self.value)

@promise.sensible()
@promise.pure()
def label(lab):
	'Helper function for creating targets'
	return Target(True, lab)

@promise.sensible()
@promise.pure()
def immediate(i):
	'Helper function for creating targets'
	return Target(False, i)

class Addrmode(object):
	'''Just a register'''
	def __init__(self, rn):
		self.rn = rn
	def __repr__(self):
		return str(self)
	
	@promise.sensible()
	@promise.pure()
	def get(self, registers):
		return registers[self.rn]
	def __str__(self):
		return "[R%i]"%self.rn

class AddrmodeImmoffset(Addrmode):
	'''Immediate offset'''
	def __init__(self, rn, shifter_operand):
		self.rn = rn
		self.shifter_operand = shifter_operand
	
	@promise.sensible()
	@promise.pure()
	def get(self, registers):
		return registers[self.rn] + self.shifter_operand.get(registers)
	def __str__(self):
		return "[R%i, %s]"%(self.rn, self.shifter_operand)

class AddrmodePreindexed(Addrmode):
	'''Pre-indexed register'''
	def __init__(self, rn, shifter_operand):
		self.rn = rn
		self.shifter_operand = shifter_operand
	
	@promise.sensible()
	@promise.pure()
	def get(self, registers):
		registers[self.rn] += self.shifter_operand.get(registers)
		return registers[self.rn]
	def __str__(self):
		return "[R%i, %s]!"%(self.rn, self.shifter_operand)
	
class AddrmodePostindexed(Addrmode):
	'''Post-indexed register'''
	def __init__(self, rn, shifter_operand):
		self.rn = rn
		self.shifter_operand = shifter_operand
		
	@promise.sensible()
	@promise.pure()
	def get(self, registers):
		val = registers[self.rn]
		registers[self.rn] += self.shifter_operand.get(registers)
		return val
	def __str__(self):
		return "[R%i], %s"%(self.rn, str(self.shifter_operand))
		

class Shifter(object):
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
		super(Shifter, self).__init__()
		self.rm = rm
		
	@promise.sensible()
	@promise.pure()
	def get(self, registers, flags=False):
		return self.rm.get(registers)
	
	def __str__(self):
		return str(self.rm)

class ASR(Shifter):
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

	@promise.sensible()
	def get(self, registers, flags=False):
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

class LSL(Shifter):
	"""
	rm, LSL <val>
	
	Logical shift left. Shifts contents left by <val>.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg
	
	def __str__(self):
		return "%s, LSL %s"%(str(self.rm), str(self.arg))
	
	@promise.sensible()
	def get(self, registers, flags=False):
		"""Applies an LSL of amount value to the register"""
		val = min(self.arg.get(registers), 32)
		tmp = self.rm.get(registers) << val
		retval = tmp & 0xFFFFFFFF
		if flags:
			registers.flag_set(registers.C, tmp & (1 << 32))
		return retval

class LSR(Shifter):
	"""
	rm, LSR <val>
	
	Logical shift right.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg

	def __str__(self):
		return "%s, LSR %s"%(str(self.rm), str(self.arg))

	@promise.sensible()
	def get(self, registers, flags=False):
		"""Applies an LSR of amount value to the register"""
		val = min(self.arg.get(registers), 32)
		tmp = self.rm.get(registers) >> val
		retval = tmp & 0xFFFFFFFF
		if flags:
			registers.flag_set(registers.C, (self.rm.get(registers) >> (val-1)) & 1)
		return retval

class ROR(Shifter):
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

	@promise.sensible()
	def get(self, registers, flags=False):
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

class RRX(Shifter):
	"""
	rm, ROR <val>
	
	33-bit rotate right, using the C flag as the 33rd bit.
	"""
	def __init__(self, rm, arg):
		self.rm = rm
		self.arg = arg

	def __str__(self):
		return "%s, RRX %s"%(str(self.rm), str(self.arg))

	@promise.sensible()
	def get(self, registers, flags=False):
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
		

class Instruction(object):
	"""
	Abstract class representing an instruction.
	
	The default constructor takes arguments that are standard
	for many instructions. Instructions that don't take these
	arguments should override this method.
	
	The class also contains some helper functions for determining
	carry and overflow and signedness.
	"""
	def __init__(self, cond, s, rd, rn,  shifter_operand):
		super(Instruction, self).__init__()
		self.cond = cond
		self.s = s
		self.rn = rn
		self.rd = rd
		self.shifter_operand = shifter_operand
	
	def __str__(self):
		return "_UNKNOWN_INSTR_%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
		
	@promise.sensible()
	@promise.pure()
	def signed_pos(self, value):
		'Is the value positive?'
		return not (value & (1 << 31))
	
	@promise.sensible()
	@promise.pure()
	def signed_neg(self, value):
		'Is the value negative'
		return value & (1 << 31)
	
	@promise.sensible()
	@promise.pure()
	def sign(self, value):
		'What is the sign of value?'
		return 1 if self.signed_pos(value) else -1
		
	@promise.sensible()
	@promise.pure()
	def carry_from(self, value):
		'Is there carry in a 33 bit value?'
		return 1 if value & (1 << 32) else 0
	
	@promise.sensible()
	@promise.pure()
	def overflow_from(self, operation, rn, rm, value):
		"""
		Overflow occurs when:
			Addition:
				Both operands have the same sign but the
				result's sign is different.
			Subtraction:
				Both operands have different signs and
				the sign of the first operand is the
				same as the sign of the answer.
		"""
		if operation == 1:
			# addition
			return self.sign(rn) == self.sign(rm) and self.sign(rn) != self.sign(value)
		elif operation == 2:
			return self.sign(rn) != self.sign(rm) and self.sign(rn) == self.sign(value)
		
		return False
			
	@promise.sensible()
	@promise.pure()
	def twos_compliment(self, value):
		'Returns twos compliment of a value'
		return ((~value) + 1) & 0xFFFFFFFF
	
	def execute(self, registers):
		pass
	
	def __repr__(self):
		return str(self)
		
class ADC(Instruction):
	"""
	ADC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Add with carry. Adds two values and accumulates it with
	the current value of the carry bit.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			tmp = rm + self.rn.get(registers) + (1 if registers.flag_get(registers.C) else 0)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, self.carry_from(tmp))
				registers.flag_set(registers.V, self.overflow_from(1, rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "ADC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
				
class ADD(Instruction):
	"""
	ADD{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Adds two values.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			tmp = rm + self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, self.carry_from(tmp))
				registers.flag_set(registers.V, self.overflow_from(1, rm, self.rn.get(registers), tmp))
	def __str__(self):
		return "ADD%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
		

class AND(Instruction):
	"""
	AND{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Calculates binary AND of two values.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers, flags = self.s)
			tmp = rm & self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "AND%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class B(Instruction):
	"""
	B{L}{cond} <target_address>
	
	Branch to target.
	"""
	def __init__(self, link, cond, target):
		self.link = link
		self.cond = cond
		self.target = target
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			if self.link:
				registers[registers.LR] = registers[registers.PC]
			registers[registers.PC] = self.target.get(registers)

	def __str__(self):
		return "B%s%s %s"%\
			("L" if self.link else "", self.cond.__name__, str(self.target))
	
class BIC(Instruction):
	"""
	BIC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Clear the bits specified by shifter_operand in Rn.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers, flags = self.s)
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

class BKPT(Instruction):
	def __init__(self):
		pass
	@promise.sensible()
	def execute(self, registers):
		raise simulator.Breakpoint()

class BX(B):
	pass

class CMN(Instruction):
	"""
	CMN{cond} Rn, <shifter_operand>
	
	Compare negative.
	"""
	def __init__(self, cond, rn, shifter_operand):
		super(Instruction, self).__init__()
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand

	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			alu_out = self.rn.get(registers) + rm
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode
			registers.flag_set(registers.C, self.carry_from(alu_out))
			registers.flag_set(registers.V, self.overflow_from(1, self.rn.get(registers), rm, alu_out))

	def __str__(self):
		return "CMN%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))

class CMP(Instruction):
	"""
	CMP{cond} <Rn>, <shifter_operand>
	
	Compare.
	"""
	def __init__(self, cond, rn, shifter_operand):
		super(Instruction, self).__init__()
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			alu_out = self.rn.get(registers) - rm
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode
			registers.flag_set(registers.C, alu_out >= 0)
			registers.flag_set(registers.V, self.overflow_from(-1, self.rn.get(registers), rm, alu_out))
			
	def __str__(self):
		return "CMP%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))
	
class EOR(Instruction):
	"""
	EOR{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Exclusive-OR
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers, flags = self.s)
			tmp = rm ^ self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "EOR%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class LDM(Instruction):
	pass

class LDR(Instruction):
	"""
	LDR{<cond>} <Rd>, <addressing_mode>
	
	Load-register
	"""
	def __init__(self, cond, rd, addr_mode):
		self.cond = cond
		self.rd = rd
		self.addr_mode = addr_mode
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			addr = self.addr_mode.get(registers)
			if type(self.addr_mode) == Target:
				registers[self.rd] = addr
			else:
				word = registers.memory.ldrw(addr)
				registers[self.rd] = word
	
	def __str__(self):
		return "LDR%s R%i, %s"%\
			(self.cond.__name__, self.rd, str(self.addr_mode))
	
class LDRB(Instruction):
	"""
	LDR{<cond>}B <Rd>, <addressing_mode>
	
	Load-register
	"""
	def __init__(self, cond, rd, addr_mode):
		self.cond = cond
		self.rd = rd
		self.addr_mode = addr_mode
		if type(addr_mode) == Target:
			raise SyntaxError("LDRB: Psuedoinstruction only allowed in word-form. (Must use LDR instead)")
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			addr = self.addr_mode.get(registers)
			byte = registers.memory.ldrb(addr)
			registers[self.rd] = byte
	
	def __str__(self):
		return "LDR%sB R%i, %s"%\
			(self.cond.__name__, self.rd, str(self.addr_mode))

class LDRH(Instruction):
	"""
	LDR{<cond>}H <Rd>, <addressing_mode>
	
	Load-register
	"""
	def __init__(self, cond, rd, addr_mode):
		self.cond = cond
		self.rd = rd
		self.addr_mode = addr_mode
		if type(addr_mode) == Target:
			raise SyntaxError("LDRB: Psuedoinstruction only allowed in word-form. (Must use LDR instead)")
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			addr = self.addr_mode.get(registers)
			hw = registers.memory.ldrh(addr)
			registers[self.rd] = byte
			
	def __str__(self):
		return "LDR%sH R%i, %s"%\
			(self.cond.__name__, self.rd, str(self.addr_mode))

class LDSB(Instruction):
	"""
	LDR{<cond>}SB <Rd>, <addressing_mode>
	
	Load-register
	"""
	def __init__(self, cond, rd, addr_mode):
		self.cond = cond
		self.rd = rd
		self.addr_mode = addr_mode
		if type(addr_mode) == Target:
			raise SyntaxError("LDRB: Psuedoinstruction only allowed in word-form. (Must use LDR instead)")
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			addr = self.addr_mode.get(registers)
			byte = registers.memory.ldrb(addr)
			if byte & 0x80:
				byte = byte | 0xFFFFFF00
			registers[self.rd] = byte
	
	def __str__(self):
		return "LDR%sSB R%i, %s"%\
			(self.cond.__name__, self.rd, str(self.addr_mode))

class LDSH(Instruction):
	"""
	LDR{<cond>}SB <Rd>, <addressing_mode>
	
	Load-register
	"""
	def __init__(self, cond, rd, addr_mode):
		self.cond = cond
		self.rd = rd
		self.addr_mode = addr_mode
		if type(addr_mode) == Target:
			raise SyntaxError("LDRB: Psuedoinstruction only allowed in word-form. (Must use LDR instead)")
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			addr = self.addr_mode.get(registers)
			hw = registers.memory.ldrh(addr)
			if hw & 0x8000:
				hw = hw | 0xFFFF0000
			registers[self.rd] = hw
	
	def __str__(self):
		return "LDR%sSH R%i, %s"%\
			(self.cond.__name__, self.rd, str(self.addr_mode))

class MLA(Instruction):
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
	
	@promise.sensible()
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

class MOV(Instruction):
	"""
	MOV{cond}{S} <Rd>, <shifter_operand>
	
	Move.
	"""
	def __init__(self, cond, s, rd, shifter_operand):
		self.cond = cond
		self.s = s
		self.rd = rd
		self.shifter_operand = shifter_operand
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			registers[self.rd] = self.shifter_operand.get(registers, flags=self.s)
			if self.s:
				registers.flag_set(registers.N, registers[self.rd] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "MOV%s%s R%i, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.shifter_operand))

class MRS(Instruction):
	pass

class MSR(Instruction):
	pass

class MUL(Instruction):
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
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			registers[self.rd] = self.rm.get(registers) * self.rs.get(registers)
			if self.s:
				registers.flag_set(registers.N, registers[self.rd] & (1 << 31))
				registers.flag_set(registers.N, registers[self.rd] == 0)

	def __str__(self):
		return "EOR%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rm), str(self.rs))

class MVN(Instruction):
	"""
	MVN{cond}{S} <Rd>, <shifter_operand>
	
	Move negative.
	"""
	def __init__(self, cond, s, rd, shifter_operand):
		self.cond = cond
		self.s = s
		self.rd = rd
		self.shifter_operand = shifter_operand
	
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			registers[self.rd] = ~self.shifter_operand.get(registers, flags=self.s)
			if self.s:
				registers.flag_set(registers.N, registers[self.rd] & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "MVN%s%s R%i, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.shifter_operand))

class ORR(Instruction):
	"""
	ORR{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Binary-OR.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers, flags = self.s)
			tmp = rm | self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				# C flag will be affected by shifter operand

	def __str__(self):
		return "ORR%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class RSB(Instruction):
	"""
	RSB{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Reverse subtract.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			tmp = rm - self.rn.get(registers)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, self.carry_from(tmp))
				registers.flag_set(registers.V, self.overflow_from(-1, rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "RSB%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class RSC(Instruction):
	"""
	RSC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Reverse subtract with carry.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			tmp = rm - self.rn.get(registers) - (0 if registers.flag_get(registers.C) else 1)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, registers[self.rd] >= 0)
				registers.flag_set(registers.V, self.overflow_from(-1, rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "RSC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class SBC(Instruction):
	"""
	SBC{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Subtract with carry.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			tmp = self.rn.get(registers) - rm - (0 if registers.flag_get(registers.C) else 1)
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, registers[self.rd] >= 0)
				registers.flag_set(registers.V, self.overflow_from(-1, rm, self.rn.get(registers), tmp))

	def __str__(self):
		return "SBC%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))

class SMLAL(Instruction):
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

	@promise.sensible()
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

class SMULL(Instruction):
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

	@promise.sensible()
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

class STM(Instruction):
	pass

class STR(Instruction):
	pass

class STRB(Instruction):
	pass

class STRH(Instruction):
	pass

class SUB(Instruction):
	"""
	SUB{cond}{S} <Rd>, <Rn>, <shifter_operand>
	
	Subtract.
	"""
	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers)
			tmp = self.rn.get(registers) - rm
			registers[self.rd] = tmp
			if self.s:
				registers.flag_set(registers.N, tmp & (1 << 31))
				registers.flag_set(registers.Z, registers[self.rd] == 0)
				registers.flag_set(registers.C, tmp >= 0)
				registers.flag_set(registers.V, self.overflow_from(-1, rm, self.rn.get(registers), tmp))
				
	def __str__(self):
		return "SUB%s%s R%i, %s, %s"%\
			(self.cond.__name__, "S" if self.s else "", self.rd, str(self.rn), str(self.shifter_operand))
				
class SWP(Instruction):
	pass

class SWPB(Instruction):
	pass

class TEQ(Instruction):
	"""
	TEQ{cond} <Rn>, <shifter_operand>
	
	Compare using EOR.
	"""
	def __init__(self, cond, rn, shifter_operand):
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand

	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers, flags=True)
			alu_out = rm ^ self.rn.get(registers)
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode

	def __str__(self):
		return "TEQ%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))

class TST(Instruction):
	"""
	TST{cond} <Rn>, <shifter_operand>
	
	Compare using AND.
	"""
	def __init__(self, cond, rn, shifter_operand):
		self.cond = cond
		self.rn = rn
		self.shifter_operand = shifter_operand

	@promise.sensible()
	def execute(self, registers):
		if self.cond(registers):
			rm = self.shifter_operand.get(registers, flags=True)
			alu_out = rm & self.rn.get(registers)
			registers.flag_set(registers.N, alu_out & (1 << 31))
			registers.flag_set(registers.Z, (alu_out & 0xFFFFFFFF) == 0) # force 32 bit mode
			
	def __str__(self):
		return "TST%s %s, %s"%\
			(self.cond.__name__, str(self.rn), str(self.shifter_operand))

class UMLAL(Instruction):
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

	@promise.sensible()
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

class UMULL(Instruction):
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

	@promise.sensible()
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

