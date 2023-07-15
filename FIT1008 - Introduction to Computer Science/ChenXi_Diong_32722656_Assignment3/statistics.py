from hash_table import LinearProbePotionTable

english_small = open("C:/Users/User/OneDrive/Desktop/Monash/FIT1008/base/english_small.txt", "r")
english_small_lst = [word for word in english_small]
english_small_lst = english_small_lst[0].split(',')
english_large_lst = [word.upper() for word in english_small_lst]

#hash_base = 1
pt1 = LinearProbePotionTable(10, True, 20021)
pt2 = LinearProbePotionTable(10, False, 20021)

for i in range(len(english_small_lst)):
    pt1[english_small_lst[i]] = str(i)

for i in range(len(english_small_lst)):
    pt2[english_small_lst[i]] = str(i)

print(pt1.statistics())
print(pt2.statistics())

pt1 = LinearProbePotionTable(10, True, 20021)
pt2 = LinearProbePotionTable(10, False, 20021)

for i in range(len(english_large_lst)):
    pt1[english_large_lst[i]] = str(i)

for i in range(len(english_large_lst)):
    pt2[english_large_lst[i]] = str(i)

print(pt1.statistics())
print(pt2.statistics())

pt1 = LinearProbePotionTable(10, True, 45053)
pt2 = LinearProbePotionTable(10, False, 45053)

for i in range(len(english_small_lst)):
    pt1[english_small_lst[i]] = str(i)

for i in range(len(english_small_lst)):
    pt2[english_small_lst[i]] = str(i)

print(pt1.statistics())
print(pt2.statistics())

pt1 = LinearProbePotionTable(10, True, 45053)
pt2 = LinearProbePotionTable(10, False, 45053)

for i in range(len(english_large_lst)):
    pt1[english_large_lst[i]] = str(i)

for i in range(len(english_large_lst)):
    pt2[english_large_lst[i]] = str(i)

print(pt1.statistics())
print(pt2.statistics())

pt1 = LinearProbePotionTable(10, True, 77017)
pt2 = LinearProbePotionTable(10, False, 77017)

for i in range(len(english_small_lst)):
    pt1[english_small_lst[i]] = str(i)

for i in range(len(english_small_lst)):
    pt2[english_small_lst[i]] = str(i)

print(pt1.statistics())
print(pt2.statistics())

pt1 = LinearProbePotionTable(10, True, 77017)
pt2 = LinearProbePotionTable(10, False, 77017)

for i in range(len(english_large_lst)):
    pt1[english_large_lst[i]] = str(i)

for i in range(len(english_large_lst)):
    pt2[english_large_lst[i]] = str(i)

print(pt1.statistics())
print(pt2.statistics())

#hash_base = 20020
#hash_base = 77019