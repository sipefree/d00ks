import cond
import instruction
import register

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
	
	def compile(self, tuples):
		start_s = 0
		code_s = 1
		data_s = 2
		mode = start_s
		
		code_woffset = 0
		data_boffset = 0
		
		self.code = []
		for (label,line) in tuples:
			if type(line) == area:
				if "CODE" in line.attrs:
					if "DATA" in line.attrs:
						raise SyntaxError("AREA %s cannot have both CODE and DATA attrs!"%line.label)
					mode = code_s
				continue
			if mode == code_s:
				if isinstance(line, instruction.instruction):
					self.code.append(line)
					if label:
						self.registers.symbol_insert(label, code_woffset, line)
					code_woffset += 1
	
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
	