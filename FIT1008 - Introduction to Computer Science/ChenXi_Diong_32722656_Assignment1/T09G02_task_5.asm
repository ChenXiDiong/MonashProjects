#Header:
#Name: Diong Chen Xi
#Last Edited Date: 23/3/2022
#Description: Task 5 of Assessment 1 FIT1008	
		.globl binary_search
		
		.data
nl:		.asciiz "\n"

		.text
main:		addi $fp, $sp, 0
		addi $sp, $sp, -8  #two variables: arr, index
	
		#initialize locals
		addi $v0, $0, 9 #allocate
		addi $t0, $t0, 5
		addi $t1, $0, 4
		mult $t0, $t1
		mflo $t0 #20
		addi $a0, $t0, 4 #24
		syscall
		sw $v0, -8($fp) # -8($fp) = address
	
		#set arr.length to 5
		addi $t0, $0, 5
		sw $t0, ($v0)
		
		#index = 0
		sw $0, -4($fp)  # -4($fp) = index
	
		#setting the values in arr
		# arr[0] = 1
		lw $t0, -8($fp)
		add $t1, $0, $0  #i = 0
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 1
		sw $t1, 4($t0)
		# arr[1] = 5
		lw $t0, -8($fp)
		addi $t1, $0, 1  #i = 1
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 5
		sw $t1, 4($t0)
		# arr[2] = 10
		lw $t0, -8($fp)
		addi $t1, $0, 2  #i = 2
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 10
		sw $t1, 4($t0)
		# arr[3] = 11
		lw $t0, -8($fp)
		addi $t1, $0, 3  #i = 3
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 11
		sw $t1, 4($t0)
		# arr[4] = 12
		lw $t0, -8($fp)
		addi $t1, $0, 4  #i = 4
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 12
		sw $t1, 4($t0)
	
		#call binary_search(the_list, target, low, high)
		addi $sp, $sp, -16
		#arg 1 = the_list
		lw $t0, -8($fp)
		sw $t0, 0($sp)
		#arg 2 = target
		addi $t0, $0, 11
		sw $t0, 4($sp)
		#arg 3 = low
		sw $0, 8($sp)
		#arg 4 = high
		lw $t0, -8($fp)
		lw $t0, ($t0)
		addi $t0, $t0, -1 #len(arr) - 1
		sw $t0, 12($sp)
		#link and goto binary_search
		jal binary_search
		
end:		#remove arguments
		addi $sp, $sp, 16
		
		#printing the result
		add $a0, $v0, $0
		addi $v0, $0, 1
		syscall
		
		#remove local variable
		addi $sp, $sp, 8
		
		#printing newline
		la $a0, nl
		addi $v0, $0, 4
		syscall
		
		#exit
		addi $v0, $0, 10
		syscall
	
		#&the_list is in 8($fp)
		#target is in 12($fp)
		#low is in 16($fp)
		#high is in 20($fp)
		#mid is in -4($fp)
binary_search:	#save $ra and $fp in stack
		addi $sp, $sp, -8
		sw $ra, 4($sp)
		sw $fp, 0($sp)
		
		
		#Copy $sp to $fp
		addi $fp, $sp, 0
		
		#allocate local variables (1*4=4 bytes)
		addi $sp, $sp, -4
		
		#initialize locals
		#mid = 0
		sw $t0, -4($fp)
		
		#if low > high:
		lw $t0, 16($fp) #low
		lw $t1, 20($fp) #high
		slt $t0, $t1, $t0
		beq $t0, $0, else #if low <= high, goto else
		
		#return -1
		#$v0 = -1
		addi $v0, $0, -1  
		
		#remove local var
		addi $sp, $sp, 4
		
		#restore $fp and $ra
		lw $fp, 0($sp) 
		lw $ra, 4($sp)
		addi $sp, $sp, 8
		
		#return to caller
		jr $ra
		
else:		#mid = (high + low) // 2
		lw $t0, 20($fp)
		lw $t1, 16($fp)
		add $t0, $t0, $t1
		addi $t1, $0, 2
		div $t0, $t1 #LO : quotient
		mflo $t0
		sw $t0, -4($fp)
		
		#if the_list[mid] == target:
		lw $t0, -4($fp) #mid
		sll $t0, $t0, 2 
		lw $t1, 8($fp) #the_list
		add $t0, $t0, $t1 #&?mid*4?-4
		lw $t0, 4($t0)
		lw $t1, 12($fp) #target
		bne $t0, $t1, nestelif #if the_list[mid] != target, goto nestelif
		#return mid
		lw $v0, -4($fp)
		#remove local var
		addi $sp, $sp, 4
		
		#restore $fp and $ra
		lw $fp, 0($sp) 
		lw $ra, 4($sp)
		addi $sp, $sp, 8
		
		#return to caller
		jr $ra
		
		
nestelif:	#if the_list[mid] > target:
		lw $t0, -4($fp) #mid
		sll $t0, $t0, 2 #mid*4
		lw $t1, 8($fp) #the_list
		add $t0, $t0, $t1 #&(mid*4)-4
		lw $t0, 4($t0)  #the_list[mid]
		lw $t1, 12($fp) #target
		slt $t0, $t1, $t0 
		beq $t0, $0, nestelse   #if the_list[mid] <= target, goto nestelse
		
		#call binary_search(the_list, target, low, high)
		addi $sp, $sp, -16
		#arg 1 = the_list
		lw $t0, 8($fp)
		sw $t0, 0($sp)
		#arg 2 = target
		lw $t0, 12($fp)
		sw $t0, 4($sp)
		#arg 3 = low
		lw $t0, 16($fp)
		sw $t0, 8($sp)
		#arg 4 = mid-1
		lw $t0,-4($fp)
		addi $t0, $t0, -1
		sw $t0, 12($sp)
		#link and goto binary_search
		jal binary_search
		
		#remove arguments
		addi $sp, $sp, 16
		
		#storing the result
		sw $v0, -4($fp)
		
		#restore $fp and $ra
		lw $fp, 0($sp) 
		lw $ra, 4($sp)
		addi $sp, $sp, 8
		
		#return the result
		j end
		
nestelse:	#else:
		#call binary_search(the_list, target, low, high)
		addi $sp, $sp, -16
		#arg 1 = the_list
		lw $t0, 8($fp)
		sw $t0, 0($sp)
		#arg 2 = target
		lw $t0, 12($fp)
		sw $t0, 4($sp)
		#arg 3 = mid+1
		lw $t0, -4($fp)
		addi $t0, $t0, 1
		sw $t0, 8($sp)
		#arg 4 = high
		lw $t0, 20($fp)
		sw $t0, 12($sp)
		#link and goto binary_search
		jal binary_search
		
		#remove arguments
		addi $sp, $sp, 16
		
		#storing the result
		sw $v0, -4($fp)
		
		#restore $fp and $ra
		lw $fp, 0($sp) 
		lw $ra, 4($sp)
		addi $sp, $sp, 8
		
		#return the result
		j end
		
		
		
		
		
