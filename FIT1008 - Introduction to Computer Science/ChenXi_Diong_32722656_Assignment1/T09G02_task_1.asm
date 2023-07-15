#Header:
#Name: Diong Chen Xi
#Last Edited Date: 25/3/2022
#Description: Task 1 of Assessment 1 FIT1008
		.data
number:		.word 0
first_divisor: 	.word 0
second_divisor: 	.word 0
divisors: 	.word 0
s1: 		.asciiz "Enter the number: "
s2: 		.asciiz "Enter the first divisor: "
s3: 		.asciiz "Enter the second divisor: "
output: 		.asciiz "\nDivisors: "
nl: 		.asciiz "\n"

		.text
		#number = int(input("Enter the number: "))
		#print the prompt for number
main:		addi $v0, $0, 4
		la $a0, s1
		syscall 
		#store the input into number
		addi $v0, $0, 5
		syscall
		sw $v0, number
		
		#first_divisor = int(input("Enter the first divisor: "))
		#print the prompt for first divisor
		addi $v0, $0, 4
		la $a0, s2
		syscall
		#store the input into first_divisor
		addi $v0, $0, 5
		syscall 
		sw $v0, first_divisor 
		
		#second_divisor = int(input("Enter the second divisor: "))
		#print the prompt for second divisor
		addi $v0, $0, 4
		la $a0, s3
		syscall
		#store the input into second_divisor
		addi $v0, $0, 5
		syscall
		sw $v0, second_divisor

		#if number % first_divisor == 0
line1:		lw $t0, number
		lw $t1, first_divisor
		div $t0, $t1 #lo:quotient hi:remainder
		mfhi $t0
		bne $t0, $0, line2 #if number % first divisor != 0, go to elif
		#if number % second_divisor == 0
		lw $t0, number
		lw $t1, second_divisor
		div $t0, $t1 #lo:quotient hi:remainder
		mfhi $t0
		bne $t0, $0, line2 #if number % second divisor != 0, go to elif
		#if both first and second condition passes, store 2 into divisors
		addi $t0, $0, 2
		sw $t0, divisors
		j endif

		#if number % first_divisor == 0
line2:		lw $t0, number
		lw $t1, first_divisor
		div $t0, $t1
		mfhi $t0
		beq $t0, $0, onedivisor #if number % first divisor == 0, go to onedivisor
		#if number % second_divisor == 0
		lw $t0, number
		lw $t1, second_divisor
		div $t0, $t1
		mfhi $t0
		beq $t0, $0, onedivisor #if number % second divisor == 0, go to onedivisor
		#if both first and second condition doesn't pass
		addi $t0, $0, 0
		sw $t0, divisors
		j endif
	
		#divisors = 1
onedivisor:	addi $t0, $0, 1
		sw $t0, divisors
		j endif

		#print("\nDivisors: " + str(divisors))
endif:		la $a0, output
		addi $v0, $0, 4
		syscall
		lw $a0, divisors
		addi $v0, $0, 1
		syscall

		#print newline
		la $a0, nl
		addi $v0, $0, 4
		syscall
		
		#exit
exit:		addi $v0, $0, 10
		syscall


