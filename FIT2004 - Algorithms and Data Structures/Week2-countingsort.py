#%% Counting sort function
def counting_sort(new_list):
    """
    Precondition : new_list must have at least 1 item

    Drawback: it is unstable - we only remember the frequency, the relative ordering isn't taken into account
    --> can be resolved with more memory

    Space : O(M + N)
    Auxiliary space : O(M)
    """
    #find the maximum
    max_item = new_list[0]
    for item in new_list:
        if item > max_item:
            max_item = item

    #initialize count array
    count_array = [0] * (max_item + 1)
    
    #update count array
    for item in new_list:
        count_array[item] += 1
    
    #update input array
    index = 0
    for i in range(len(count_array)):
        item = i
        frequency = count_array[i]
        for j in range(frequency):
            new_list[index] = item
            index = index + 1

    #new_list will be sorted
    return new_list

def counting_sort_alpha(new_list):
    """
    Precondition : new_list must have at least 1 item
    """
    #find the maximum
    max_item = ord(new_list[0])- 97 #starts from a, unicode 97
    for item in new_list:
        item = ord(item) - 97
        if item > max_item:
            max_item = item

    #initialize count array
    count_array = [0] * (max_item + 1)
    
    #update count array
    for item in new_list:
        item = ord(item) - 97
        count_array[item] += 1
    
    #update input array
    index = 0
    for i in range(len(count_array)):
        item = i
        frequency = count_array[i]
        for j in range(frequency):
            new_list[index] = chr(item + 97)
            index = index + 1

    #new_list will be sorted
    return new_list

#%% Stable counting sort function
def stable_counting_sort(new_list):
    """
    Precondition : new_list must have at least 1 item

    Drawback: it is unstable - we only remember the frequency, the relative ordering isn't taken into account
    --> can be resolved with more memory

    Space: O(M + N)
    Auxiliary space: O(M + N)
    """
    #find the maximum
    max_item = new_list[0]
    for item in new_list:
        if item > max_item:
            max_item = item
    
    #initialize count array
    count_array = [None] * (max_item + 1) #[[]] * (max_item + 1) makes copies of the same list
    for i in range(len(count_array)):
        count_array[i] = [] #ensures every list created is a new, separate list
    
    #update count array
    for item in new_list:
        count_array[item].append(item)
    
    #update input array
    index = 0
    for nlist in count_array:
        for item in nlist:
            new_list[index] = item
            index += 1

    #new_list will be sorted
    return new_list

def stable_counting_sort_alpha(new_list):
    """
    Precondition : new_list must have at least 1 item

    Drawback: it is unstable - we only remember the frequency, the relative ordering isn't taken into account
    --> can be resolved with more memory

    Space: O(M + N)
    Auxiliary space: O(M + N)
    """
    #find the maximum
    max_item = ord(new_list[0]) - 97
    for item in new_list:
        item = ord(item) - 97
        if item > max_item:
            max_item = item
    
    #initialize count array
    count_array = [None] * (max_item + 1) #[[]] * (max_item + 1) makes copies of the same list
    for i in range(len(count_array)):
        count_array[i] = [] #ensures every list created is a new, separate list
    
    #update count array
    for item in new_list:
        item = ord(item) - 97
        count_array[item].append(item)
    
    #update input array
    index = 0
    for nlist in count_array:
        for item in nlist:
            new_list[index] = chr(item + 97)
            index += 1

    #new_list will be sorted
    return new_list

#%%Driver
list_a = [6,3,1,7,2,8,1,7]
list_b = ["a", "b", "a", "c", "x", "a"]
print(list_a)
list_a = stable_counting_sort(list_a)
print(list_a)

print(list_b)
list_b = stable_counting_sort_alpha(list_b)
print(list_b)

#check
for i in range(len(list_a)-1):
    if list_a[i] > list_a[i+1]:
        print("fail!")
print("pass")

for i in range(len(list_b)-1):
    if ord(list_b[i]) > ord(list_b[i+1]):
        print("fail!")
print("pass")


# %%
