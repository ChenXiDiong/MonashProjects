def dnf(a_list, target):
    boundary1 = 0
    j = 0
    boundary2 = len(a_list)-1
    while j <= boundary2:
        if a_list[j] < target:
            a_list[j], a_list[boundary1] = a_list[boundary1], a_list[j]
            boundary1 += 1
            j += 1
        elif  a_list[j] > target:
            a_list[j], a_list[boundary2] = a_list[boundary2], a_list[j]
            boundary2 -= 1
        else:
            j += 1
    return a_list[boundary1:boundary2+1]
    

list_a = [1,3,2,4,5,3,2,3,5,1,4,2,3,3,2,1]
print(dnf(list_a,5))