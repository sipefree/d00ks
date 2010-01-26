AREA	ReversePolish, CODE, READONLY

start
	LDR	R12, =STK_TOP
	LDR	R5, =EXPR

L1
	LDRB	R0, [R5], #1
	CMP	R0, #0
	BEQ	L2
	CMP	R0, #'+'
	BLEQ	addition
	BEQ	L1
	CMP	R0, #'-'
	BLEQ	subtraction
	BEQ	L1
	CMP	R0, #'*'
	BLEQ	multiply
	BEQ	L1
	BL	atoi
	STMFD	R12!, {R0}
	B	L1

L2
	LDMFD	R12!, {R0}
	B	stop



atoi
	SUB	R0, R0, #'0'
	MOV	PC, LR

addition
	LDMFD	R12!, {R1}
	LDMFD	R12!, {R0}
	ADD	R0, R0, R1
	STMFD	R12!, {R0}
	MOV	PC, LR

subtraction
	LDMFD	R12!, {R1}
	LDMFD	R12!, {R0}
	SUB	R0, R0, R1
	STMFD	R12!, {R0}
	MOV	PC, LR

multiply
	LDMFD	R12!, {R1}
	LDMFD	R12!, {R0}
	MUL	R0, R0, R1
	STMFD	R12!, {R0}
	MOV	PC, LR

stop
	B	stop

AREA	TestData, DATA, READWRITE
EXPR	DCB	"12+34+*",0

AREA	Stack, DATA, READWRITE

STK_MEM	SPACE	0x400
STK_TOP

