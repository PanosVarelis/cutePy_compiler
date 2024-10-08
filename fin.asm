	.data
str_nl: .asciz "\n"
	.text 
j main
max3: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 28(T_1)
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(x)
	lw $t0, -16($sp)
	lw $t2, 0(y)
	bgt $t1, $t2, 7
	j 9
L7: 
	lw $t0, -12($sp)
	lw $t1, 0(x)
	lw $t0, -20($sp)
	lw $t2, 0(z)
	bgt $t1, $t2, 9
	j 11
L9:
	lw $t0, -24($sp)
	lw $t1, 0(m)
	lw $t2, 12(x)
	sw $t1, 0($t0)
	j 18
L11:
	lw $t0, -16($sp)
	lw $t1, 0(y)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	bgt $t1, $t2, 13
	j 15
L13: 
	lw $t0, -16($sp)
	lw $t1, 0(y)
	lw $t0, -20($sp)
	lw $t2, 0(z)
	bgt $t1, $t2, 15
	j 17
L15:
	lw $t0, -24($sp)
	lw $t1, 0(m)
	lw $t2, 16(y)
	sw $t1, 0($t0)
	j 18
L17:
	lw $t0, -24($sp)
	lw $t1, 0(m)
	lw $t2, 20(z)
	sw $t1, 0($t0)
L18:
	lw $ra, 0($sp)
	jr $ra
fib: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 16(T_2)
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(x)
	li $t2, 0
	blt $t1, $t2, 25
	j 27
L25: 
	j 41
L27:
	lw $t0, -12($sp)
	lw $t1, 0(x)
	li $t2, 0
	beq $t1, $t2, 31
	j 31
	lw $t0, -12($sp)
	lw $t1, 0(x)
	li $t2, 1
	beq $t1, $t2, 31
	j 33
L31:
	j 41
L33:
	addi $s7, $sp, 32
	jal fib
	lw $t0, -12($sp)
	lw $t1, 0(x)
	li $t2, 1
	sub $t3, $t1, $t2
	lw $t0, -20($sp)
	lw $t1, 0(T_3)
	addi $s7, $sp, 32
	jal fib
	lw $t0, -12($sp)
	lw $t1, 0(x)
	li $t2, 2
	sub $t3, $t1, $t2
	lw $t0, -24($sp)
	lw $t1, 0(T_4)
	lw $t1, 0(fib)
	lw $t2, 0(fib)
	add $t3, $t1, $t2
L41:
	lw $ra, 0($sp)
	jr $ra
divides: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -28($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -28($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 20(T_6)
	sw $t1, 0($t0)
	lw $t0, -16($sp)
	lw $t1, 0(y)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	div $t3, $t1, $t2
	lw $t0, -24($sp)
	lw $t1, 0(T_7)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	mul $t3, $t1, $t2
	lw $t0, -16($sp)
	lw $t1, 0(y)
	lw $t0, -28($sp)
	lw $t2, 0(T_8)
	beq $t1, $t2, 50
	j 52
L50: 
	j 53
L52:
L53:
	lw $ra, 0($sp)
	jr $ra
isPrime: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 20(T_9)
	sw $t1, 0($t0)
	lw $t0, -16($sp)
	lw $t1, 0(i)
	li $t2, 2
	sw $t1, 0($t0)
	lw $t0, -16($sp)
	lw $t1, 0(i)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	blt $t1, $t2, 59
	j 68
L59: 
	addi $sp, $sp, 20
	jal divides
	lw $t0, -16($sp)
	lw $t1, 0(i)
	lw $t0, -12($sp)
	lw $t1, 0(x)
	lw $t1, 0(divides)
	li $t2, 1
	beq $t1, $t2, 64
	j 66
L64: 
	lw $t0, -16($sp)
	lw $t1, 0(i)
	li $t2, 1
	add $t3, $t1, $t2
L66:
	lw $t0, -16($sp)
	lw $t1, 0(i)
	lw $t2, 24(T_10)
	sw $t1, 0($t0)
	j 57
L68:
	lw $ra, 0($sp)
	jr $ra
sqr: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -28($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -28($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 16(T_11)
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(x)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	mul $t3, $t1, $t2
	lw $ra, 0($sp)
	jr $ra
quad: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 20(T_13)
	sw $t1, 0($t0)
	addi $sp, $sp, 20
	jal sqr
	lw $t0, -12($sp)
	lw $t1, 0(x)
	addi $sp, $sp, 20
	jal sqr
	lw $t0, -12($sp)
	lw $t1, 0(x)
	lw $t1, 0(sqr)
	lw $t2, 0(sqr)
	mul $t3, $t1, $t2
	lw $t0, -16($sp)
	lw $t1, 0(y)
	lw $t2, 24(T_14)
	sw $t1, 0($t0)
	lw $ra, 0($sp)
	jr $ra
leap: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	lw $t2, 16(T_15)
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(year)
	li $t2, 4
	rem $t3, $t1, $t2
	lw $t0, -20($sp)
	lw $t1, 0(T_16)
	li $t2, 0
	beq $t1, $t2, 93
	j 96
L93: 
	lw $t0, -12($sp)
	lw $t1, 0(year)
	li $t2, 100
	rem $t3, $t1, $t2
	lw $t0, -24($sp)
	lw $t1, 0(T_17)
	li $t2, 0
	bne $t1, $t2, 96
	j 99
L96:
	lw $t0, -12($sp)
	lw $t1, 0(year)
	li $t2, 400
	rem $t3, $t1, $t2
	lw $t0, -28($sp)
	lw $t1, 0(T_18)
	li $t2, 0
	beq $t1, $t2, 99
	j 101
L99:
	j 102
L101:
L102:
	lw $ra, 0($sp)
	jr $ra
table: 
	sw $ra, 0($sp)
	lw $t0, -16($sp)
	lw $t1, 0(i)
	li $t2, 1
	sw $t1, 0($t0)
	lw $t0, -20($sp)
	lw $t1, 0(j)
	li $t2, 1
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(x)
	li $t2, 2
	mul $t3, $t1, $t2
	lw $t0, multiplier
	sw $t0, -4($gp)
	lw $t1, 0(multiplier)
	lw $t2, 24(T_19)
	sw $t1, 0($t0)
	lw $t0, -16($sp)
	lw $t1, 0(i)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	ble $t1, $t2, 110
	j 119
L110: 
	lw $t0, -20($sp)
	lw $t1, 0(j)
	lw $t0, -12($sp)
	lw $t2, 0(x)
	ble $t1, $t2, 112
	j 116
L112: 
	mv $a0,$t0
	li $a7, 1
	ecall
	lw $t0, -20($sp)
	lw $t1, 0(j)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, -20($sp)
	lw $t1, 0(j)
	lw $t2, 28(T_20)
	sw $t1, 0($t0)
	j 110
L116:
	lw $t0, -16($sp)
	lw $t1, 0(i)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, -16($sp)
	lw $t1, 0(i)
	lw $t2, 32(T_21)
	sw $t1, 0($t0)
	j 108
L119:
	lw $ra, 0($sp)
	jr $ra
decisions: 
	sw $ra, 0($sp)
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 1
	ble $t1, $t2, 123
	j 125
L123: 
	j 152
L125:
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 2
	bge $t1, $t2, 127
	j 129
L127: 
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 10
	ble $t1, $t2, 129
	j 135
L129:
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 5
	blt $t1, $t2, 131
	j 133
L131: 
	mv $a0,$t0
	li $a7, 1
	ecall
	j 134
L133:
	mv $a0,$t0
	li $a7, 1
	ecall
L134:
	j 152
L135:
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 20
	ble $t1, $t2, 137
	j 147
L137: 
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 13
	blt $t1, $t2, 139
	j 141
L139: 
	mv $a0,$t0
	li $a7, 1
	ecall
	j 146
L141:
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 18
	ble $t1, $t2, 143
	j 145
L143: 
	mv $a0,$t0
	li $a7, 1
	ecall
	j 146
L145:
	mv $a0,$t0
	li $a7, 1
	ecall
L146:
	j 152
L147:
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 30
	ble $t1, $t2, 149
	j 151
L149: 
	mv $a0,$t0
	li $a7, 1
	ecall
	j 152
L151:
	mv $a0,$t0
	li $a7, 1
	ecall
L152:
	addi $s7, $sp, 20
	jal decisions
	lw $t0, -12($sp)
	lw $t1, 0(flag)
	li $t2, 2
	div $t3, $t1, $t2
	lw $t0, -16($sp)
	lw $t1, 0(T_22)
	lw $ra, 0($sp)
	jr $ra
main: 
	sw $ra, 0($sp)
	lw $t0, counterFunctionCalls
	sw $t0, -8($gp)
	lw $t1, 0(counterFunctionCalls)
	li $t2, 0
	sw $t1, 0($t0)
	lw $t0, multiplier
	sw $t0, -4($gp)
	lw $t1, 0(multiplier)
	li $t2, 2
	sw $t1, 0($t0)
	li $a7, 5
	ecall
	mv $a0,$t0
	li $a7, 1
	ecall
	lw $t0, -12($sp)
	lw $t1, 0(i)
	li $t2, 1600
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(i)
	li $t2, 2000
	ble $t1, $t2, 165
	j 171
L165: 
	addi $sp, $sp, 20
	jal leap
	lw $t0, -12($sp)
	lw $t1, 0(i)
	mv $a0,$t0
	li $a7, 1
	ecall
	lw $t0, -12($sp)
	lw $t1, 0(i)
	li $t2, 400
	add $t3, $t1, $t2
	lw $t0, -12($sp)
	lw $t1, 0(i)
	lw $t2, 20(T_24)
	sw $t1, 0($t0)
	j 163
L171:
	addi $sp, $sp, 20
	jal leap
	li $t1, 2023
	mv $a0,$t0
	li $a7, 1
	ecall
	addi $sp, $sp, 20
	jal leap
	li $t1, 2024
	mv $a0,$t0
	li $a7, 1
	ecall
	addi $sp, $sp, 20
	jal quad
	li $t1, 3
	mv $a0,$t0
	li $a7, 1
	ecall
	addi $sp, $sp, 20
	jal fib
	li $t1, 5
	mv $a0,$t0
	li $a7, 1
	ecall
	addi $sp, $sp, 20
	jal leap
	addi $sp, $sp, 20
	jal decisions
	li $t1, 45
	lw $t1, 0(decisions)
	mv $a0,$t0
	li $a7, 1
	ecall
	lw $t0, -12($sp)
	lw $t1, 0(i)
	li $t2, 1
	sw $t1, 0($t0)
	lw $t0, -12($sp)
	lw $t1, 0(i)
	li $t2, 12
	ble $t1, $t2, 191
	j 197
L191: 
	addi $sp, $sp, 20
	jal isPrime
	lw $t0, -12($sp)
	lw $t1, 0(i)
	mv $a0,$t0
	li $a7, 1
	ecall
	lw $t0, -12($sp)
	lw $t1, 0(i)
	li $t2, 1
	add $t3, $t1, $t2
	lw $t0, -12($sp)
	lw $t1, 0(i)
	lw $t2, 24(T_25)
	sw $t1, 0($t0)
	j 189
L197:
	mv $a0,$t0
	li $a7, 1
	ecall
	lw $ra, 0($sp)
	jr $ra
