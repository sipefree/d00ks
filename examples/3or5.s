AREA ThreeOrFive, CODE, READONLY

start
	B main

divide
	LDR R0, =0
	LDR R1, =0
L1
	CMP R2, R3
	BLT L2
	SUB R2, R2, R3
	ADD R0, R0, #1
	B L1
L2
	MOV R1, R2
	MOV PC, LR

main
	LDR R4, =1
	LDR R5, =0
L3
	CMP R4, #1000
	BEQ L4
	MOV R2, R4
	MOV R3, #3
	BL divide
	CMP R1, #0
	BEQ L5
	MOV R2, R4
	MOV R3, #5
	BL divide
	CMP R1, #0
	BEQ L5
	B L6
L5
	ADD R5, R5, R4
L6
	ADD R4, R4, #1
	B L3

L4
	B L4
