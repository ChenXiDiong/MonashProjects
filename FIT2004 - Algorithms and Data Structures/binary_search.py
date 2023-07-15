def binary_search(result_list, key, lo, hi):
    """
    Performs a binary search on a list of lists to find the list containing key.

    :Precondition: result_list is not empty.

    :Input:
        result_list: A list of lists containing the results.
        key: A number, the target to find in the results list.
        lo: A number, starting position
        hi: A number, end position

    :Output: A list containing the key.

    :Time Complexity: O(log N) where N is the length of result_list. The search range is always divided by half for each recursion.

    :Auxiliary Space Complexity: 
    """
    while lo < hi:
        mid = (lo+hi)//2
        print(result_list[mid][2])
        if result_list[mid][2] == key:
            return result_list[mid]
        elif result_list[mid][2] < key:
            return binary_search(result_list, key, mid+1, hi)
        else:
            return binary_search(result_list, key, lo, mid-1)
    return result_list[lo]