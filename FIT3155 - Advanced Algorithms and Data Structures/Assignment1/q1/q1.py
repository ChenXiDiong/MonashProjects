"""
Name: Chen Xi Diong
Student ID: 32722656

FIT3155 S1 2023 Assignment 1 - Question 1
"""

import sys

def rev_z_algo(s):
    """
    Performs the reverse z-algorithm on an input string.

    :Input: 
        s: A string to be computed on.

    :Return: An array of z-values (i.e. the z-suffix array).

    :Time Complexity: O(n) where n is the length of the input string. We perform a linear scan through the string and only check for matches or 
    mismatches of each character at most once.

    :Space Complexity: O(n) where n is the length of the input string. We store the z-values of each character in the string in an array.
    """
    #initialize z-array
    n = len(s)
    ret_z_array = [0] * n

    #main loop
    ret_z_array[n-1] = n
    #initialize z-box l and r, l is exclusive
    l = n-1
    r = n-1
    i = n-2
    while i >= 0:
            
        #case 1: i out of z-box : i < l (l exclusive)
        if i < l:
            count = n-1
            ptr = i
            z = 0
            while ptr >= 0 and count >= 0 and s[ptr] == s[count]:
                count -= 1
                ptr -= 1
                z += 1
                    
            ret_z_array[i] = z
            if z > 0:
                l = ptr + 1
                r = i

        else: #i in z-box : i > l

            #k is the mirror of i in the right box, k = l + i + 1 (i inclusive)
            k = (n-1) - (r - i)
                
            #remaining = i - l (i exclusive)
            rem = i - l + 1

            #case 2a : z[k] > rem
            if ret_z_array[k] > rem:
                ret_z_array[i] = rem

            #case 2b : z[k] < rem
            elif ret_z_array[k] < rem:
                ret_z_array[i] = ret_z_array[k]
                
            #case 2c : z[k] == rem
            else:
                count = n - 1 - ret_z_array[k]
                ptr = l - 1
                z = 0
                while ptr >= 0 and count >= 0 and s[ptr] == s[count]:
                    count -= 1
                    ptr -= 1
                    z += 1
                ret_z_array[i] = ret_z_array[k] + z
                if z > 0:
                    l = ptr + 1
                    r = i

        i -= 1    

    
    
    return ret_z_array

def q1_solution(text, pat):
    """
    Computes the z-algorithm on the input text and pattern. By making use of the reverse z-algorithm, we can check if there is a possible transposition 
    error from len(prefix) + len(suffix) = len(pat) - 2.

    See comments_q1.pdf for more details.

    :Input:
        text: The text to be searched on.
        pat: The pattern to be searched for.

    :Return: 
        match_count: The number of matches 
        indices: A single number if there is an exact match, or two numbers if there is a transposition error that corresponds to the index
        of the match and the index of error respectively.

    :Time Complexity: O(n + m) where n is the length of the text and m is the length of the pattern. Preprocessing the text and pattern with the reverse
    z-algorithm takes O(n + m) time. Then we run the z-algorithm on the text and pattern to check for exact matches, which is in O(n + m) time. At
    each step of computing the z-prefix values, we also use an additional step to check for possible transposition errors, then another 2 
    character comparisons to check for whether it is a match or not. This takes O(n + m) time. Thus, the total time complexity is O(2(n + m)) = O(n + m).

    :Space Complexity: O(n + m) where n is the length of the text and m is the length of the pattern. After preprocessing the length of the rev_z_array
    is O(n + m). Then we prepend m additional cells to accomodate for the values of the z-prefix array. Thus, the total space complexity is O(m + n + m),
    which is O(n + 2m) = O(n + m).
    
    """
    N = len(text)
    M = len(pat)

    rev_z_array = rev_z_algo(text + "$" + pat)

    res = ""
    match_count = 0

    s = pat + "$" + text
    arr = [0]* (M+1) #to align z prefix array with z suffix array
    rev_z_array = arr + rev_z_array
    rev_z_array[0] = len(s)

    #initialize z-box l and r, r is exclusive
    l = 0
    r = 0
    i = 1
    while i < N+M+1:
        #case 1: i out of z-box : i >= r (r exclusive)
        if i >= r:
            count = 0
            ptr = i
            while ptr < len(s) and s[ptr] == s[count]:
                count += 1
                ptr += 1
            rev_z_array[i] = count
            if count > 0:
                l = i
                r = ptr
                        

        else: #i in z-box : i < r

            #k is the mirror of i in the left box, k = i - l + 1 (i inclusive)
            k = i - l
                    
            #remaining = r - i (r exclusive)
            rem = r - i 

            #case 2a : z[k] > rem
            if rev_z_array[k] > rem:
                rev_z_array[i] = rem

            #case 2b : z[k] < rem
            elif rev_z_array[k] < rem:
                rev_z_array[i] = rev_z_array[k]
                    
            #case 2c : z[k] == rem
            else:
                count = rev_z_array[k]
                ptr = r
                while ptr < rev_z_array[0] and s[ptr] == s[count]:
                    count += 1
                    ptr += 1
                rev_z_array[i] = count
                if count > 0:
                    l = i
                    r = ptr

        #We only care about the z_values from M+1 to (M+1) + (N-M) + 1 = N+2
        if M < i < N+2:
            z_value = rev_z_array[i]
            if z_value == M: #we found an exact match
                res += str(i-M) + "\n"
                match_count += 1

            #if len(matchedprefix) + len(matched suffix) = M-2, there is a possible transposition error
            elif z_value + rev_z_array[i+M-1] == M-2: 
                #Checking if we flip the characters, they are a match
                if text[i+z_value-M-1] == pat[z_value + 1] and text[i+z_value-M] == pat[z_value]:
                    res += str(i-M) + " " + str(i + rev_z_array[i] - M) + "\n"
                    match_count += 1

        i += 1
    

    return match_count, res

def readInput(txtFileName, patFileName):
    """
    Reading input files and returning the text and pattern for q1.

    :Input:
        txtFileName: The name of the text file.
        patFileName: The name of the pattern file.

    :Return:
        txt: The text to be searched on.
        pat: The pattern to be searched for.

    Source: wk3 tutorial bm_incomplete.py
    """
    # Open and read the files
    txtFile = open(txtFileName, "r")
    txt = txtFile.read()

    patFile = open(patFileName, "r")
    pat = patFile.read()

    # Closing the files
    txtFile.close()
    patFile.close()

    return txt, pat

def writeOutput(nOccurrences, indices):
    """
    Writing the result of q1_solution to a file.

    :Input:
        nOccurrences: The number of matches.
        indices: A single number if there is an exact match, or two numbers if there is a transposition error that corresponds to the index
        of the match and the index of error respectively.

    :Output:
        output_q1.txt: The output file containing the number of matches and the indices of the matches.
    
    Source: wk3 tutorial bm_incomplete.py
    """
    # Open output file with correct name
    outputFile = open("output_q1.txt", "w")

    # Iterate through the occurence list and write results to an output file
    if nOccurrences == 0:
        outputFile.write("0")

    elif nOccurrences > 0:
        outputFile.write(str(nOccurrences) + "\n")
        outputFile.write(indices)
        
    # Close output file
    outputFile.close()

if __name__ == "__main__":
    # Retrieving file names from console
    _, txtFileName, patFileName = sys.argv

    # Reading text and pattern from files
    txt, pat = readInput(txtFileName, patFileName)

    # Processing text and pattern
    nOccurrences, indices = q1_solution(txt, pat)

    # Write output to file
    writeOutput(nOccurrences, indices)