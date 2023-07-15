"""
S2 2022 FIT2004 Assignment 1
Python 3.9.6

Name: Diong Chen Xi
Student ID: 32722656
Email: cdio0004@student.monash.edu
"""

def stable_counting_sort_alpha(a_list, col):
    """
    Uses a list of lists (count_array) to keep track of items in a_list, and then sorts the list by retrieving the items in order from count_array.   

    Precondition : a_list must have at least 1 item

    :Input:
        a_list: An unsorted list of characters.

    :Return: A sorted version of a_list

    :Time complexity: O(M+N), where N is the number of items in the input list, and M is the number of lists in count_array. The worst case happens when all the items
    in the input list are unique, therefore it will require O(M) time to append every item into count_array. Finding the maximum in the list requires O(N) time, therefore
    the overall time complexity will be O(M) + O(N) = O(M+N).

    :Auxiliary space complexity: O(M+N), where N is the number of items in the the input list, and M is the number of unique items in the input list. There will always be 
    N items to sort, which has space complexity of O(N), and M arrays created in count_array, which has a space complexity of O(M). Therefore the total auxiliary space 
    complexity is O(M) + O(N) = O(M+N).
    """
    #find the maximum
    curr_max = ord(a_list[0][col])
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


def sort_team_comp(team_name):
    """
    Sorts a team's composition in lexicographical order.

    :Input:
        team_name: A string which consists of the team composition.

    :Return: A sorted version of team_name.

    :Time Complexity: O(M + N), N is the length of team_name and M is the number of lists in the count array of stable_counting_sort_alpha. The dominant line is 
    the function call to stable_counting_sort_alpha, which has a time complexity of O(M + N).

    :Auxiliary Space Complexity: O(N), where N is the length of team_name. An array consisting the individual characters of team_name is created, which has length n.
    """
    namelist = [chr for chr in team_name]
    namelist = stable_counting_sort_alpha(namelist, 0)
    team_name = ""
    for chr in namelist:
        team_name += chr
    return team_name


def pretty(result_list):
    """
    Sorts all the team compositions of results in lexicographical order.

    :Input:
        result_list: A list of lists containing the result of a single match. 

    :Postcondition: All the team compositions of every result in result_list is sorted by lexicographical order.

    :Time Complexity: O(NM + NK), where N is the number of items in result_list, M is the length of the team names in the results of result_list, and K is the number 
    of lists in the count array of stable_counting_sort_alpha. We will invoke sort_team_comp for each of the lists in result_list, which executes the function of 
    complexity O(M + K) for a total of N times. Since K is always a number ranging between 1 and 26, it can be treated as a constant, thus the overall time complexity 
    is O(NM).

    :Auxiliary Space Complexity: O(N) where N is the maximum length of the team names in result_list. O(N) auxiliary space is required for sort_team_comp.
    """
    for result in result_list:
        result[0], result[1] = sort_team_comp(result[0]), sort_team_comp(result[1])


def create_opposite_match(result):
    """
    Creates the opposite match for a certain result. E.g. ["AEE", "ABC", 85] will have a result of ["ABC", "AEE", 15].

    :Input:
        result: A list containing team1: string, team2: string, score: int.

    :Return: A list containing the opposite match for result.

    :Time Complexity: O(1). List access and mathematical operations are O(1). And the size of result is always 3.

    :Auxiliary Space Complexity: O(1). A list of size 3 is created.
    """
    return [result[1], result[0], 100-result[2]]


def team_counting_sort(res_list, col, team, carray_size):
    """
    Uses a list of lists (count_array) to keep track of items in a_list, and then sorts the list by retrieving the items in order from count_array.   

    Precondition : res_list must have at least 1 item, col must be between 0 to maximum length of team name in the results of res_list, team must be
    1 or 2.

    :Input:
        res_list: An unsorted list of lists.
        col: An integer specifying the column of team name to perform counting sort on.
        team: An integer specifying which team name to sort.
        carray_size: An integer specifying the number of empty lists to create for the count array.

    :Return: A sorted version of res_list.

    :Time complexity: O(N + M), where N is the number of items in the input list, M is the value of carray_size. We have to put all N items in res_list in the count array 
    and creating M empty arrays in the count array required O(M) time.

    :Auxiliary space complexity: O(M+N), where N is the number of items in the the input list, and M is the value of carray_size. There will always be 
    N items to sort, which requires space complexity of O(N) in the count array, and M arrays created in count_array has a space complexity of O(M). Therefore the total auxiliary space 
    complexity is O(M) + O(N) = O(M+N).
    """
    #initialize count array
    count_array = [None] * (carray_size + 1) #[[]] * (curr_max + 1) makes copies of the same list
    for i in range(len(count_array)):
        count_array[i] = [] #ensures every list created is a new, separate list
    
    #update count array
    for result in res_list:
        if col < len(result[team-1]):
            index = (ord(result[team-1][col]) - 65)
            count_array[index].append(result)
        else:
            count_array[0].append(result)
    
    #update input array
    index = 0
    for nlist in count_array:
        for item in nlist:
            res_list[index] = item
            index += 1
    
    #a_list will be sorted
    return res_list


def sort_res_by_team(res_list, team, carray_size):
    """
    Calls team_counting_sort to perform radix sort on a result list based on the team names.

    :Precondition: res_list is not empty.

    :Input:
        res_list: A list of lists containing results (team1, team2, score).
        team: An integer specifying the team to sort (team1 or team2).
        carray_size: An integer specifying the number of empty lists to create for the count array in team_counting_sort.

    :Postcondition: res_list is sorted by team names in lexicographical order.

    :Time complexity: O(KN + KM) where K is the maximum length of the team name of either team1 or team2 (whichever is specified) in 
    res_list, N is the number of items in res_list, and M is the number of lists in the count array created in team_counting_sort.

    :Auxiliary space complexity: O(N) where N is the length of res_list. max() requires O(N) space, and team_counting_sort requires 
    O(M+N) space, where M is the maximum number of count arrays created in team_counting_sort. However, since the team names are always
    capital letters, we can treat M as a constant since it will always range from 1 to 26, therefore the total auxiliary space is O(N).
    """
    k = max([len(result[team-1]) for result in res_list])
    while k > 0:
        res_list = team_counting_sort(res_list, k-1, team, carray_size)
        k -= 1


def score_counting_sort(res_list, col):
    """
    Performs counting sort on a specific column of the scores of res_list by the column specified (col).   

    Precondition : res_list must have at least 1 item

    :Input:
        res_list: An unsorted list of lists.

    :Return: A sorted version of res_list by score descending.

    :Time complexity: O(M+N), where N is the number of items in the input list, and M is the number of lists in count_array. The worst case happens when all the items
    in the input list are unique, therefore it will require O(M) time to append every item into count_array. Finding the maximum in the list requires O(N) time, therefore
    the overall time complexity will be O(M) + O(N) = O(M+N).

    :Auxiliary space complexity: O(M+N), where N is the number of items in the the input list, and M is the number of unique items in the input list. There will always be 
    N items to sort, which has space complexity of O(N), and M arrays created in count_array, which has a space complexity of O(M). Therefore the total auxiliary space 
    complexity is O(M) + O(N) = O(M+N).
    """
    #find the maximum
    base = 10
    curr_max = res_list[0][2]//(base**col)%base
    for result in res_list:
        item = result[2]//(base**col)%base
        if item > curr_max:
            curr_max = item
    
    #initialize count array
    count_array = [None] * (curr_max + 1) #[[]] * (curr_max + 1) makes copies of the same list
    for i in range(len(count_array)):
        count_array[i] = [] #ensures every list created is a new, separate list
    
    #update count array
    for result in res_list:
        index = result[2]//(base**col)%base
        count_array[len(count_array)-index-1].append(result)
    
    #update input array
    index = 0
    for nlist in count_array:
        for item in nlist:
            res_list[index] = item
            index += 1

    #a_list will be sorted
    return res_list


def sort_res_by_score(res_list):
    """
    Calls score_counting_sort to perform radix sort on a result list based on the scores.

    :Precondition: res_list is not empty.

    :Input:
        res_list: A list of lists containing results (team1, team2, score).

    :Postcondition: res_list is sorted by score descending.

    :Time complexity: O(KN + KM) where K is the maximum length of the score converted to string in res_list, N is the number of items 
    in res_list, and M is the number of lists in the count array created in score_counting_sort.

    :Auxiliary space complexity: O(N) where N is the length of res_list. max() requires O(N) space, and score_counting_sort requires 
    O(M+N) space, where M is the base we're sorting the list in. However, since the base is always 10, we can treat M as a constant,
    therefore the total auxiliary space is O(N).
    """
    k = max([len(str(result[2])) for result in res_list])
    col = 0
    while col < k:
        res_list = score_counting_sort(res_list, col)
        col += 1


def binary_search(result_list, key, lo, hi):
    """
    Performs a binary search on a list of lists to find the list containing key.

    :Precondition: result_list is not empty.

    :Input:
        result_list: A list of lists containing the results.
        key: A number, the target to find in the results list.
        lo: A number, starting position
        hi: A number, end position (exclusive)

    :Return: A list containing the key if found, else return the list containing the next highest.

    :Time Complexity: O(log N) where N is the length of result_list. The search range is always divided by half for each iteration, so
    the maximum number of operations would be log N.

    :Auxiliary Space Complexity: O(1), since no extra space is added.
    """
    curr_min = result_list[0] #keeps track of the minimum element greater than key
    while 0 <= lo < len(result_list)  and lo <= hi:
        mid = (lo+hi)//2
        if result_list[mid][2] >= key and result_list[mid][2] < curr_min[2]:
            curr_min = result_list[mid]
        if result_list[mid][2] == key:
            return result_list[mid]
        elif result_list[mid][2] < key:
            hi = mid-1
        else:
            lo = mid+1
    
    return curr_min


def dnf(res_list, target):
    """
    Performs the Dutch National Flag algorithm to find all the elements containing the target specified.

    :Precondition: res_list is not empty.

    :Input:
        res_list: A list of lists containing results (team1, team2, score)
        target: A target score to be searched for.

    :Return: A list containing all the results containing the target score.

    :Time complexity: O(N) where N is the number of items in res_list. It will loop through the whole list no matter what and perform swapping which is in O(1).

    :Auxiliary space complexity: O(1) since it only performs swapping in the original list.
    """
    boundary1 = 0
    j = 0
    boundary2 = len(res_list)-1
    while j <= boundary2:
        if res_list[j][2] < target:
            res_list[j], res_list[boundary1] = res_list[boundary1], res_list[j]
            boundary1 += 1
            j += 1
        elif  res_list[j][2] > target:
            res_list[j], res_list[boundary2] = res_list[boundary2], res_list[j]
            boundary2 -= 1
        else:
            j += 1
    return res_list[boundary1:boundary2+1]


def analyze(results, roster, score):
    """
    Returns a list of findings denoted as [top10matches, searchedmatches] where top10matches is a list of 10 matches with the highest score, and searchedmatches is 
    a list of matches with the same score as score, matches with the closest score if not, and an empty list if there are none.

    :Precondition: results is not empty, score must be within 0-100.

    :Input:
        results: A list of lists containing the results [team1, team2, score].
        roster: An integer denoting the maximum number of unique characters of team matchups.
        score: An integer denoting the score to be searched for searchedmatches.

    :Return:
        top10matches: A list of results containing the 10 matches with the highest score, or maximum number of matches possible if there are less than 10 matches.
        searchedmatches: A list of results containing the same score as score, results with the closest score if not, and an empty list if there are none.

    :Time complexity: O(NM). The dominant line is the call to the pretty() function, which runs in O(NM) time, where N is the number of items in results, and M is the 
    length of the team name in the items of results.

    :Auxiliary space complexity: O(M+N).
    Assuming N is the number of items in results, M is the maximum length of team name in results.
    pretty : O(M)
    sort_res_by_team : O(N)
    sort_res_by_score : O(N) 
    binary_search : O(1)
    dnf : O(1)
    The total auxiliary space complexity would be O(M) + 2O(N) + O(1) + O(1) = O(M+N).
    """
    #sort the team names in lexicographical order to facilitate sorting later
    pretty(results)

    #creates the opposite matches of the results 
    results2 = []
    for result in results:
        if result not in results2:
            results2.append(result)
        if create_opposite_match(result) not in results2:
            results2.append(create_opposite_match(result))
    results = results2

    #sorting the results
    sort_res_by_team(results,2,roster) 
    sort_res_by_team(results,1,roster) 
    sort_res_by_score(results) 

    #solving for top10matches
    top10matches = []
    i = 0
    while len(top10matches) < 10 and i < len(results):
        top10matches.append(results[i])
        i += 1
    
    #solving for searchedmatches
    newscore = binary_search(results, score, 0, len(results))[2]
    searchedmatches = []
    if newscore >= score: 
        searchedmatches = dnf(results, newscore)
        sort_res_by_team(searchedmatches, 2, roster)
        sort_res_by_team(searchedmatches, 1, roster)
        sort_res_by_score(searchedmatches)

    #return result
    return [top10matches, searchedmatches]



