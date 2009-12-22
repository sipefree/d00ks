import ply.yacc as yacc
from lexer import tokens
import instruction
import cond
import register
import simulator

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

######
# ADC
######
def p_adc(p):
	'command : adc_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.ADC(con, s, p[2].value, p[3], p[4])

def p_adc_(p):
	'adc_cmd : ADC'
	p[0] = (p[1], cond.AL, False)

def p_adcs(p):
	'adc_cmd : ADC STATUS'
	p[0] = (p[1], cond.AL, True)

def p_adccs(p):
	'adc_cmd :  ADC condition STATUS'
	p[0] = (p[1], p[2], True)

def p_adcc(p):
	'adc_cmd : ADC condition'
	p[0] = (p[1], p[2], False)

######
# ADD
######
def p_add(p):
	'command : add_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.ADD(con, s, p[2].value, p[3], p[4])

def p_add_(p):
	'add_cmd : ADD'
	p[0] = (p[1], cond.AL, False)

def p_adds(p):
	'add_cmd : ADD STATUS'
	p[0] = (p[1], cond.AL, True)

def p_addcs(p):
	'add_cmd :  ADD condition STATUS'
	p[0] = (p[1], p[2], True)

def p_addc(p):
	'add_cmd : ADD condition'
	p[0] = (p[1], p[2], False)

######
# AND
######
def p_and(p):
	'command : and_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.AND(con, s, p[2].value, p[3], p[4])

def p_and_(p):
	'and_cmd : AND'
	p[0] = (p[1], cond.AL, False)

def p_ands(p):
	'and_cmd : AND STATUS'
	p[0] = (p[1], cond.AL, True)

def p_andcs(p):
	'and_cmd :  AND condition STATUS'
	p[0] = (p[1], p[2], True)

def p_andc(p):
	'and_cmd : AND condition'
	p[0] = (p[1], p[2], False)

######
# B
######
def p_brk(p):
	'command : b_cmd branchtarget'
	(cmd, con, l) = p[1]
	p[0] = instruction.B(l, con, p[2])

def p_brk_(p):
	'b_cmd : B'
	p[0] = (p[1], cond.AL, False)

def p_brkcl(p):
	'b_cmd : B LINK condition'
	p[0] = (p[1], p[3], True)

def p_brkc(p):
	'b_cmd : B condition'
	p[0] = (p[1], p[2], False)

def p_brkcl(p):
	'b_cmd : B LINK'
	p[0] = (p[1], cond.AL, True)	
	
######
# BIC
######
def p_bic(p):
	'command : bic_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.BIC(con, s, p[2].value, p[3], p[4])

def p_bic_(p):
	'bic_cmd : BIC'
	p[0] = (p[1], cond.AL, False)

def p_bics(p):
	'bic_cmd : BIC STATUS'
	p[0] = (p[1], cond.AL, True)

def p_biccs(p):
	'bic_cmd :  BIC condition STATUS'
	p[0] = (p[1], p[2], True)

def p_bicc(p):
	'bic_cmd : BIC condition'
	p[0] = (p[1], p[2], False)


######
# BKPT
######

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
	'command : cmn_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.CMN(con, s, p[2].value, p[3])

def p_cmn_(p):
	'cmn_cmd : CMN'
	p[0] = (p[1], cond.AL, False)

def p_cmns(p):
	'cmn_cmd : CMN STATUS'
	p[0] = (p[1], cond.AL, True)

def p_cmncs(p):
	'cmn_cmd :  CMN condition STATUS'
	p[0] = (p[1], p[2], True)

def p_cmnc(p):
	'cmn_cmd : CMN condition'
	p[0] = (p[1], p[2], False)

######
# CMP
######
def p_cmp(p):
	'command : cmp_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.CMP(con, s, p[2].value, p[3])

def p_cmp_(p):
	'cmp_cmd : CMP'
	p[0] = (p[1], cond.AL, False)

def p_cmps(p):
	'cmp_cmd : CMP STATUS'
	p[0] = (p[1], cond.AL, True)

def p_cmpcs(p):
	'cmp_cmd :  CMP condition STATUS'
	p[0] = (p[1], p[2], True)

def p_cmpc(p):
	'cmp_cmd : CMP condition'
	p[0] = (p[1], p[2], False)

######
# CMP
######
def p_cmp(p):
	'command : cmp_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.CMP(con, s, p[2].value, p[3])

def p_cmp_(p):
	'cmp_cmd : CMP'
	p[0] = (p[1], cond.AL, False)

def p_cmps(p):
	'cmp_cmd : CMP STATUS'
	p[0] = (p[1], cond.AL, True)

def p_cmpcs(p):
	'cmp_cmd :  CMP condition STATUS'
	p[0] = (p[1], p[2], True)

def p_cmpc(p):
	'cmp_cmd : CMP condition'
	p[0] = (p[1], p[2], False)

# ######
# # CPY
# ######
# def p_cpy(p):
# 	'command : cpy_cmd argument argument'
# 	(cmd, con, s) = p[1]
# 	p[0] = instruction.MOV(con, False, p[2].value, instruction.shifter(p[3]))
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
	'command : eor_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.EOR(con, s, p[2].value, p[3], p[4])

def p_eor_(p):
	'eor_cmd : EOR'
	p[0] = (p[1], cond.AL, False)

def p_eors(p):
	'eor_cmd : EOR STATUS'
	p[0] = (p[1], cond.AL, True)

def p_eorcs(p):
	'eor_cmd :  EOR condition STATUS'
	p[0] = (p[1], p[2], True)

def p_eorc(p):
	'bic_cmd : EOR condition'
	p[0] = (p[1], p[2], False)


######
# LDR
######

######
# MLA
######
def p_mla(p):
	'command : mla_cmd argument argument argument argument'
	(cmd, con, s) = p[1]
	p[0] = instruction.MLA(con, s, p[2].value, p[3], p[4], p[5])

def p_mla_(p):
	'mla_cmd : MLA'
	p[0] = (p[1], cond.AL, False)

def p_mlas(p):
	'mla_cmd : MLA STATUS'
	p[0] = (p[1], cond.AL, True)

def p_mlacs(p):
	'mla_cmd :  MLA condition STATUS'
	p[0] = (p[1], p[2], True)

def p_mlac(p):
	'bic_cmd : MLA condition'
	p[0] = (p[1], p[2], False)

######
# MOV
######
def p_mov(p):
	'command : mov_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.MOV(con, bool(s), p[2].value, p[3])

def p_mov_(p):
	'mov_cmd : MOV'
	p[0] = (p[1], cond.AL, False)

def p_movs(p):
	'mov_cmd : MOV STATUS'
	p[0] = (p[1], cond.AL, True)

def p_movcs(p):
	'mov_cmd : MOV condition STATUS'
	p[0] = (p[1], p[2], True)

def p_movc(p):
	'mov_cmd : MOV condition'
	p[0] = (p[1], p[2], False)

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
	'command : mul_cmd argument argument argument argument'
	(cmd, con, s) = p[1]
	p[0] = instruction.MUL(con, s, p[2].value, p[3], p[4], p[5])

def p_mul_(p):
	'mul_cmd : MUL'
	p[0] = (p[1], cond.AL, False)

def p_muls(p):
	'mul_cmd : MUL STATUS'
	p[0] = (p[1], cond.AL, True)

def p_mulcs(p):
	'mla_cmd :  MUL condition STATUS'
	p[0] = (p[1], p[2], True)


######
# MVN
######
def p_mvn(p):
	'command : mvn_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.MVN(con, bool(s), p[2].value, p[3])

def p_mvn_(p):
	'mvn_cmd : MVN'
	p[0] = (p[1], cond.AL, False)

def p_mvns(p):
	'mvn_cmd : MVN STATUS'
	p[0] = (p[1], cond.AL, True)

def p_mvncs(p):
	'mvn_cmd : MVN condition STATUS'
	p[0] = (p[1], p[2], True)

def p_mvnc(p):
	'mvn_cmd : MVN condition'
	p[0] = (p[1], p[2], False)
	
######
# ORR
######
def p_orr(p):
	'command : orr_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.ORR(con, s, p[2].value, p[3], p[4])

def p_orr_(p):
	'orr_cmd : ORR'
	p[0] = (p[1], cond.AL, False)

def p_orrs(p):
	'orr_cmd : ORR STATUS'
	p[0] = (p[1], cond.AL, True)

def p_orrcs(p):
	'orr_cmd :  ORR condition STATUS'
	p[0] = (p[1], p[2], True)

def p_orrc(p):
	'bic_cmd : ORR condition'
	p[0] = (p[1], p[2], False)

######
# RSB
######
def p_rsb(p):
	'command : rsb_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.RSB(con, s, p[2].value, p[3], p[4])

def p_rsb_(p):
	'rsb_cmd : RSB'
	p[0] = (p[1], cond.AL, False)

def p_rsbs(p):
	'rsb_cmd : RSB STATUS'
	p[0] = (p[1], cond.AL, True)

def p_rsbcs(p):
	'rsb_cmd :  RSB condition STATUS'
	p[0] = (p[1], p[2], True)

def p_rsbc(p):
	'rsb_cmd : RSB condition'
	p[0] = (p[1], p[2], False)
	
######
# RSC
######
def p_rsc(p):
	'command : rsc_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.RSC(con, s, p[2].value, p[3], p[4])

def p_rsc_(p):
	'rsc_cmd : RSC'
	p[0] = (p[1], cond.AL, False)

def p_rscs(p):
	'rsc_cmd : RSC STATUS'
	p[0] = (p[1], cond.AL, True)

def p_rsccs(p):
	'rsc_cmd :  RSC condition STATUS'
	p[0] = (p[1], p[2], True)

def p_rscc(p):
	'rsc_cmd : RSC condition'
	p[0] = (p[1], p[2], False)
	
######
# SBC
######
def p_sbc(p):
	'command : sbc_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.SBC(con, s, p[2].value, p[3], p[4])

def p_sbc_(p):
	'sbc_cmd : SBC'
	p[0] = (p[1], cond.AL, False)

def p_sbcs(p):
	'sbc_cmd : SBC STATUS'
	p[0] = (p[1], cond.AL, True)

def p_sbccs(p):
	'sbc_cmd :  SBC condition STATUS'
	p[0] = (p[1], p[2], True)

def p_sbcc(p):
	'sbc_cmd : SBC condition'
	p[0] = (p[1], p[2], False)

######
# SMLAL
######
def p_smlal(p):
	'command : smlal_cmd argument argument argument argument'
	(cmd, con, s) = p[1]
	p[0] = instruction.SMLAL(con, s, p[2].value, p[3].value, p[4], p[5])

def p_smlal_(p):
	'smlal_cmd : SMLAL'
	p[0] = (p[1], cond.AL, False)

def p_smlals(p):
	'smlal_cmd : SMLAL STATUS'
	p[0] = (p[1], cond.AL, True)

def p_smlalcs(p):
	'smlal_cmd :  SMLAL condition STATUS'
	p[0] = (p[1], p[2], True)

def p_smlalc(p):
	'smlal_cmd : SMLAL condition'
	p[0] = (p[1], p[2], False)

######
# SMULL
######
def p_smull(p):
	'command : smull_cmd argument argument argument argument'
	(cmd, con, s) = p[1]
	p[0] = instruction.SMULL(con, s, p[2].value, p[3].value, p[4], p[5])

def p_smull_(p):
	'smull_cmd : SMULL'
	p[0] = (p[1], cond.AL, False)

def p_smulls(p):
	'smull_cmd : SMULL STATUS'
	p[0] = (p[1], cond.AL, True)

def p_smullcs(p):
	'smull_cmd :  SMULL condition STATUS'
	p[0] = (p[1], p[2], True)

def p_smullc(p):
	'smull_cmd : SMULL condition'
	p[0] = (p[1], p[2], False)

######
# SUB
######
def p_sub(p):
	'command : sub_cmd argument argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.SUB(con, s, p[2].value, p[3], p[4])

def p_sub_(p):
	'sub_cmd : SUB'
	p[0] = (p[1], cond.AL, False)

def p_subs(p):
	'sub_cmd : SUB STATUS'
	p[0] = (p[1], cond.AL, True)

def p_subcs(p):
	'sub_cmd :  SUB condition STATUS'
	p[0] = (p[1], p[2], True)

def p_subc(p):
	'sub_cmd : SUB condition'
	p[0] = (p[1], p[2], False)


######
# TEQ
######
def p_teq(p):
	'command : teq_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.TEQ(con, s, p[2].value, p[3])

def p_teq_(p):
	'teq_cmd : TEQ'
	p[0] = (p[1], cond.AL, False)

def p_teqs(p):
	'teq_cmd : TEQ STATUS'
	p[0] = (p[1], cond.AL, True)

def p_teqcs(p):
	'teq_cmd :  TEQ condition STATUS'
	p[0] = (p[1], p[2], True)

def p_teqc(p):
	'teq_cmd : TEQ condition'
	p[0] = (p[1], p[2], False)

######
# TST
######
def p_tst(p):
	'command : tst_cmd argument shifter'
	(cmd, con, s) = p[1]
	p[0] = instruction.TST(con, s, p[2].value, p[3])

def p_tst_(p):
	'tst_cmd : TST'
	p[0] = (p[1], cond.AL, False)

def p_tsts(p):
	'tst_cmd : TST STATUS'
	p[0] = (p[1], cond.AL, True)

def p_tstcs(p):
	'tst_cmd :  TST condition STATUS'
	p[0] = (p[1], p[2], True)

def p_tstc(p):
	'tst_cmd : TST condition'
	p[0] = (p[1], p[2], False)
	
	
######
# UMLAL
######
def p_umlal(p):
	'command : umlal_cmd argument argument argument argument'
	(cmd, con, s) = p[1]
	p[0] = instruction.UMLAL(con, s, p[2].value, p[3].value, p[4], p[5])

def p_umlal_(p):
	'umlal_cmd : UMLAL'
	p[0] = (p[1], cond.AL, False)

def p_umlals(p):
	'umlal_cmd : UMLAL STATUS'
	p[0] = (p[1], cond.AL, True)

def p_umlalcs(p):
	'umlal_cmd :  UMLAL condition STATUS'
	p[0] = (p[1], p[2], True)

def p_umlalc(p):
	'umlal_cmd : UMLAL condition'
	p[0] = (p[1], p[2], False)
	
######
# UMULL
######
def p_umull(p):
	'command : umull_cmd argument argument argument argument'
	(cmd, con, s) = p[1]
	p[0] = instruction.UMULL(con, s, p[2].value, p[3].value, p[4], p[5])

def p_umull_(p):
	'umull_cmd : UMULL'
	p[0] = (p[1], cond.AL, False)

def p_umulls(p):
	'umull_cmd : UMULL STATUS'
	p[0] = (p[1], cond.AL, True)

def p_umullcs(p):
	'umull_cmd :  UMULL condition STATUS'
	p[0] = (p[1], p[2], True)

def p_umullc(p):
	'umull_cmd : UMULL condition'
	p[0] = (p[1], p[2], False)


###########
# NOISE
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

def p_branchtarget_label(p):
	'branchtarget : LABEL'
	p[0] = instruction.branchtarget(True, p[1])

def p_branchtarget_addr(p):
	'branchtarget : argument'
	p[0] = p[1]

def p_shifter_arg(p):
	'shifter : argument shift argument'
	shft = p[2]
	p[0] = shft(p[1], p[3])


def p_shifter_none(p):
	'shifter : argument'
	p[0] = instruction.shifter(p[1])



def p_argument_h(p):
	'argument : HEXNUM'
	p[0] = p[1]


def p_argument_i(p):
	'argument : CONSTNUM'
	p[0] = p[1]

def p_argument_r(p):
	'argument : REGISTER'
	p[0] = p[1]



def p_condition_al(p):
	'condition : AL'
	p[0] = cond.AL

def p_condition_cc(p):
	'condition : CC'
	p[0] = cond.CC

def p_condition_cs(p):
	'condition : CS'
	p[0] = cond.CS

def p_condition_eq(p):
	'condition : EQ'
	p[0] = cond.EQ

def p_condition_ge(p):
	'condition : GE'
	p[0] = cond.GE

def p_condition_gt(p):
	'condition : GT'
	p[0] = cond.GT

def p_condition_hi(p):
	'condition : HI'
	p[0] = cond.HI

def p_condition_hs(p):
	'condition : HS'
	p[0] = cond.HS

def p_condition_le(p):
	'condition : LE'
	p[0] = cond.LE

def p_condition_lo(p):
	'condition : LO'
	p[0] = cond.LO

def p_condition_ls(p):
	'condition : LS'
	p[0] = cond.LS

def p_condition_lt(p):
	'condition : LT'
	p[0] = cond.LT

def p_condition_mi(p):
	'condition : MI'
	p[0] = cond.MI

def p_condition_ne(p):
	'condition : NE'
	p[0] = cond.NE

def p_condition_pl(p):
	'condition : PL'
	p[0] = cond.PL

def p_condition_vc(p):
	'condition : VC'
	p[0] = cond.VC

def p_condition_vs(p):
	'condition : VS'
	p[0] = cond.VS

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


def p_error(p):
	print "Syntax error at %s!"%p

parser = yacc.yacc()

prog = simulator.program()

prog = """
start
	; Load a test value into R1
	
	MOV	R1, #0xAC

	; Begin by expanding the 8-bit value to 12-bits, inserting
	; zeros in the positions for the four check bits (bit 0, bit 1, bit 3
	; and bit 7).
	
	AND	R2, R1, #0x1		; Clear all bits apart from d0
	MOV	R0, R2, LSL #2		; Align data bit d0
	
	AND	R2, R1, #0xE		; Clear all bits apart from d1, d2, & d3
	ORR	R0, R0, R2, LSL #3	; Align data bits d1, d2 & d3 and combine with d0
	
	AND	R2, R1, #0xF0		; Clear all bits apart from d3-d7
	ORR	R0, R0, R2, LSL #4	; Align data bits d4-d7 and combine with d0-d3
	
	; We now have a 12-bit value in R0 with empty (0) check bits in
	; the correct positions
	
	; Generate check bit c0
	
	EOR	R2, R0, R0, LSR #2	; Generate c0 parity bit using parity tree
	EOR	R2, R2, R2, LSR #4	; ... second iteration ...
	EOR	R2, R2, R2, LSR #8	; ... final iteration
	
	AND	R2, R2, #0x1		; Clear all but check bit c0
	ORR	R0, R0, R2		; Combine check bit c0 with result
	
	; Generate check bit c1
	
	EOR	R2, R0, R0, LSR #1	; Generate c1 parity bit using parity tree
	EOR	R2, R2, R2, LSR #4	; ... second iteration ...
	EOR	R2, R2, R2, LSR #8	; ... final iteration
	
	AND	R2, R2, #0x2		; Clear all but check bit c1
	ORR	R0, R0, R2		; Combine check bit c1 with result
	
	; Generate check bit c2
	
	EOR	R2, R0, R0, LSR #1	; Generate c2 parity bit using parity tree
	EOR	R2, R2, R2, LSR #2	; ... second iteration ...
	EOR	R2, R2, R2, LSR #8	; ... final iteration
	
	AND	R2, R2, #0x8		; Clear all but check bit c2
	ORR	R0, R0, R2		; Combine check bit c2 with result	
	
	; Generate check bit c3
	
	EOR	R2, R0, R0, LSR #1	; Generate c3 parity bit using parity tree
	EOR	R2, R2, R2, LSR #2	; ... second iteration ...
	EOR	R2, R2, R2, LSR #4	; ... final iteration
	
	AND	R2, R2, #0x80		; Clear all but check bit c3
	ORR	R0, R0, R2		; Combine check bit c3 with result
	
	; We now have a 12-bit value with Hamming code check bits
	
	; Create an artificial "error" in the encoded value by flipping a single bit
	
	EOR	R0, R0, #0x100		; Flip bit 8 to test
	
	;
	; YOUR EXTENSION TO THE PROGRAM TO CORRECT SINGLE-BIT
	; ERRORS GOES HERE
	;
	
	MOV	R1, R0			; copy received value to R1
	BIC	R1, R1, #0x8B		; clear all check bits
	
	; We are now back to line 31, with a 12 bit value
	; in R1 with empty check bits

	; Generate check bit c0
	EOR	R2, R1, R1, LSR #2	; c0
	EOR	R2, R2, R2, LSR #4
	EOR	R2, R2, R2, LSR #8
	
	AND	R2, R2, #0x1
	ORR	R1, R1, R2
	
	; Generate c1
	EOR	R2, R1, R1, LSR #1
	EOR	R2, R2, R2, LSR #4
	EOR	R2, R2, R2, LSR #8
	
	AND	R2, R2, #0x2
	ORR	R1, R1, R2

	; Generate c2
	EOR	R2, R1, R1, LSR #1
	EOR	R2, R2, R2, LSR #2
	EOR	R2, R2, R2, LSR #8

	AND	R2, R2, #0x8
	ORR	R1, R1, R2

	; Generate c3
	EOR	R2, R1, R1, LSR #1
	EOR	R2, R2, R2, LSR #2
	EOR	R2, R2, R2, LSR #4

	AND	R2, R2, #0x80
	ORR	R1, R1, R2

	; We now have recreated the hamming code
	
	EOR	R3, R0, R1		; get the difference of the original and the new

	; Isolate check bits
	MOV	R4, R3 
	AND	R4, R4, #0x3		; clear all but c0, c1
	MOV	R5, R3, LSR #1		; move c2 into place
	AND	R5, R5, #0x4		; isolate c2
	ORR	R4, R4, R5			; merge c2 to check
	MOV	R5, R3, LSR #4		; move c3 into place
	AND	R5, R5, #0x8		; isolate c3
	ORR	R4, R4, R5			; merge c3 into check

	SUB	R3, R4, #1		; r3 = r4 - 1
	MOV	R2, #1			; r1 = 1
	MOV	R2, R2, LSL R3	; r2 = r2 << r3
	
	; We nowhave a 1 in the location that needs
	; to be swapped
											 
	EOR	R0, R0, R2			

stop	B	stop
"""
print "INPUT >>>"
i = 1
for line in prog.split("\n"):
	print "%i %s"%(i, line)
	i = i + 1
print ""
print "COMPILING >>>"

import pprint
pp = pprint.PrettyPrinter()


output = parser.parse(prog)
pp.pprint(output)

prog = simulator.program()
prog.compile(output)

prog.debug()



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
	


