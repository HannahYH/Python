from math import sqrt

three_digit_list = []
for i in range(100,1000):
    three_digit_list.append(i)
#three_digit_list

def is_sum_of_two_square(three_digit):
    for a in range(int(sqrt(three_digit))+1):
        for b in range(int(sqrt(three_digit))+1):
            if (a*a + b*b) == three_digit:
                return [a,b]
    return []        

pair = []
result_list = []
for i in range(len(three_digit_list)-2):
    pair1=is_sum_of_two_square(three_digit_list[i])
    pair2=is_sum_of_two_square(three_digit_list[i+1])
    pair3=is_sum_of_two_square(three_digit_list[i+2])
    if pair1 != [] and pair2 != [] and pair3 != []:
        result_list.append([three_digit_list[i],three_digit_list[i+1],three_digit_list[i+2],\
                           pair1,pair2,pair3])

for line in result_list:
    print(f'({str(line[0])}, {str(line[1])}, {str(line[2])}) (equal to ('
                            f'{str(line[3][0])}^2+{str(line[3][1])}^2, '
                            f'{str(line[4][0])}^2+{str(line[4][1])}^2, '
                            f'{str(line[5][0])}^2+{str(line[5][1])}^2'')) is a solution.')
