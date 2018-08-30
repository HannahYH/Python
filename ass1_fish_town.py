import os.path
import sys
import os

try:
    file_name = input('Which data file do you want to use? ')
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
if not os.path.isfile(file_name):
    print(f'I could not find {file_name}. Giving up...')
    sys.exit()
    
f = open(file_name)#coast_2.txt
file_result = []  
result = []
result_temp = []
for line in open(file_name):
    line = f.readline()
    file_result.append(line)
    result += [[]] 
    result_temp += [[]] 
for i in range(len(file_result)):
    for j in file_result[i].split():
        if j != ' ' and j != '\n':
            result[i].append(int(j))
            result_temp[i].append(int(j))
result.sort()
result_temp.sort(key=lambda x:x[1])
min_fish = result_temp[0][1]
max_fish = 0
for item in result_temp:
    max_fish += item[1]
max_fish = int(max_fish/len(result_temp))

list_min_max = [min_fish, max_fish]

result_temp.sort()

average_fish = int((list_min_max[0] + list_min_max[1]) / 2)
print('average_fish_firsttime:', average_fish)

while True:
    for i in range(len(result_temp)-1): 
        if result_temp[i][1] < average_fish:
            result_temp[i+1][1] -= ((average_fish-result_temp[i][1])+(result_temp[i+1][0]-result_temp[i][0]))
            result_temp[i][1] = average_fish
        elif result_temp[i][1] > average_fish:
            if (result_temp[i][1]-average_fish) > (result_temp[i+1][0]-result_temp[i][0]):
                result_temp[i+1][1] += ((result_temp[i][1]-average_fish)-(result_temp[i+1][0]-result_temp[i][0]))
            result_temp[i][1] = average_fish


    if result_temp[len(result_temp)-1][1] > average_fish: #ave取小了
        list_min_max[0] = average_fish
    elif result_temp[len(result_temp)-1][1] < average_fish:
        list_min_max[1] = average_fish
    
    count_of_average_fish = 0
    for item in result_temp:
        if item[1] == average_fish:
            count_of_average_fish += 1
    if count_of_average_fish == len(result_temp):
        break
    
    if average_fish == int((list_min_max[0] + list_min_max[1]) / 2):
        average_fish = int((list_min_max[0] + list_min_max[1]) / 2)
        break
    
    average_fish = int((list_min_max[0] + list_min_max[1]) / 2)
    
    result_temp = []
    for i in range(len(result)):
        result_temp += [[]]
        result_temp[i].append(result[i][0])
        result_temp[i].append(result[i][1])

print(f'The maximum quantity of fish that each town can have is {int(average_fish)}.')
#coast_2.txt
