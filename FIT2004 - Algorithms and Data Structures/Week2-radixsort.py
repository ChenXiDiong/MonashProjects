import math

def radix_sort(a_list):
    """
    Splits each item in a_list into k columns, and performs counting sort onto each column.

    :Input:
        a_list: An unsorted list of items.

    :Output: A sorted version of a_list.

    :Time complexity: O(KN) + O(KM), where M is the number of unique characters (i.e. 10 for integers in base 10, or 26 for all uppercase or all lowercase characters), N is 
    the size of the input list, K is the number of digits/characters of an item in the list. The worst case is when we split the items into K different columns, and run
    counting sort on all of them. The time complexity of counting sort is O(M+N), therefore the overall time complexity would be O(K) * O(M+N) = O(KM + KN)

    :Auxiliary space complexity : O(N), where N is the number of items in a_list. Originally it should be O(M+N) for the complexity of counting sort, but since M is constant 
    (i.e. we would always create the same amount of arrays in count_array for every call of counting sort, and the arrays would be cleaned up by the garbage collector after 
    each call), the auxiliary space complexity can be taken as O(N).
    """
    if type(a_list[0]) == int:
        sort = stable_counting_sort 
        k = len(str(max(a_list)))
    else: 
        sort = stable_counting_sort_alpha
        k = max(len(item)for item in a_list)
    col = k-1
    while col >= 0:
        a_list = sort(a_list, col)
        col -= 1
    return a_list

def stable_counting_sort(a_list, col):
    """
    Uses a list of lists (count_array) to keep track of items in a_list, and then sorts the list by retrieving the items in order from count_array.   

    Precondition : a_list must have at least 1 item

    :Input:
        a_list: An unsorted list of integers.
        col: the current column to base the sort on.

    :Output: A sorted version of a_list.

    :Time complexity: O(M+N), where N is the number of items in the input list, and M is the number of lists in count_array. The worst case happens when all the items
    in the input list are unique, therefore it will require O(M) time to append every item into count_array. Finding the maximum in the list requires O(N) time, therefore
    the overall time complexity will be O(M) + O(N) = O(M+N).

    :Auxiliary space complexity: O(M+N), where N is the number of items in the the input list, and M is the number of unique items in the input list. There will always be 
    N items to sort, which has space complexity of O(N), and M arrays created in count_array, which has a space complexity of O(M). Therefore the total auxiliary space 
    complexity is O(M) + O(N) = O(M+N).
    """
    #find the maximum
    base = 10
    curr_max = a_list[0]//(base**col)%base
    for item in a_list:
        item = item//(base**col)%base
        if item > curr_max:
            curr_max = item
    
    #initialize count array
    count_array = [None] * (curr_max + 1) #[[]] * (curr_max + 1) makes copies of the same list
    for i in range(len(count_array)):
        count_array[i] = [] #ensures every list created is a new, separate list
    
    #update count array
    for item in a_list:
        index = item//(base**col)%base
        count_array[index].append(item)
    
    #update input array
    index = 0
    for nlist in count_array:
        for item in nlist:
            a_list[index] = item
            index += 1

    #a_list will be sorted
    return a_list

def stable_counting_sort_alpha(a_list, col):
    """
    Uses a list of lists (count_array) to keep track of items in a_list, and then sorts the list by retrieving the items in order from count_array.   

    Precondition : a_list must have at least 1 item

    :Input:
        a_list: An unsorted list of characters.

    :Output: A sorted version of a_list

    :Time complexity: O(M+N), where N is the number of items in the input list, and M is the number of lists in count_array. The worst case happens when all the items
    in the input list are unique, therefore it will require O(M) time to append every item into count_array. Finding the maximum in the list requires O(N) time, therefore
    the overall time complexity will be O(M) + O(N) = O(M+N).

    :Auxiliary space complexity: O(M+N), where N is the number of items in the the input list, and M is the number of unique items in the input list. There will always be 
    N items to sort, which has space complexity of O(N), and M arrays created in count_array, which has a space complexity of O(M). Therefore the total auxiliary space 
    complexity is O(M) + O(N) = O(M+N).
    """
    #find the maximum
    curr_max = -math.inf
    for item in a_list:
        if col < len(item):
            item = (ord(item[col]) - 65)
            if item > curr_max:
                curr_max = item
    
    #initialize count array
    count_array = [None] * (curr_max + 1) #[[]] * (curr_max + 1) makes copies of the same list
    for i in range(len(count_array)):
        count_array[i] = [] #ensures every list created is a new, separate list
    
    #update count array
    for item in a_list:
        if col < len(item):
            index = (ord(item[col]) - 65)
            count_array[index].append(item)
        else:
            count_array[0].append(item)
    
    #update input array
    index = 0
    for nlist in count_array:
        for item in nlist:
            a_list[index] = item
            index += 1
    
    #a_list will be sorted
    return a_list


list_a = [200,151,291,981,369,421,671]
list_b = ["cat","taco","tags","gitgud","gudetama","food"]
list_c = ["hello","elloh","eloho","abcde","weird"]
list_d = ["cAt","TacO","tAgS","gItGuD","guDeTamA","fOoD"]
"""
base = 10
col = 0
(200//(base**col))%base = 0
(151//(base**col))%base = 1
(291//(base**col))%base = 1
(369//(base**col))%base = 9

base = 10
col = 1
(200//(base**col))%base = 0
(151//(base**col))%base = 5
(291//(base**col))%base = 9
(369//(base**col))%base = 6

base = 10
col = 2
(200//(base**col))%base = 2
(151//(base**col))%base = 1
(291//(base**col))%base = 2
(369//(base**col))%base = 3
"""
#print(radix_sort(list_a))
print(radix_sort(list_d))
print(sorted(list_d))







