#Header:
#Name: Diong Chen Xi
#Last Edited Date: 23/3/2022
#Description: Task 4 of Assessment 1 FIT1008
		.globl insertion_sort
		
		.data
space:		.asciiz " "
nl:		.asciiz "\n"

		.text
main:		addi $fp, $sp, 0
		addi $sp, $sp, -8  #two variables: arr, i
		
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
		
		#i = 0
		sw $0, -4($fp)  # -4($fp) = i
		
		#setting the values in arr
		# arr[0] = 6
		lw $t0, -8($fp)
		add $t1, $0, $0  #i = 0
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 6
		sw $t1, 4($t0)
		# arr[1] = -2
		lw $t0, -8($fp)
		addi $t1, $0, 1  #i = 1
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, -2
		sw $t1, 4($t0)
		# arr[2] = 7
		lw $t0, -8($fp)
		addi $t1, $0, 2  #i = 2
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 7
		sw $t1, 4($t0)
		# arr[3] = 4
		lw $t0, -8($fp)
		addi $t1, $0, 3  #i = 3
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, 4
		sw $t1, 4($t0)
		# arr[4] = -10
		lw $t0, -8($fp)
		addi $t1, $0, 4  #i = 4
		sll $t1, $t1, 2  # i*4
		add $t0, $t0, $t1 # &(i*4)-4
		addi $t1, $0, -10
		sw $t1, 4($t0)
		
		#call insertion_sort(the_list)
		addi $sp, $sp, -4
		#arg 1 = the_list
		lw $t0, -8($fp)
		sw $t0, 0($sp)
		#link and goto insertion_sort
		jal insertion_sort
		
		#remove arguments
		addi $sp, $sp, 4
		
mainfor:		lw $t0, -4($fp) #i
		lw $t1, -8($fp) #address of arr
		lw $t1, ($t1) #$t1=  arr.length
		beq $t0, $t1, end #if i = len(arr), break out of the for loop
		
		lw $t0, -8($fp) #address of arr
		lw $t1, -4($fp) #i
		sll $t1, $t1, 2 #i*4
		add $t0, $t0, $t1 #&(i*4)-4
		lw $a0, 4($t0)
		addi $v0, $0, 1
		syscall
		la $a0, space
		addi $v0, $0, 4
		syscall
		
		#i += 1
		lw $t0, -4($fp)
		addi $t0, $t0, 1
		sw $t0, -4($fp)
		
		j mainfor

end:		#remove locals
		addi $sp, $sp, 8
		#print()
		la $a0, nl
		addi $v0, $0, 4
		syscall
		
		#exit
		addi $v0, $0, 10
		syscall
	
		#&the_list is in 8($fp)
		#len(the_list) is in -4($fp)
		#i is in -8($fp)
		#key is in -12($fp)
		#j is in -16($fp)
insertion_sort:	#save $ra and $fp in stack
		addi $sp, $sp, -8
		sw $ra, 4($sp)
		sw $fp, 0($sp)
		
		#Copy $sp to $fp
		addi $fp, $sp, 0
		
		#allocate local variables (4*4=16 bytes)
		addi $sp, $sp, -16
		
		#initialize locals
		#length = len(the_list)
		lw $t0, 8($fp)
		lw $t0, ($t0)
		sw $t0, -4($fp) 
		#i = 1
		addi $t0, $0, 1
		sw $t0, -8($fp) 
		sw $0, -12($fp) #key = 0
		sw $0, -16($fp) #j = 0
		
forloop:		#stop if i = length
		lw $t0, -8($fp) #i
		lw $t1, -4($fp) #length
		beq $t0, $t1, endfor
		
		#key = the_list[i]
		lw $t0, 8($fp)
		lw $t1, -8($fp) #i
		sll $t1, $t1, 2 #i*4
		add $t1, $t0, $t1 #&(i*4)-4
		lw $t0, 4($t1) # $t0 = the_list[i]
		sw $t0, -12($fp) 
		
		#j = i-1
		lw $t0, -8($fp)
		addi $t0, $t0, -1
		sw $t0, -16($fp)
		
whileloop:	#1st condition
		lw $t0, -16($fp)
		slt $t0, $t0, $0
		bne $t0, $0, endwhile #if j<0, break out of the while loop
		
		#2nd condition
		lw $t0, -12($fp) #key
		lw $t1, 8($fp) #address of arr
		lw $t2, -16($fp) #j
		sll $t2, $t2, 2 #j*4
		add $t1, $t1, $t2 #&(j*4)-4
		lw $t1, 4($t1) # $t1 = the_list[j]
		slt $t0, $t0, $t1
		beq $t0, $0, endwhile #if key not < the_list[j], break out of the while loop
		
		#$t0 = the_list[j]
		lw $t0, 8($fp) #address of arr
		lw $t1, -16($fp) #j
		sll $t1, $t1, 2 #j*4
		add $t0, $t0, $t1 #&(j*4)-4
		lw $t0, 4($t0)
				
		#the_list[j+1] = the_list[j]
		lw $t1, 8($fp) #address of arr
		lw $t2, -16($fp) #j
		addi $t2, $t2, 1 #j+1
		sll $t2, $t2, 2 #(j+1)*4
		add $t1, $t1, $t2 #&((j+1)*4)-4
		sw $t0, 4($t1)
				
		#j -= 1
		lw $t0, -16($fp) #j
		addi $t0, $t0, -1
		sw $t0, -16($fp) 
				
		j whileloop
				
				
endwhile:	lw $t0, 8($fp) #address of arr
		lw $t1, -16($fp) #j
		addi $t1, $t1, 1 #j+1
		sll $t1, $t1, 2 #(j+1)*4
		add $t0, $t0, $t1 #&((j+1)*4)-4
		lw $t2, -12($fp) #key
		sw $t2, 4($t0) #the_list[j+1] = key
				
		#i += 1
		lw $t0, -8($fp)
		addi $t0, $t0, 1
		sw $t0, -8($fp)
				
		j forloop
		
		
		
		
endfor:		#remove local var
		addi $sp, $sp, 16
		
		#restore $fp and $ra
		lw $fp, 0($sp) 
		lw $ra, 4($sp)
		addi $sp, $sp, 8
		
		#return to caller
		jr $ra
		
		
