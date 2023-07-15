"""
Name: Chen Xi Diong
Student ID: 32722656

FIT3155 S1 2023 Assignment 1 - Question 2
"""

import sys

def bad_char(pat):
    """
    Preprocesses the given pattern to yield a Rk(x) matrix used for bad character shift.

    :Input:
        pat: A str of the pattern.

    :Return:
        rk_matrix: A matrix consisting of the Rk(x) values. (1-indexed)
        wc_idx: The index of the wildcard character in the pattern. If there is no wildcard, then this is None.


    :Time Complexity: O(kN) where N is the length of the pattern, and k is the number of unique characters in the pattern. We only initialize a column if a unique character
    is found in the pattern, and each column is of size N.

    :Space Complexity: O(kN) where N is the length of the pattern, and k is the number of unique characters in the pattern. We only allocate space for k unique characters
    and for each character we need to store N values.

    Note that the Rk(x) values are positions that start from 1, so we need to -1 to get the actual position.
    """
    #Init of Rk(x) matrix
    rk_matrix = [None]*26
    M = len(pat)
    wc_idx = None

    #computing matrix from right to left of pat
    for i in range(M):
        ascii = ord(pat[i])
        
        if ascii != 46: #the current character is not a wildcard
            #if the corresponding column of a char is not yet initialised
            index = ord(pat[i]) - 97
            if rk_matrix[index] is None:
                rk_matrix[index] = [0] * M
            #update to the rightmost position (starting from 1)
            for j in range(i+1, M):
                rk_matrix[index][j] = i+1

        elif ascii == 46:
            wc_idx = i
                

    return rk_matrix, wc_idx
                
def rev_z_algo(s):
    """
    Performs the reverse z-algorithm on an input string.

    :Input: 
        s: A string to be computed on.
        
    :Return: An array of z-values (i.e. the z-suffix-array).

    :Time Complexity: O(N) where N is the length of the string. We only perform comparisons of each character at most once.

    :Space Complexity: O(N) where N is the length of the string. We only allocate space for N z-values.
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
            while ptr >= 0 and count >= 0 and (s[ptr] == s[count] or s[ptr] == '.' or s[count] == '.'):
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
                while ptr >= 0 and count >= 0 and (s[ptr] == s[count] or s[ptr] == '.' or s[count] == '.'):
                    count -= 1
                    ptr -= 1
                    z += 1
                ret_z_array[i] = ret_z_array[k] + z
                if z > 0:
                    l = ptr + 1
                    r = i

        i -= 1    
    
    return ret_z_array

def good_suffix(pat, rev_z_array):
    """
    Preprocesses the given pattern to yield a gs matrix used for good suffix shift.
    
    :Input:
        pat: A str of the pattern.
        rev_z_array: The z-suffix array of pat.

    :Return: A list consisting of the gs values (1-indexed).

    :Time Complexity: O(N) where N is the length of the pattern. We only iterate through the pattern once and perform constant time operations.

    :Space Complexity: O(N) where N is the length of the pattern. We only allocate space for N gs values.
    """
    M = len(pat)
    gs_arr = [0] * (M+1) #the last cell is to hold the dummy value

    for i in range(M-1):
        j = M - rev_z_array[i]
        gs_arr[j] = i + 1

    return gs_arr

def matched_prefix(rev_z_array):
    """
    A version of matched prefix that makes use of the z-suffix array instead of the z-prefix array.
    Matched_prefix is finding the match of a prefix with the longest proper suffix, so in reverse we are matching the known suffix with a prefix.

    :Input:
        rev_z_arry: The z-values of a z-suffix array.

    :Return: The length array containing all the matchedprefix values.

    :Time Complexity: O(N) where N is the length of the pattern. We only iterate through the pattern once and perform constant time operations.

    :Space Complexity: O(N) where N is the length of the pattern. We only allocate space for N matched prefix values.
    """
    M = len(rev_z_array)
    #Init of length array
    len_arr = [0]*(M+1)
    
    for i in range(M):
        j = M-1 - i 
        z_value = rev_z_array[i]

        if i - z_value == -1  and rev_z_array[i] > len_arr[j+1]:
            len_arr[j] = z_value
        else:
            len_arr[j] = len_arr[j+1]

    return len_arr

def q2_solution(txt, pat):
    """
    The Boyer-Moore string pattern matching algorithm with at most one wildcard character.

    :Input:
        pat: A str of the pattern.
        s: A str of the string to be searched.

    :Return: A list of all the indices of the pattern in the text.

    :Time Complexity: O(N + M) where N is the length of the text and M is the length of the pattern. Pre-processing the bad character, 
    z-suffix, good suffix and matched prefix arrays takes O(M) time each for a total of O(4M) = O(M) time, whereas for the Boyer-Moore
    algorithm, we only need to perform comparisons of each character in the text at most once in the worst case, which accounts for O(N) time.
    Slight modifications are made to the original algorithm to account for the wildcard character. More details are specified in the pdf.

    :Space Complexity: O(N + M) where N is the length of the text, M is the length of the pattern and k is the number of unique characters 
    present in the pattern. The total space needed is O(N + 3M + kM), which is O(N + M).
    Breakdown for space needed:
    O(kM) for the bad character array. (k<=26 since we only consider lowercase letters)
    O(M) for the good suffix array.
    O(M) for the matched prefix array.
    O(M) for the z-suffix array.
    O(N) for the result list. We have to allocate space for at most N indices.    
    """
    #result to be returned
    res = []

    #length of pat and str so that we don't have to calculate each time
    N = len(txt)
    M = len(pat)

    #Preprocessing for bad character rule, good suffix rule and matched prefix
    rk_arr, wc_idx = bad_char(pat)
    z_suffix = rev_z_algo(pat)
    gs_arr = good_suffix(pat, z_suffix)
    len_arr = matched_prefix(z_suffix)

    #Pointers
    ptr = M-1 #pointer of current matching of s
    break_ptr = -1 #the break pointer
    continue_ptr = -1 #the continue pointer

    #Main Loop
    while ptr < N:
        #pointers for character  k for pat, i for str
        k = M - 1
        i = ptr
        matched = False

        while k >= 0:
            if k == break_ptr: #break pointer met
                if wc_idx is not None and continue_ptr < wc_idx < break_ptr:
                    #calculate the distance between the wildcard and the end of the pattern
                    dist = M - 1 - wc_idx
                    if txt[i - dist] == pat[k-dist] or pat[k-dist] == '.':
                        k = continue_ptr
                        i -= k
                    else:
                        k -= dist
                        break  
                #reset break and continue pointers
                break_ptr = -1
                continue_ptr= - 1

            #all match
            if k == 0 and (txt[i] == pat[k] or pat[k] == '.'):
                matched = True
                break

            #current character of the s and pat match
            elif txt[i] == pat[k] or pat[k] == '.':
                k -= 1
                i -= 1

            #current character is a mismatch
            elif txt[i] != pat[k]:
                break_ptr = -1
                continue_ptr = -1
                break

        if not matched: #there is a mismatch
            #bad character 
            rk_index = ord(txt[i]) - 97
            rk_row = rk_arr[rk_index]
            shift = 1

            if rk_row:
                shift = k+1 - rk_row[k]

            elif rk_row is None: #there is no occurrence of bc in pat
                #if wildcard before , we align bc with wildcard
                #otherwise, we can only do a naive shift
                if k > wc_idx:
                    shift = k - wc_idx

            #good suffix shift
            if k < M-1:
                if gs_arr[k+1] > 0:
                    if M - gs_arr[k+1] > shift:
                        shift = M - gs_arr[k+1]
                        break_ptr = gs_arr[k+1] - 1
                        #continue_ptr = break_ptr - num_matches + 1 (break pointer inclusive)
                        #num_matches = len(pat) - (k+1) = M - k - 1
                        continue_ptr = break_ptr - (M - k - 1) + 1 

                elif gs_arr[k+1] == 0: #matched prefix shift
                    if M - len_arr[k+1] > shift:
                        shift = M - len_arr[k+1]
                        break_ptr = len_arr[k+1] - 1
                        continue_ptr = 0

            if wc_idx is not None and k > wc_idx:
                shift = min(shift, k - wc_idx)
                break_ptr = -1
                continue_ptr = -1 

        else: # we found an exact match
            res.append(ptr-M+2) #(ptr - M + 1) + 1 since we need to return pos of 1-indexed
            shift = M - len_arr[1]
            break_ptr = len_arr[1] - 1
            continue_ptr = 0
        
        ptr += shift

    return res

    
def readInput(txtFileName, patFileName):
    """
    Reading input files and returning the text and pattern for q2.

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

def writeOutput(indices):
    """
    Writing the result of q2_solution to a file.

    :Input:
        indices: A list of indices of the matches.

    :Output:
        output_q1.txt: The output file containing the indices of the matches, printed out on different lines.
    
    Source: wk3 tutorial bm_incomplete.py
    """
    # Open output file with correct name
    outputFile = open("output_q2.txt", "w")

    # Iterate through the indices list and write results to an output file
    for index in indices:
        outputFile.write(str(index) + "\n")
         
    # Close output file
    outputFile.close()

if __name__ == "__main__":
    # Retrieving file names from console
    _, txtFileName, patFileName = sys.argv

    # Reading text and pattern from files
    txt, pat = readInput(txtFileName, patFileName)

    # Processing text and pattern
    indices = q2_solution(txt, pat)

    # Write output to file
    writeOutput(indices)