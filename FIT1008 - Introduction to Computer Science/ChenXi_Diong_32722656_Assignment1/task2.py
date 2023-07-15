size = int(input("Enter array length: "))
the_list = [None]*size
n = int(input("Enter n: "))
count = 0

for i in range(len(the_list)):
    the_list[i] = int(input("Enter the value: "))
    if the_list[i] % n == 0 and the_list[i] != n:
        count += 1

print("\nThe number of multiples (excluding itself) = " + str(count))
