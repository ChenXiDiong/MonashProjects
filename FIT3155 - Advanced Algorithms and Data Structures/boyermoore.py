def bad_char(pat):
    """
    Preprocesses the given pattern to yield a Rk(x) matrix used for bad character shift.

    :Input:
        pat: A str of the pattern.

    :Return:
        A matrix consisting of the Rk(x) values. (1-indexed)

    Note that the Rk(x) values are positions that start from 1, so we need to -1 to get the actual position.
    """
    #Init of Rk(x) matrix
    rk_matrix = [None]*26
    M = len(pat)

    #computing matrix from right to left of pat
    for i in range(M):
        #if the corresponding column of a char is not yet initialised
        index = ord(pat[i]) - 97
        if rk_matrix[index] is None:
            rk_matrix[index] = [0] * M
        #update to the rightmost position (starting from 1)
        for j in range(i+1, M):
            rk_matrix[index][j] = i+1
                

    return rk_matrix

def rev_z_algo(s):
    """
    Performs the reverse z-algorithm on an input string.

    :Input: 
        s: A string to be computed on.
        
    :Return: An array of z-values (i.e. the z-suffix-array).
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

def good_suffix(pat, rev_z_array):
    """
    Preprocesses the given pattern to yield a gs matrix used for good suffix shift.
    
    :Input:
        pat: A str of the pattern.
        rev_z_array: The z-suffix array of pat.

    :Return:
        A list consisting of the gs values (1-indexed).
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

def boyermoore(pat, s):
    #result to be returned
    res = []

    #Preprocessing for bad character rule, good suffix rule and matched prefix
    rk_arr = bad_char(pat)
    z_suffix = rev_z_algo(pat)
    gs_arr = good_suffix(pat, z_suffix)
    len_arr = matched_prefix(z_suffix)

    print(rk_arr)
    print(z_suffix)
    print(gs_arr)
    print(len_arr)

    #length of pat and str so that we don't have to calculate each time
    N = len(s)
    M = len(pat)

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
                k = continue_ptr
                #reset break and continue pointers
                break_ptr = -1
                continue_ptr= - 1

            #all match
            if k == 0 and s[i] == pat[k]:
                matched = True
                break

            #current character of the s and pat match
            elif s[i] == pat[k]:
                k -= 1
                i -= 1

            #current character is a mismatch
            elif s[i] != pat[k]:
                break_ptr = -1
                continue_ptr = -1
                break

        if not matched: #there is a mismatch
            #bad character shift
            rk_index = ord(s[i]) - 97
            rk_row = rk_arr[rk_index]
            if rk_row:
                shift = k+1 - rk_arr[rk_index][k]
            elif rk_row is None:
                shift = 1

            #good suffix shift
            if k < M-1:
                if gs_arr[k+1] > 0:
                    shift = max(shift, M - gs_arr[k+1] - 1)
                    break_ptr = gs_arr[k+1] - 1
                    continue_ptr = break_ptr - (M - k - 1)

                elif gs_arr[k+1] == 0: #matched prefix shift
                    shift = max(shift, M - len_arr[k+1])
                    break_ptr = len_arr[k+1] - 1
                    continue_ptr = 0

        else: # we found an exact match
            res.append(ptr-M+2) #(ptr - M + 1) + 1 since we need to return pos of 1-indexed
            shift = M - len_arr[1]
            break_ptr = len_arr[1] - 1
            continue_ptr = 0
        
        ptr += shift

    return res

    
s = "bbbbbababbbbbabb"
pat = "bbbbb"
print(boyermoore(pat, s))