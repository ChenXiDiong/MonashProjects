# Add comments to this file
def binary_search(the_list: list, target: int, low: int, high: int) -> int:
    #if the range is invalid, return -1 as the result
    if low > high:
        return -1
    else:
        mid = (high + low) // 2 #finding the midpoint of the given range

        if the_list[mid] == target: 
            return mid #target's index found
        elif the_list[mid] > target:
            return binary_search(the_list, target, low, mid - 1) #if the current midpoint is larger than the target, reduce the search range to the lower half of the list. 
        else:
            return binary_search(the_list, target, mid + 1, high) #if the current midpoint is smaller than the target, reduce the search range to the upper half of the list.
        
    
    #since the length of the search list is always halving, the total complexity of the function is O(logn).


def main() -> None:
    arr = [1, 5, 10, 11, 12]
    index = binary_search(arr, 11, 0, len(arr) - 1)
    print(index)


main()
