# Add comments to this file
from typing import List, TypeVar

T = TypeVar('T')


def insertion_sort(the_list: List[T]):
    """
    Input: An unsorted list
    Output: None

    Description: Sorts an input list (the_list) in ascending order using insertion sort.
    """
    #let n = length
    length = len(the_list) #assignment, complexity O(1)
    for i in range(1, length): #complexity O(n)
        key = the_list[i]  #sets the key as the ith number in the list, complexity O(1)
        j = i-1 #j is always 1 less than i, complexity O(1)
        while j >= 0 and key < the_list[j]: #keep on swapping the key with its previous number until the key is the smallest number from i-1 onwards, complexity O(n)
            the_list[j + 1] = the_list[j] #if the key is less than its previous number, swap the two, complexity O(1)
            j -= 1 #control, complexity O(1)
        the_list[j + 1] = key #now that the_list[i-1] is sorted, move the key onward to the next number complexity O(1)
    
    #overall complexity: O(n^2)


def main() -> None:
    arr = [6, -2, 7, 4, -10]
    insertion_sort(arr)
    for i in range(len(arr)):
        print(arr[i], end=" ")
    print()


main()