# Finds all triples of positive integers (i, j, k) such that
# i, j and k are two digit numbers, i < j < k,
# every digit occurs at most once in i, j and k,
# and the product of i, j and k is a 6-digit number
# consisting precisely of the digits that occur in i, j and k.


# Insert your code here

two_digits = []
for i in range(10, 100):
    if i//10 != i%10:
        two_digits.append(str(i))

target = []
for item1 in two_digits:
    left_digits = set()
    right_digits = set()
    left_digits.add(item1[0])
    left_digits.add(item1[1])
    for item2 in two_digits:
        if item2[0] not in left_digits and item2[1] not in left_digits:
            left_digits.add(item2[0])
            left_digits.add(item2[1])
            for item3 in two_digits:
                if item3[0] not in left_digits and item3[1] not in left_digits:
                    left_digits.add(item3[0])
                    left_digits.add(item3[1])
                    right_digits = set(str(int(item1)*int(item2)*int(item3)))
                    if right_digits == left_digits:
                        target.append([int(item1),int(item2),int(item3),int(item1)*int(item2)*int(item3)])
                    left_digits -= set(item3)
            left_digits -= set(item2)
    left_digits -= set(item1)
    
#print(target)
result = []
for i in range(len(target)-1):
    for j in range(i+1,len(target)):
        if set(target[i]) == set(target[j]):
            break
    if j == len(target)-1:#mei you zhao dao yu ta xiang tong de
        result.append(sorted(target[i]))#an shuzi daxiao paixu
result.sort()


for line in result:
    print(f'{line[0]} x {line[1]} x {line[2]} = {line[3]} is a solution.')

#print(target_set)

                    
