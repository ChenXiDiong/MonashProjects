def z_algo(s, reverse=False):
    """
    Performs the z-algorithm on an input string, either reverse or non reverse.

    :Input: 
        s: A string to be computed on.
        reverse: An indication to perform z-algorithm or reverse z-algorithm.

    :Return: An array of z-values (i.e. the z-array).
    """
    #initialize z-array
    n = len(s)
    ret_z_array = [0] * n

    #main loop
    if reverse:
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

    else:
        ret_z_array[0] = len(s)
        #initialize z-box l and r, r is exclusive
        l = 0
        r = 0
        i = 1
        while i < len(s):
        
            #case 1: i out of z-box : i >= r (r exclusive)
            if i >= r:
                count = 0
                ptr = i
                while ptr < ret_z_array[0] and s[ptr] == s[count]:
                    count += 1
                    ptr += 1
                ret_z_array[i] = count
                if count > 0:
                    l = i
                    r = ptr
                    

            else: #i in z-box : i < r

                #k is the mirror of i in the left box, k = i - l + 1 (i inclusive)
                k = i - l
                
                #remaining = r - i (r exclusive)
                rem = r - i 

                #case 2a : z[k] > rem
                if ret_z_array[k] > rem:
                    ret_z_array[i] = rem

                #case 2b : z[k] < rem
                elif ret_z_array[k] < rem:
                    ret_z_array[i] = ret_z_array[k]
                
                #case 2c : z[k] == rem
                else:
                    count = ret_z_array[k]
                    ptr = r
                    while ptr < ret_z_array[0] and s[ptr] == s[count]:
                        count += 1
                        ptr += 1
                    ret_z_array[i] = count
                    if count > 0:
                        l = i
                        r = ptr 

            i += 1
    
    return ret_z_array


# text = "babbababaabbaba"
# pat = "abba"

# N = len(text)
# M = len(pat)

# z_array = z_algo(pat + "$" + text)
# rev_z_array = z_algo(text + "$" + pat , reverse=True)

# res = ""
# count = 0

# #we want to compare z-values of the z_array from M+1 to (M+1) + (N-M) + 1
# for i in range(M+1, N+2):
#     if z_array[i] == M: #we found an exact match
#         res += str(i-M) + "\n"
#         count += 1

#     #if len(matchedprefix) + len(matched suffix) = M-2, there is a possible transposition error
#     #rev_z_array[0] corresponds to the same character in z_array[M+1]
#     #we want to check for z_array[i] + rev_z_array[i-M-1+M-1] == M-2, which is simply z_array[i] + rev_z_array[i-2] == M-2
#     elif z_array[i] + rev_z_array[i-2] == M-2: 
#         if text[i-M-1] == pat[z_array[i] + 1] and text[i-M] == pat[z_array[i]]:
#             res += str(i-M) + " " + str(i + z_array[i] - M) + "\n"
#             count += 1

# print(count)
# print(res)

txt = "abcdefghabcdefgh"
z_arr = z_algo(txt)
print(z_arr)
period = 0
for i in range(len(z_arr)-1,0,-1):
    if z_arr[i] > 0:
        period = z_arr[i]
        break
if period == 0 or period == 1 and txt[0] != txt[1]:
    print("string not periodic")
for i in range(0,len(z_arr),period):
    if z_arr[i] == 0 or z_arr[i] % period != 0:
        print("string not periodic")
    
print("String with period " + str(period))





