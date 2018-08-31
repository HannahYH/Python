import sys

input_str = input('Please input a string of lowercase letters: ')

consecutive_strs_list = []
if len(input_str) > 1:
    for i in range(len(input_str)-1):
        consecutive_strs_list += [[input_str[i]]]
        j = 0
        current_element = input_str[i]
        for e in input_str[i:]:
            if ord(e) - ord(current_element) == 1:
                consecutive_strs_list[-1].append(e)
                current_element = e
    len_list = []
    for item in consecutive_strs_list:
        len_list.append(len(item))
    result = consecutive_strs_list[len_list.index(max(len_list))]
else:
    result = [input_str[0]]
    
print('The solution is: ', end='')
for e in result:
    print(e, end='')
print()
