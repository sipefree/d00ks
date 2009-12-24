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

reserved = [
	'SL',
	'FP',
	'IP',
	'SP',
	'LR',
	'PC',
	
	# instructions
	'ADC',
	'ADD',
	'AND',
	'ASR',
	'B',
	'BL',
	'BAL',
	'BCC',
	'BCS',
	'BEQ',
	'BGE',
	'BGT',
	'BHI',
	'BHS',
	'BLE',
	'BLO',
	'BLS',
	'BLT',
	'BMI',
	'BNE',
	'BPL',
	'BVC',
	'BVS',
	
	'BLAL',
	'BLCC',
	'BLCS',
	'BLEQ',
	'BLGE',
	'BLGT',
	'BLHI',
	'BLHS',
	'BLLE',
	'BLLO',
	'BLLS',
	'BLLT',
	'BLMI',
	'BLNE',
	'BLPL',
	'BLVC',
	'BLVS',
	
	'BIC',
	'BKPT',
	'BX',
	'CMN',
	'CMP',
	'EOR',
	'LDM',
	'LDR',
	'LDRB',
	'LDRH',
	'LDSB',
	'LDSH',
	'LSL',
	'LSR',
	'MLA',
	'MOV',
	'MRS',
	'MSR',
	'MUL',
	'MVN',
	'ORR',
	'ROR',
	'RRX',
	'RSB',
	'RSC',
	'SBC',
	'SMLAL',
	'SMULL',
	'STM',
	'STR',
	'STRB',
	'STRH',
	'SUB',
	'SWP',
	'SWPB',
	'TEQ',
	'TST',
	'UMLAL',
	'UMULL',
	
	# conditionals
	'AL',
	'CC',
	'CS',
	'EQ',
	'GE',
	'GT',
	'HI',
	'HS',
	'LE',
	'LO',
	'LS',
	'LT',
	'MI',
	'NE',
	'PL',
	'VC',
	'VS',

	# directives
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
	'SPACE',
]

tokens = [
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
	'MEMNUM',
	'MEMHEXNUM',
	
] + reserved

t_OPENSQ = r'\['
t_CLOSESQ = r'\]'

t_ignore = ' \t,'

def t_STRING(t):
	r'\"([^\\\n]|(\\.))*?\"'
	t.value = t.value[1:-1]
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

t_B = r'(b|B)'
t_BL = r'(bl|BL)'
t_STATUS = r'(s|S)'

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

t_ADC = r'(adc|ADC)'
t_ADD = r'(add|ADD)'
t_AND = r'(and|AND)'
t_ASR = r'(asr|ASR)'

t_BAL = r'(bal|BAL)'
t_BCC = r'(bcc|BCC)'
t_BCS = r'(bcs|BCS)'
t_BEQ = r'(beq|BEQ)'
t_BGE = r'(bge|BGE)'
t_BGT = r'(bgt|BGT)'
t_BHI = r'(bhi|BHI)'
t_BHS = r'(bhs|BHS)'
t_BLE = r'(ble|BLE)'
t_BLO = r'(blo|BLO)'
t_BLS = r'(bls|BLS)'
t_BLT = r'(blt|BLT)'
t_BMI = r'(bmi|BMI)'
t_BNE = r'(bne|BNE)'
t_BPL = r'(bpl|BPL)'
t_BVC = r'(bvc|BVC)'
t_BVS = r'(bvs|BVS)'

t_BLAL = r'(blal|BLAL)'
t_BLCC = r'(blcc|BLCC)'
t_BLCS = r'(blcs|BLCS)'
t_BLEQ = r'(bleq|BLEQ)'
t_BLGE = r'(blge|BLGE)'
t_BLGT = r'(blgt|BLGT)'
t_BLHI = r'(blhi|BLHI)'
t_BLHS = r'(blhs|BLHS)'
t_BLLE = r'(blle|BLLE)'
t_BLLO = r'(bllo|BLLO)'
t_BLLS = r'(blls|BLLS)'
t_BLLT = r'(bllt|BLLT)'
t_BLMI = r'(blmi|BLMI)'
t_BLNE = r'(blne|BLNE)'
t_BLPL = r'(blpl|BLPL)'
t_BLVC = r'(blvc|BLVC)'
t_BLVS = r'(blvs|BLVS)'


t_BIC = r'(bic|BIC)'
t_BKPT = r'(bkpt|BKPT)'
t_BX = r'(bx|BX)'
t_CMN = r'(cmn|CMN)'
t_CMP = r'(cmp|CMP)'
t_EOR = r'(eor|EOR)'
t_LDM = r'(ldm|LDM)'
t_LDR = r'(ldr|LDR)'
t_LDRB = r'(ldrb|LDRB)'
t_LDRH = r'(ldrh|LDRH)'
t_LDSB = r'(ldsb|LDSB)'
t_LDSH = r'(ldsh|LDSH)'
t_LSL = r'(lsl|LSL)'
t_LSR = r'(lsr|LSR)'
t_MLA = r'(mla|MLA)'
t_MOV = r'(mov|MOV)'
t_MRS = r'(mrs|MRS)'
t_MSR = r'(msr|MSR)'
t_MUL = r'(mul|MUL)'
t_MVN = r'(mvn|MVN)'
t_ORR = r'(orr|ORR)'
t_ROR = r'(ror|ROR)'
t_RRX = r'(rrx|RRX)'
t_RSB = r'(rsb|RSB)'
t_RSC = r'(rsc|RSC)'
t_SBC = r'(sbc|SBC)'
t_SMLAL = r'(smlal|SMLAL)'
t_SMULL = r'(smull|SMULL)'
t_STM = r'(stm|STM)'
t_STR = r'(str|STR)'
t_STRB = r'(strb|STRB)'
t_STRH = r'(strh|STRH)'
t_SUB = r'(sub|SUB)'
t_SWP = r'(swp|SWP)'
t_SWPB = r'(swpb|SWPB)'
t_TEQ = r'(teq|TEQ)'
t_TST = r'(tst|TST)'
t_UMLAL = r'(umlal|UMLAL)'
t_UMULL = r'(umull|UMULL)'
t_AL = r'(al|AL)'
t_CC = r'(cc|CC)'
t_CS = r'(cs|CS)'
t_EQ = r'(eq|EQ)'
t_GE = r'(ge|GE)'
t_GT = r'(gt|GT)'
t_HI = r'(hi|HI)'
t_HS = r'(hs|HS)'
t_LE = r'(le|LE)'
t_LO = r'(lo|LO)'
t_LS = r'(ls|LS)'
t_LT = r'(lt|LT)'
t_MI = r'(mi|MI)'
t_NE = r'(ne|NE)'
t_PL = r'(pl|PL)'
t_VC = r'(vc|VC)'
t_VS = r'(vs|VS)'

def t_LABEL(t):
	r'[a-zA-Z_][a-zA-Z0-9_]+'
	t.type = t.value if t.value in reserved else "LABEL"
	return t

def t_LABELTARGET(t):
	r'\=[A-Za-z_][a-zA-Z0-9_]+'
	t.value = instruction.label(t.value[1:])
	return t

def t_IMMTARGET(t):
	r'\=\d+'
	t.value = instruction.immediate(int(t.value[1:]))
	return t

def t_IMMHEXTARGET(t):
	r'\=0x[A-Fa-f0-9]+'
	t.value = instruction.immediate(int(t.value[1:], 16))
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