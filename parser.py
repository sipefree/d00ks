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



import ply.yacc as yacc
from lexer import tokens
import instruction
import cond
import register
import simulator
import memory

def p_commands_(p):
	'commands :'
	p[0] = []

def p_commands(p):
	'commands : commands line'
	p[0] = p[1] + [p[2]]

def p_linel(p):
	'line : LABEL command'
	p[0] = (p[1], p[2])

def p_line(p):
	'line : command'
	p[0] = ('', p[1])

def p_directivecmd(p):
	'command : directive'
	p[0] = p[1]

######
# ADC
######
def p_adc(p):
	'command : ADC argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.ADC(con, s, p[2].value, p[3], p[4])

######
# ADD
######
def p_add(p):
	'command : ADD argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.ADD(con, s, p[2].value, p[3], p[4])

######
# AND
######
def p_and(p):
	'command : AND argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.AND(con, s, p[2].value, p[3], p[4])


######
# BRANCH
######
def p_brch(p):
	'command : B branchtarget'
	(ins, con, s, other) = p[1]
	p[0] = instruction.B(other, con, p[2])


######
# BIC
######
def p_bic(p):
	'command : BIC argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.BIC(con, s, p[2].value, p[3], p[4])


######
# BKPT
######
def p_bkpt(p):
	'command : BKPT'
	p[0] = instruction.BKPT()

######
# BLX
######

######
# BX
######

######
# BXJ
######

# TODO: Implement CLZ

######
# CLZ
######

######
# CMN
######
def p_cmn(p):
	'command : CMN argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.CMN(con, p[2].value, p[3])




######
# CMP
######
def p_cmp(p):
	'command : CMP argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.CMP(con, p[2], p[3])




# ######
# # CPY
# ######
# def p_cpy(p):
# 	'command : cpy_cmd argument argument'
# 	(cmd, con, s) = p[1]
# 	p[0] = instruction.MOV(con, False, p[2].value, instruction.Shifter(p[3]))
# 
# def p_cpyc(p):
# 	'cpy_cmd : CPY condition'
# 	p[0] = (p[1], p[2], False)
# 
# def p_cpy_(p):
# 	'cpy_cmd : CPY'
# 	p[0] = (p[1], cond.AL, False)
# 


######
# EOR
######
def p_eor(p):
	'command : EOR argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.EOR(con, s, p[2].value, p[3], p[4])

######
# LDR
######
def p_ldr(p):
	'command : LDR argument addrmode'
	(ins, con, s, other) = p[1]
	if other == False:
		p[0] = instruction.LDR(con, p[2].value, p[3])
	elif other == "B":
		p[0] = instruction.LDRB(con, p[2].value, p[3])
	elif other == "SB":
		p[0] = instruction.LDRSB(con, p[2].value, p[3])
	elif other == "H":
		p[0] = instruction.LDRH(con, p[2].value, p[3])
	elif other =="SH":
		p[0] = instruction.LDRSH(con, p[2].value, p[3])


######
# MLA
######
def p_mla(p):
	'command : MLA argument argument argument argument'
	(ins, con, s, other) = p[1]
	p[0] = instruction.MLA(con, s, p[2].value, p[3], p[4], p[5])

######
# MOV
######
def p_mov(p):
	'command : MOV argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.MOV(con, bool(s), p[2].value, p[3])


######
# MRS
######

######
# MSR
######

######
# MUL
######
def p_mul(p):
	'command : MUL argument argument argument argument'
	(ins, con, s, other) = p[1]
	p[0] = instruction.MUL(con, s, p[2].value, p[3], p[4], p[5])


######
# MVN
######
def p_mvn(p):
	'command : MVN argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.MVN(con, bool(s), p[2].value, p[3])

	
######
# ORR
######
def p_orr(p):
	'command : ORR argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.ORR(con, s, p[2].value, p[3], p[4])


######
# RSB
######
def p_rsb(p):
	'command : RSB argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.RSB(con, s, p[2].value, p[3], p[4])

	
######
# RSC
######
def p_rsc(p):
	'command : RSC argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.RSC(con, s, p[2].value, p[3], p[4])

	
######
# SBC
######
def p_sbc(p):
	'command : SBC argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.SBC(con, s, p[2].value, p[3], p[4])


######
# SMLAL
######
def p_smlal(p):
	'command : SMLAL argument argument argument argument'
	(ins, con, s, other) = p[1]
	p[0] = instruction.SMLAL(con, s, p[2].value, p[3].value, p[4], p[5])


######
# SMULL
######
def p_smull(p):
	'command : SMULL argument argument argument argument'
	(ins, con, s, other) = p[1]
	p[0] = instruction.SMULL(con, s, p[2].value, p[3].value, p[4], p[5])

######
# STR
######
def p_str(p):
	'command : STR argument addrmode'
	(ins, con, s, other) = p[1]
	if other == False:
		p[0] = instruction.STR(con, p[2].value, p[3])
	elif other == "B":
		p[0] = instruction.STRB(con, p[2].value, p[3])
	elif other == "H":
		p[0] = instruction.STRH(con, p[2].value, p[3])


######
# SUB
######
def p_sub(p):
	'command : SUB argument argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.SUB(con, s, p[2].value, p[3], p[4])



######
# TEQ
######
def p_teq(p):
	'command : TEQ argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.TEQ(con, p[2].value, p[3])


######
# TST
######
def p_tst(p):
	'command : TST argument shifter'
	(ins, con, s, other) = p[1]
	p[0] = instruction.TST(con, p[2].value, p[3])
	
	
######
# UMLAL
######
def p_umlal(p):
	'command : UMLAL argument argument argument argument'
	(ins, con, s, other) = p[1]
	p[0] = instruction.UMLAL(con, s, p[2].value, p[3].value, p[4], p[5])


######
# DCB
######
def p_dcb(p):
	'command : DCB dcb_list'
	p[0] = memory.DCB(p[2])

def p_dcb_list_(p):
	'dcb_list : dcb_item'
	p[0] = [p[1]]

def p_dcb_list(p):
	'dcb_list : dcb_list dcb_item'
	p[0] = p[1] + [p[2]]

#########
# SPACE
#########
def p_space(p):
	'command : SPACE memnum'
	p[0] = memory.SPACE(p[2])

def p_memnum(p):
	'memnum : MEMNUM'
	p[0] = p[1]

def p_hexmemnum(p):
	'memnum : MEMHEXNUM'
	p[0] = p[1]


######
# UMULL
######
def p_umull(p):
	'command : UMULL argument argument argument argument'
	(ins, con, s, other) = p[1]
	p[0] = instruction.UMULL(con, s, p[2].value, p[3].value, p[4], p[5])



###########
# target
###########

def p_target_label(p):
	'target : LABELTARGET'
	p[0] = p[1]
	
def p_target_imm(p):
	'target : IMMTARGET'
	p[0] = p[1]

def p_target_immhex(p):
	'target : IMMHEXTARGET'
	p[0] = p[1]

################
# branchtarget
################

def p_branchtarget_label(p):
	'branchtarget : LABEL'
	p[0] = instruction.BranchTarget(True, p[1])

def p_branchtarget_addr(p):
	'branchtarget : argument'
	p[0] = p[1]
	
###############
# addrmode
###############

def p_addrmode_preindexed(p):
	'addrmode : OPENSQ REGISTER shifter CLOSESQ BANG'
	p[0] = instruction.AddrmodePreindexed(p[2].value, p[3])

def p_addrmode_immoffset(p):
	'addrmode : OPENSQ REGISTER shifter CLOSESQ'
	p[0] = instruction.AddrmodeImmoffset(p[2].value, p[3])

def p_addrmode_postindexed(p):
	'addrmode : OPENSQ REGISTER CLOSESQ shifter'
	p[0] = instruction.AddrmodePostindexed(p[2].value, p[4])

def p_addrmode_reg(p):
	'addrmode : OPENSQ REGISTER CLOSESQ'
	p[0] = instruction.Addrmode(p[2].value)

def p_addrmode_label(p):
	'addrmode : target'
	p[0] = p[1]


###############
# shifter
###############

def p_shifter_arg(p):
	'shifter : argument shift argument'
	shft = p[2]
	p[0] = shft(p[1], p[3])


def p_shifter_none(p):
	'shifter : argument'
	p[0] = instruction.Shifter(p[1])



#############
# argument
#############

def p_argument_h(p):
	'argument : HEXNUM'
	p[0] = p[1]


def p_argument_i(p):
	'argument : CONSTNUM'
	p[0] = p[1]

def p_argument_r(p):
	'argument : REGISTER'
	p[0] = p[1]

def p_argument_c(p):
	'argument : CHAR'
	p[0] = p[1]

def p_argument_sp(p):
	'argument : SP'
	p[0] = instruction.reg(13)

def p_argument_lr(p):
	'argument : LR'
	p[0] = instruction.reg(14)

def p_argument_pc(p):
	'argument : PC'
	p[0] = instruction.reg(15)

########
# shift
########
def p_shift_lsl(p):
	'shift : LSL'
	p[0] = instruction.LSL

def p_shift_lsr(p):
	'shift : LSR'
	p[0] = instruction.LSR

def p_shift_asr(p):
	'shift : ASR'
	p[0] = instruction.ASR

def p_shift_ror(p):
	'shift : ROR'
	p[0] = instruction.ROR

def p_shift_rrx(p):
	'shift : RRX'
	p[0] = instruction.RRX


###############
# directive
###############
def p_directive(p):
	'directive : AREA LABEL dir_attrlist'
	p[0] = simulator.Area(p[2], p[3])


################
# dir_attrlist
################
def p_dir_attrlist_(p):
	'dir_attrlist : dir_attr'
	p[0] = [p[1]]

def p_dir_attrlist(p):
	'dir_attrlist : dir_attrlist dir_attr'
	p[0] = p[1] + [p[2]]


##############
# dir_attr
##############
def p_dir_attr_align(p):
	'dir_attr : ALIGN'
	p[0] = p[1]

def p_dir_attr_code(p):
	'dir_attr : CODE'
	p[0] = p[1]

def p_dir_attr_data(p):
	'dir_attr : DATA'
	p[0] = p[1]

def p_dir_attr_noinit(p):
	'dir_attr : NOINIT'
	p[0] = p[1]

def p_dir_attr_readonly(p):
	'dir_attr : READONLY'
	p[0] = p[1]

def p_dir_attr_readwrite(p):
	'dir_attr : READWRITE'
	p[0] = p[1]


#############
# dcb_items
#############
def p_dcb_item_string(p):
	'dcb_item : STRING'
	p[0] = p[1]

def p_dcb_item_num(p):
	'dcb_item : MEMNUM'
	p[0] = p[1]

def p_dcb_item_hexnum(p):
	'dcb_item : MEMHEXNUM'
	p[0] = p[1]


def p_error(p):
	print "Syntax error at %s!"%p

parser = yacc.yacc()





# while True:
# 	try:
# 		s = raw_input('instr > ')
# 	except EOFError:
# 		break
# 	if not s: continue
# 	instr = parser.parse(s)
# 	#prog.add_instr(instr)
# 	#prog.step()
# 	print instr
	


