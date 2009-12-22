import cond
import instruction
import register

class program(object):
	"""Represents an ARM program."""
	def __init__(self, instructions=[]):
		super(program, self).__init__()
		self.instructions = instructions
		self.registers = register.registers()
	
	def compile(self, instr_tuple_list):
		self.instructions = []
		i = 0
		for (label,ins) in instr_tuple_list:
			self.instructions.append(ins)
			if label:
				self.registers.symbol_insert(label, i, ins)
			i = i + 1
	
	def add_instr(self, instruction):
		self.instructions.append(instruction)
	
	def start(self):
		self.registers = register.registers()

	def step(self):
		# fetch/decode
		instr = self.instructions[self.registers[self.registers.PC]]
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
	