#Header:
#Name: Diong Chen Xi
#Last Edited Date: 25/3/2022
#Description: Task 3 of Assessment 1 FIT1008
.globl get_multiples

.data
__author__:	.asciiz "Saksham Nagpal"
__date__:	.asciiz "01.08.2021"
res_prompt1:	.asciiz "The number of multiples of "
res_prompt2:	.asciiz " is: "
nl:		.asciiz "\n"

.text
main:		addi $fp, $sp, 0 
		addi $sp, $sp, -8 #two variables: my_list, n
		
		#initialize locals
		addi $v0, $0, 9 #allocate
		addi $t0, $t0, 3
		addi $t0, $t0, 1
		sll $a0, $t0, 2 #16 bytes  
		syscall
		sw $v0, -8($fp) # -8($fp) = address
		
		#set my_list's length to 3
		addi $t0, $0, 3 
		sw $t0, ($v0)
		
		#n = 3
		addi $t0, $0, 3
		sw $t0, -4($fp) # -4($fp) = n
		
		#set the values in my_list
		# store 2 into my_list[0]
		lw $t0, -8($fp)
		add $t1, $0, $0 #i = 0
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		addi $t1, $0, 2 
		sw $t1, 4($t0) 
		# store 4 into my_list[1]
		lw $t0, -8($fp)
		addi $t1, $0, 1 #i = 1
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		addi $t1, $0, 4
		sw $t1, 8($t0) 
		# store 6 into my_list[2]
		lw $t0, -8($fp)
		addi $t1, $0, 2 #i = 2
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		addi $t1, $0, 6
		sw $t1, 12($t0) 
		
		#printing the result
		la $a0, res_prompt1
		addi $v0, $0, 4
		syscall
		lw $a0, -4($fp)
		addi $v0, $0, 1
		syscall
		la $a0, res_prompt2
		addi $v0, $0, 4
		syscall
		
		#call get_multiples(the_list, n)
		addi $sp, $sp, -8
		#arg 1 = the_list
		lw $t0, -8($fp)
		sw $t0, 0($sp)
		#arg 2 = n
		lw $t0, -4($fp)
		sw $t0, 4($sp)
		#link and goto get_multiples 
		jal get_multiples
		#remove arguments
		addi $sp, $sp, 8
		#store return value
		add $a0, $v0, $0
		addi $v0, $0, 1
		syscall
		
		#remove locals, then exit
		addi $sp, $sp, 8
		addi $v0, $0, 10
		syscall
		
		#n is in 12($fp)
		#&arr is in 8($fp)
		#count is in -4($fp)
		#i is in -8($fp)
get_multiples: 	#save $ra and $fp in stack
		addi $sp, $sp, -8
		sw $ra, 4($sp)
		sw $fp, 0($sp)
		
		#Copy $sp to $fp
		addi $fp, $sp, 0
		
		#allocate local variables (2*4=8 bytes)
		addi $sp, $sp, -8
		
		#initialize locals
		sw $0, -4($fp) #count = 0
		sw $0, -8($fp) #i = 0
		
loop:		#stop if i = my_list.length
		lw $t0, -8($fp) #loading i
		lw $t1, 8($fp) #retrieving the address of my_list
		lw $t1, ($t1) #storing the length of my_list into $t1
		beq $t0, $t1, endloop
		
		#if condition 1
		lw $t0, 8($fp) #address of the_list
		lw $t1, -8($fp) #i
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		lw $t0, 4($t0) #load the value of the_list[i] into $t0
		lw $t1, 12($fp) #load the value of n
		div $t0, $t1 #lo: quotient hi: remainder
		mfhi $t0
		bne $t0, $0, continue
		
		#if condition 2
		lw $t0, 8($fp) #address of the_list
		lw $t1, -8($fp) #i
		sll $t1, $t1, 2 # i*4
		add $t0, $t0, $t1 # &(the_list[i])-4
		lw $t0, 4($t0) #load the value of the_list[i] into $t0
		lw $t1, 12($fp) #load the value of n
		beq $t0, $t1, continue
		
		#if condition 1 and condition 2 are both fulfilled
		lw $t0, -4($fp)
		addi $t0, $t0, 1
		sw $t0, -4($fp) #count += 1

continue:	#i += 1
		lw $t0, -8($fp)
		addi $t0, $t0, 1
		sw $t0, -8($fp)
		
		#jump back to the loop
		j loop
		
endloop:		lw $v0, -4($fp) #$v0 = count

		#remove local var
		addi $sp, $sp, 8
		
		#restore $fp and $ra
		lw $fp, 0($sp) 
		lw $ra, 4($sp)
		addi $sp, $sp, 8
		
		#return to caller
		jr $ra
		
			
		
