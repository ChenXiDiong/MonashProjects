#Header:
#Name: Diong Chen Xi
#Last Edited Date: 14/3/2022
#Description: Task 2 of Assessment 1 FIT1008
		.data
size:		.word 0
the_list: 	.word 0
n:		.word 0
count:		.word 0
i:		.word 0
arr_len:		.asciiz "Enter array length: "
n_inp:		.asciiz "Enter n: "
value_inp:	.asciiz "Enter the value: "
output:		.asciiz "\nThe number of multiples (excluding itself) = "
nl:		.asciiz "\n"

		.text
		#obtaining the array length via input and storing it
		la $a0, arr_len
		addi $v0, $0, 4
		syscall
		addi $v0, $0, 5
		syscall
		sw $v0, size
		#allocating space for the_list in Heap
		addi $v0, $0, 9 #allocate
		lw $t0, size
		addi $t1, $0, 4
		mult $t0, $t1
		mflo $t0 #size*4
		addi $a0, $t0, 4 #(size*4) + 4 
		syscall
		sw $v0, the_list #the_list = address
		#set the_list's length to size
		lw $t0, size
		sw $t0, ($v0)
		#obtaining n via input and storing it
		la $a0, n_inp
		addi $v0, $0, 4
		syscall
		addi $v0, $0, 5
		syscall
		sw $v0, n
		
		#init for i
		sw $0, i
		
		#the for loop
loop:		lw $t0, i
		lw $t1, size
		beq $t0, $t1, end #if i=size, break out of the loop
		#if i<size
		addi $v0, $0, 4
		la $a0, value_inp 
		syscall
		addi $v0, $0, 5
		syscall
		#store in input value
		lw $t0, the_list
		lw $t1, i
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		sw $v0, 4($t0) # store the value of the input number into the_list[i]
		#if condition 1
		lw $t0, the_list
		lw $t1, i
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		lw $t0, 4($t0) #load the value of the_list[i] into $t0
		lw $t1, n
		div $t0, $t1
		mfhi $t0
		bne $t0, $0, continue
		#if condition 2
		lw $t0, the_list
		lw $t1, i
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		lw $t0, 4($t0) #load the value of the_list[i] into $t0
		lw $t1, n
		beq $t0, $t1, continue
		#if condition 1 and condition 2 are both fulfilled
		lw $t0, count
		addi $t0, $t0, 1
		sw $t0, count
		
		#i = i+1
continue:	lw $t0, i
		addi $t0, $t0, 1
		sw $t0, i
		#jump back to the loop
		j loop
		
end:		la $a0, output
		addi $v0, $0, 4
		syscall
		lw $a0, count
		addi $v0, $0, 1
		syscall
		la $a0, nl
		addi $v0, $0, 4
		syscall
		#exit 
		addi $v0, $0, 10
		syscall
		
			
