AREA Fib, CODE, READONLY

start
	BL	main
	B	end

fib
	mov	ip, sp
	stmfd	sp!, {r4, r11, ip, lr, pc}
	sub	r11, ip, #4
	sub	sp, sp, #8
	str	r0, [r11, #-20]
	ldr	r3, [r11, #-20]
	cmp	r3, #0
	beq	L2
	ldr	r3, [r11, #-20]
	cmp	r3, #1
	bne	L4
L2
	ldr	r3, [r11, #-20]
	str	r3, [r11, #-24]
	b	L5
L4
	ldr	r3, [r11, #-20]
	sub	r3, r3, #1
	mov	r0, r3
	bl	fib
	mov	r4, r0
	ldr	r3, [r11, #-20]
	sub	r3, r3, #2
	mov	r0, r3
	bl	fib
	mov	r3, r0
	add	r4, r4, r3
	str	r4, [r11, #-24]
L5
	ldr	r3, [r11, #-24]
	mov	r0, r3
	sub	sp, r11, #16
	ldmfd	sp, {r4, r11, sp, pc}

main
	ldr	sp, =STK_TOP
	mov	ip, sp
	stmfd	sp!, {r11, ip, lr, pc}
	sub	r11, ip, #4
	sub	sp, sp, #8
	str	r0, [r11, #-16]
	str	r1, [r11, #-20]
	mov	r0, #20
	bl	fib
	mov	r3, r0
	mov	r0, r3
	sub	sp, r11, #12
	ldmfd	sp, {r11, sp, pc}

stop
	B stop

AREA	Stack, DATA, READWRITE
STK_MEM	SPACE, 4096
STK_TOP
