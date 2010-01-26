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



import ply.lex as lex
import instruction
import cond

"""
Notes:
Originally the compiler tried to match things like
<instruction> <condition> <status>

This ended up causing ambiguities and didn't work ;_;

So we have a new solution. We generate every permutation of
an instruction and add it to a table, storing metadata of
the instruction (status flag on, which condition etc) in a tuple
which is handed to the parser.

The parser became much simpler due to this.
"""

_conds = ['', 'EQ', 'NE', 'CS', 'HS', 'CC', 'LO', 'MI', 'PL', 'VS', 'VC', 'HI', 'LS', 'GE', 'LT', 'GT', 'LE', 'AL']
_aconds = [cond.AL, cond.EQ, cond.NE, cond.CS, cond.HS, cond.CC, cond.LO, cond.MI, cond.PL, cond.VS, cond.VC, cond.HI, cond.LS, cond.GE, cond.LT, cond.GT, cond.LE, cond.AL]
instrs = []
perms = {}

def get_cond(s):
	return _aconds[_conds.index(s)]

def generate(instr, conds=True, status=True, other=False, fother=False):
	ret = []
	instrs.append(instr)
	if conds:
		for c in _conds:
			ret.append(instr+c)
			perms[instr+c] = (instr, get_cond(c), False, False)
			if status:
				ret.append(instr+c+"S")
				perms[instr+c+"S"] = (instr, get_cond(c), True, False)
			if other:
				for o in other:
					ret.append(instr+c+o)
					perms[instr+c+o] = (instr, get_cond(c), False, o)
			if fother:
				for o in fother:
					ret.append(instr+o+c)
					perms[instr+o+c] = (instr, get_cond(c), False, o)
	else:
		ret = [instr]
		perms[instr] = (instr, False, False, False)
		if status:
			ret.append(instr+"S")
			perms[instr+"S"] = (instr, False, True, False)
		if other:
			for o in other:
				ret.append(instr+o)
				perms[instr+o] = (instr, False, False, o)
	return ret
	

reserved = [
	'SL',
	'FP',
	'IP',
	'SP',
	'LR',
	'PC',
	
	# instructions
	] + \
	generate('ADC') +\
	generate('ADD') +\
	generate('AND') +\
	['ASR'] +\
	generate('B', fother=['X', 'L']) +\
	generate('LDR', status=False, other=['B', 'H', 'SB', 'SH']) +\
	generate('BIC', status=False) +\
	['BKPT'] +\
	generate('CMN', status=False) +\
	generate('CMP', status=False) +\
	generate('EOR') +\
	generate('LDM', status=False, other=['IA', 'IB', 'DA', 'DB', 'FD', 'FA', 'ED', 'EA']) +\
	['LSL'] +\
	['LSR'] +\
	generate('MLA') +\
	generate('MOV') +\
	generate('MRS') +\
	generate('MSR', status=False) +\
	generate('MUL') +\
	generate('MVN') +\
	generate('ORR') +\
	['ROR'] +\
	['RRX'] +\
	generate('RSB') +\
	generate('RSC') +\
	generate('SBC') +\
	generate('SMLAL') +\
	generate('SMULL') +\
	generate('STM', status=False, other=['IA', 'IB', 'DA', 'DB', 'FD', 'FA', 'ED', 'EA']) +\
	generate('STR', status=False, other=['B', 'H', 'SB', 'SH']) +\
	generate('SUB') +\
	generate('SWP', status=False, other=['B']) +\
	generate('TEQ', status=False) +\
	generate('TST', status=False) +\
	generate('UMLAL') +\
	generate('UMULL') + [
	#directives
	'AREA',
	'CODE',
	'DATA',
	'READONLY',
	'ALIGN',
	'READWRITE',
	'NOINIT',
	
	# memory
	'DCB',
	'DCW',
	'DCH',
	'SPACE']

stuff = [
	'CONSTNUM',
	'HEXNUM',
	'REGISTER',
	'LABEL',
	'LABELTARGET',
	'IMMTARGET',
	'IMMHEXTARGET',
	'COMMENT',
	'STATUS',
	'OPENSQ',
	'CLOSESQ',
	'STRING',
	'CHAR',
	'MEMNUM',
	'MEMHEXNUM',
	'BANG',	
	'OPENCB',
	'CLOSECB',
	'TO',
]
tokens = stuff + reserved

t_OPENSQ = r'\['
t_CLOSESQ = r'\]'
t_BANG = r'!'
t_TO = r'-'
t_OPENCB = r'{'
t_CLOSECB = r'}'

t_ignore = ' \t,'

def t_STRING(t):
	r'\"([^\\\n]|(\\.))*?\"'
	t.value = t.value[1:-1]
	return t

def t_CHAR(t):
	r'\#\'.\''
	t.value = instruction.num(ord(t.value[2:-1]))
	return t

def t_HEXNUM(t):
	r'\#[-+]?0x[A-Fa-f0-9]+'
	t.value = instruction.num(int(t.value[1:], 16))
	return t

def t_CONSTNUM(t):
	r'\#[-+]?\d+'
	t.value = instruction.num(int(t.value[1:]))
	return t
	
def t_MEMHEXNUM(t):
	r'[-+]?0x[A-Fa-f0-9]+'
	t.value = int(t.value, 16)
	return t

def t_MEMNUM(t):
	r'[-+]?\d+'
	t.value = int(t.value)
	return t

def t_REGISTER(t):
	r'[Rr]\d?\d'
	t.value = instruction.reg(int(t.value[1:]))
	return t

#t_B = r'(b|B)'
#t_BL = r'(bl|BL)'
#t_STATUS = r'(s|S)'

t_SL = r'(sl|SL)'
t_FP = r'(fp|FP)'
t_IP = r'(ip|IP)'
t_SP = r'(sp|SP)'
t_LR = r'(lr|LR)'
t_PC = r'(pc|PC)'

t_AREA = r'(area|AREA)'
t_CODE = r'(code|CODE)'
t_DATA = r'(data|DATA)'
t_READONLY = r'(readonly|READONLY)'
t_ALIGN = r'(align|ALIGN)'
t_READWRITE = r'(readwrite|READWRITE)'
t_NOINIT = r'(noinit|NOINIT)'

t_DCB = r'(dcb|DCB)'
t_DCW = r'(dcw|DCW)'
t_DCH = r'(dch|DCH)'
t_SPACE = r'(space|SPACE)'


def t_IMMHEXTARGET(t):
	r'\=0x([A-Fa-f0-9])+'
	t.value = instruction.immediate(int(t.value[1:], 16))
	return t

def t_IMMTARGET(t):
	r'\=\d+'
	t.value = instruction.immediate(int(t.value[1:]))
	return t

def t_COMMENT(t):
	r'\;.*'
	pass
	

def t_newline(t):
	r'\n+'
	t.lexer.lineno += len(t.value)

def t_error(t):
    print "Illegal character '%s'" % t.value[0]
    t.lexer.skip(1)

def t_LABEL(t):
	r'[a-zA-Z_]([a-zA-Z0-9_]+)?'
	if t.value.upper() in perms:
		t.type = perms[t.value.upper()][0]
		t.value = perms[t.value.upper()]
	elif t.value.upper() in reserved:
		t.type = t.value.upper()
	return t

def t_LABELTARGET(t):
	r'\=[a-zA-Z_][a-zA-Z0-9_]+'
	t.value = instruction.label(t.value[1:])
	return t

lex.lex()

# instrs = """
# ; full line comment
# start MOVALS R0, R1, LSL #3
# ADD R0, #2, #0x3 ; comment blah
# end B end
# LDR R0, =4
# LDRB R1, =durr
# """
# lex.input(instrs)
# while 1:
# 	tok  = lex.token()
# 	if not tok: break
# 	print tok
# 

def toks():
	while 1:
		tok = lex.token()
		if not tok: break
		print tok