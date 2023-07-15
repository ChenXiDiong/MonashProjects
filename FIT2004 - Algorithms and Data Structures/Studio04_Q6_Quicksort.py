import random

def randomised_quicksort(a_list):
    if len(a_list) == 0 or len(a_list) == 1:
        return a_list
    pivot = a_list[random.randint(0, len(a_list)-1)]
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
    return randomised_quicksort(left) + middle + randomised_quicksort(right)

print(randomised_quicksort([7,4,1,3,1,1,1,1,1,1,6,5,2]))

