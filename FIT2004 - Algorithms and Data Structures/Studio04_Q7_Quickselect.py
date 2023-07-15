import random

def randomised_quickselect(a_list, k):
    pivot = a_list[random.randint(0, len(a_list)-1)]
    left = []
    right = []
    
    for i in range(len(a_list)):
        if a_list[i] <= pivot:
            left.append(a_list[i])
        else:
            right.append(a_list[i])
        
    if len(left) == k:
        return left
    elif len(left) > k:
        return left[0:k]
    else:
        return left + randomised_quickselect(right, k-len(left))

print(randomised_quickselect([1,1,1,1,1,1,1,1,1,1,1], 8))

def quicksort(a_list):
    if len(a_list) == 0 or len(a_list) == 1:
        return a_list
    pivot = max(randomised_quickselect(a_list, len(a_list)//2))
    left = []
    right = []
    middle = []
    for i in range(len(a_list)):
        if a_list[i] < pivot:
            left.append(a_list[i])
        elif a_list[i] > pivot:
            right.append(a_list[i])
        else:
            middle.append(a_list[i])
    return quicksort(left) + middle + quicksort(right)

print(quicksort([7,4,1,3,1,1,1,1,1,1,6,5,2]))