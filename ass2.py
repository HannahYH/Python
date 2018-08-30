import sys
import os
from collections import defaultdict

def int2bin(n, count=24):   
    return "".join([str((n >> y) & 1) for y in range(count-1, -1, -1)])

def find_repeat(line):
    repeat_num = 0
    for i in range(1, (len(line)//2+1)):#the length of the repeat unit is i, from 1 to len(line)//2
        repeat_unit = []
        is_repeat = True
        for j in range(i):
            repeat_unit += [line[j]]
        for k in range(i, len(line)-1, i):
            if line[k: k+i] != repeat_unit:
                is_repeat = False
                break
        if is_repeat == True:
            repeat_num = len(line)//i
            break 
    return repeat_num

class FriezeError(Exception):
    def __init__(self, message):
        self.message = message

class Frieze():
    def __init__(self, filename):
        if not os.path.isfile(filename):
            print(f'I could not find {filename}. Giving up...')
            sys.exit()
            
        f = open(filename)
        file_result = []#original data
        result = []#2bit data
        valid_num_flag = True
        len_num_flag = True
        height_num_flag = True
        same_len_flag = True
        top_line_valid_flag = True
        bottom_line_valid_flag = True
        left_line_valid_flag = True
        right_line_valid_flag = True
        crossing_falg = True
        repeat_flag = False
        self.filename = filename
        self.repeat_len = 0
        self.frizez_dict = defaultdict(list)
        self.frizez_dict = {'N2S':[], 'NW2SE':[], 'W2E':[], 'SW2NE':[]}#record the pairs of coordinate of every draw type
        self.frizez_result = []#record decomposed numbers of every number

        for line in open(filename):
            line = f.readline()
            line_list = list(line.split())
            if line_list != []:#remove the lines only contain space
                file_result += [[]]
                for item in line_list:
                    if item.isdigit() and int(item) <= 15 and int(item) >=0:
                        file_result[-1] += [int(item)]
                    else:
                        valid_num_flag = False#only space and digits allowed
                        break
                if len(file_result[-1]) < 5 or len(file_result[-1]) > 51:
                    len_num_flag = False
                    break
           
        if len(file_result) < 3 or len(file_result) > 17:
            height_num_flag = False
        else:
            len_0 = len(file_result[0])        
            for line in file_result:
                if len(line) != len_0:
                    same_len_flag = False
                    break

        if valid_num_flag and len_num_flag and height_num_flag and same_len_flag:
            for item in file_result[0][:-2]:
                if not (item == 4 or item == 12):
                    top_line_valid_flag = False
                    break
            if file_result[0][-1] != 0:
                top_line_valid_flag = False

            for item in file_result[-1][:-2]:
                if not (item >= 4 and item <= 7):
                    bottom_line_valid_flag = False
                    break

            for i in range(len(file_result)):
                if file_result[i][-1] > 1:
                    right_line_valid_flag = False
                    break
                if file_result[i][-1] == 1 and (file_result[i][0] % 2 != 1):
                    left_line_valid_flag = False
                    break
                if file_result[i][-1] == 0 and (file_result[i][0] % 2 == 1):
                    left_line_valid_flag = False
                    break

            for i in range(len(file_result)-1):
                for j in range(len(file_result[i])):
                    if file_result[i][j] >= 8 and (file_result[i+1][j] % 4 == 2 or file_result[i+1][j] % 4 == 3):
                        crossing_falg = False
                        break
                    
            repeat_times_list = []
            for line in file_result:
                repeat_times_list.append(find_repeat(line))
            repeat_times = min(repeat_times_list)
            if repeat_times:
                self.repeat_len = (len(file_result[0])-1)//repeat_times#repeat_times
                if self.repeat_len >= 2:
                    for line in file_result:
                        repeat_unit = []
                        is_repeat = True
                        #print(self.repeat_len,repeat_times,len(file_result[0]))
                        for j in range(self.repeat_len):#length of repeatation
                            repeat_unit += [line[j]]
                        for k in range(self.repeat_len, len(line)-1, self.repeat_len):
                            if line[k: k+self.repeat_len] != repeat_unit:
                                is_repeat = False
                                break
                    if is_repeat == True and repeat_times >= 2 and (len(file_result[0])-1) % self.repeat_len == 0:
                        #print(self.repeat_len, repeat_times)
                        repeat_flag = True
                else:
                    repeat_flag = False

            if top_line_valid_flag and bottom_line_valid_flag and left_line_valid_flag and right_line_valid_flag and crossing_falg and repeat_flag:
                for line in file_result:
                    temp_line = []
                    for item in line:
                        temp_line += [int2bin(int(item),4)]
                    result += [temp_line]
                for i in range(len(result)):
                    self.frizez_result += [[]]
                    for j in range(len(result[i])):
                        self.frizez_result[-1] += [[]]
                        if result[i][j][0] == '1':
                            self.frizez_dict['NW2SE'].append([(j,i),(j+1,i+1)])
                            self.frizez_result[-1][-1].append(8)
                        if result[i][j][1] == '1':
                            self.frizez_dict['W2E'].append([(j,i),(j+1,i)])
                            self.frizez_result[-1][-1].append(4)
                        if result[i][j][2] == '1':
                            self.frizez_dict['SW2NE'].append([(j,i),(j+1,i-1)])
                            self.frizez_result[-1][-1].append(2)
                        if result[i][j][3] == '1':
                            self.frizez_dict['N2S'].append([(j,i-1),(j,i)])
                            self.frizez_result[-1][-1].append(1)
            else:
                raise FriezeError('Input does not represent a frieze.')
        else:
            raise FriezeError('Incorrect input.')

    def is_horizon_sym(self, frizez_result, repeat_len):
        len_of_line = len(frizez_result[0])
        height = len(frizez_result)
        is_horizon_sym = True
        if height%2 == 0:#the number of interval is odd
            interval_line_num_1 = len(frizez_result)//2-1
            interval_line_num_2 = len(frizez_result)//2
            for j in range(repeat_len+2):
                if frizez_result[interval_line_num_1][j] == [] and frizez_result[interval_line_num_2][j] == []:
                    continue
                if 8 in frizez_result[interval_line_num_1][j] or 2 in frizez_result[interval_line_num_2][j]:#in this case, can not have diagonal, cos cross
                    is_horizon_sym = False
                    break
                if 4 in frizez_result[interval_line_num_1][j]:
                    if 4 not in frizez_result[interval_line_num_2][j]:
                        is_horizon_sym = False
                        break
                if 2 in frizez_result[interval_line_num_1][j]:
                    if 8 not in frizez_result[interval_line_num_2][j]:
                        is_horizon_sym = False
                        break
                if 1 in frizez_result[interval_line_num_1][j]:
                    if 1 not in frizez_result[interval_line_num_2+1][j]:
                        is_horizon_sym = False
                        break
                if 4 in frizez_result[interval_line_num_2][j]:
                    if 4 not in frizez_result[interval_line_num_1][j]:
                        is_horizon_sym = False
                        break
                if 8 in frizez_result[interval_line_num_2][j]:
                    if 2 not in frizez_result[interval_line_num_1][j]:
                        is_horizon_sym = False
                        break
            if is_horizon_sym:
                for i in range(interval_line_num_1):
                    for j in range(repeat_len+2):
                        if frizez_result[i][j] == [] and frizez_result[height-i-1][j] == []:
                            continue
                        #for the first line
                        if 2 in frizez_result[i][j]:
                            if 8 not in frizez_result[height-i-1][j]:
                                is_horizon_sym = False
                                break
                        if 8 in frizez_result[i][j]:
                            if 2 not in frizez_result[height-i-1][j]:
                                is_horizon_sym = False
                                break
                        if 4 in frizez_result[i][j]:
                            if 4 not in frizez_result[height-i-1][j]:
                                is_horizon_sym = False
                                break
                        if 1 in frizez_result[i][j]:
                            if 1 not in frizez_result[height-i][j]:
                                is_horizon_sym = False
                                break
                        #for the second line
                        if 2 in frizez_result[height-i-1][j]:
                            if 8 not in frizez_result[i][j]:
                                is_horizon_sym = False
                                break
                        if 8 in frizez_result[height-i-1][j]:
                            if 2 not in frizez_result[i][j]:
                                is_horizon_sym = False
                                break
                        if 4 in frizez_result[height-i-1][j]:
                            if 4 not in frizez_result[i][j]:
                                is_horizon_sym = False
                                break
                        if 1 in frizez_result[height-i-1][j]:
                            if 1 not in frizez_result[i+1][j]:
                                is_horizon_sym = False
                                break
        else:
            interval_line_num = len(frizez_result)//2
            for j in range(repeat_len+2):
                if frizez_result[interval_line_num][j] == []:
                    continue
                if 8 in frizez_result[interval_line_num][j]:
                    if 2 not in frizez_result[interval_line_num][j]:
                        is_horizon_sym = False
                        break
                if 2 in frizez_result[interval_line_num][j]:
                    if 8 not in frizez_result[interval_line_num][j]:
                        is_horizon_sym = False
                        break
                if 1 in frizez_result[interval_line_num][j]:
                    if 1 not in frizez_result[interval_line_num+1][j]:
                        is_horizon_sym = False
                        break
            if is_horizon_sym:
                for i in range(interval_line_num):
                    for j in range(repeat_len+2):
                        if frizez_result[i][j] == [] and frizez_result[height-i-1][j] == []:
                            continue
                        #for the first line
                        if 2 in frizez_result[i][j]:
                            if 8 not in frizez_result[height-i-1][j]:
                                is_horizon_sym = False
                                break
                        if 8 in frizez_result[i][j]:
                            if 2 not in frizez_result[height-i-1][j]:
                                is_horizon_sym = False
                                break
                        if 4 in frizez_result[i][j]:
                            if 4 not in frizez_result[height-i-1][j]:
                                is_horizon_sym = False
                                break
                        if 1 in frizez_result[i][j]:
                            if 1 not in frizez_result[height-i][j]:
                                is_horizon_sym = False
                                break
                        #for the second line
                        if 2 in frizez_result[height-i-1][j]:
                            if 8 not in frizez_result[i][j]:
                                is_horizon_sym = False
                                break
                        if 8 in frizez_result[height-i-1][j]:
                            if 2 not in frizez_result[i][j]:
                                is_horizon_sym = False
                                break
                        if 4 in frizez_result[height-i-1][j]:
                            if 4 not in frizez_result[i][j]:
                                is_horizon_sym = False
                                break
                        if 1 in frizez_result[height-i-1][j]:
                            if 1 not in frizez_result[i+1][j]:
                                is_horizon_sym = False
                                break
        return is_horizon_sym

    def is_glid_horizon_sym(self, frizez_result, repeat_len):
        len_of_line = len(frizez_result[0])
        height = len(frizez_result)
        is_glid_horizon_sym = True
        if repeat_len%2 == 1:
            return False
        if height%2 == 0:#the number of interval is odd
            interval_line_num_1 = len(frizez_result)//2-1
            interval_line_num_2 = len(frizez_result)//2
            for j in range(repeat_len+2):#judge these two middle lines whether valid
                col_num = j + repeat_len//2
                if frizez_result[interval_line_num_1][j] == [] and frizez_result[interval_line_num_2][col_num] == []:
                    continue
                if 4 in frizez_result[interval_line_num_1][j]:
                    if 4 not in frizez_result[interval_line_num_2][col_num]:
                        is_glid_horizon_sym = False
                        break
                if 2 in frizez_result[interval_line_num_1][j]:
                    if 8 not in frizez_result[interval_line_num_2][col_num]:
                        is_glid_horizon_sym = False
                        break
                if 1 in frizez_result[interval_line_num_1][j]:
                    if 1 not in frizez_result[interval_line_num_2+1][col_num]:
                        is_glid_horizon_sym = False
                        break
                if 4 in frizez_result[interval_line_num_2][col_num]:
                    if 4 not in frizez_result[interval_line_num_1][j]:
                        is_glid_horizon_sym = False
                        break
                if 8 in frizez_result[interval_line_num_2][col_num]:
                    if 2 not in frizez_result[interval_line_num_1][j]:
                        is_glid_horizon_sym = False
                        break
            if is_glid_horizon_sym:
                for i in range(interval_line_num_1):
                    for j in range(repeat_len+2):
                        col_num = j + repeat_len//2
                        if frizez_result[i][j] == [] and frizez_result[height-i-1][col_num] == []:
                            continue
                        if 2 in frizez_result[i][j]:
                            if 8 not in frizez_result[height-i-1][col_num]:
                                is_glid_horizon_sym = False
                                break
                        if 8 in frizez_result[i][j]:
                            if 2 not in frizez_result[height-i-1][col_num]:
                                is_glid_horizon_sym = False
                                break
                        if 4 in frizez_result[i][j]:
                            if 4 not in frizez_result[height-i-1][col_num]:
                                is_glid_horizon_sym = False
                                break
                        if 1 in frizez_result[i][j]:
                            if 1 not in frizez_result[height-i][col_num]:
                                is_glid_horizon_sym = False
                                break
                        #for the second line
                        if 2 in frizez_result[height-i-1][col_num]:
                            if 8 not in frizez_result[i][j]:
                                is_glid_horizon_sym = False
                                break
                        if 8 in frizez_result[height-i-1][col_num]:
                            if 2 not in frizez_result[i][j]:
                                is_glid_horizon_sym = False
                                break
                        if 4 in frizez_result[height-i-1][col_num]:
                            if 4 not in frizez_result[i][j]:
                                is_glid_horizon_sym = False
                                break
                        if 1 in frizez_result[height-i-1][col_num]:
                            if 1 not in frizez_result[i+1][j]:
                                is_glid_horizon_sym = False
                                break
        else:
            interval_line_num = len(frizez_result)//2
            for j in range(repeat_len+2):
                col_num = j + repeat_len//2
                if frizez_result[interval_line_num][j] == [] and frizez_result[interval_line_num][col_num] == []:
                    continue
                if 8 in frizez_result[interval_line_num][j]:
                    if 2 not in frizez_result[interval_line_num][col_num]:
                        is_glid_horizon_sym = False
                        break
                if 2 in frizez_result[interval_line_num][j]:
                    if 8 not in frizez_result[interval_line_num][col_num]:
                        is_glid_horizon_sym = False
                        break
                if 1 in frizez_result[interval_line_num][j]:
                    if 1 not in frizez_result[interval_line_num+1][col_num]:
                        is_glid_horizon_sym = False
                        break
            if is_glid_horizon_sym:
                for i in range(interval_line_num):
                    for j in range(repeat_len+2):
                        col_num = j + repeat_len//2
                        if frizez_result[i][j] == [] and frizez_result[height-i-1][col_num] == []:
                            continue
                        if 2 in frizez_result[i][j]:
                            if 8 not in frizez_result[height-i-1][col_num]:
                                is_glid_horizon_sym = False
                                break
                        if 8 in frizez_result[i][j]:
                            if 2 not in frizez_result[height-i-1][col_num]:
                                is_glid_horizon_sym = False
                                break
                        if 4 in frizez_result[i][j]:
                            if 4 not in frizez_result[height-i-1][col_num]:
                                is_glid_horizon_sym = False
                                break
                        if 1 in frizez_result[i][j]:
                            if 1 not in frizez_result[height-i][col_num]:
                                is_glid_horizon_sym = False
                                break
                        #for the second line
                        if 2 in frizez_result[height-i-1][col_num]:
                            if 8 not in frizez_result[i][j]:
                                is_glid_horizon_sym = False
                                break
                        if 8 in frizez_result[height-i-1][col_num]:
                            if 2 not in frizez_result[i][j]:
                                is_glid_horizon_sym = False
                                break
                        if 4 in frizez_result[height-i-1][col_num]:
                            if 4 not in frizez_result[i][j]:
                                is_glid_horizon_sym = False
                                break
                        if 1 in frizez_result[height-i-1][col_num]:
                            if 1 not in frizez_result[i+1][j]:
                                is_glid_horizon_sym = False
                                break
        return is_glid_horizon_sym

    def is_vertical_sym(self, frizez_result, repeat_len):
        len_of_line = len(frizez_result[0])
        height = len(frizez_result)
 #       is_vertical_sym = True
        #testing the even case
        #first step is to find the palce of vertical axis
        for j in range(1, repeat_len//2+1):#start with second column within one repeat_len
            #print(j)
 #           is_vertical_sym = True
            vertical_axis_1 = j#column number  only can have 1 and 4, 4 is dosent matter
            vertical_axis_2 = vertical_axis_1+1 # can have 1,2,4,8
            is_vertical_sym = True
            for i in range(height):
                is_vertical_sym = True#if some j col make it false, we should turn it to True for the next loop of j 
                if 2 in frizez_result[i][vertical_axis_1] or 8 in frizez_result[i][vertical_axis_1]:#in this case, can not have diagonal, cos cross
                    is_vertical_sym = False
                    break
                #for the first axis
                if 1 in frizez_result[i][vertical_axis_1]:
                    if 1 not in frizez_result[i][vertical_axis_2]:
                        is_vertical_sym = False
                        break
                #for the second axis
                if 1 in frizez_result[i][vertical_axis_2]:
                    if 1 not in frizez_result[i][vertical_axis_1]:
                        is_vertical_sym = False
                        break
                if 2 in frizez_result[i][vertical_axis_2]:
                    if 8 not in frizez_result[i-1][vertical_axis_1-1]:
                        is_vertical_sym = False
                        break
                if 8 in frizez_result[i][vertical_axis_2]:
                    if 2 not in frizez_result[i+1][vertical_axis_1-1]:
                        is_vertical_sym = False
                        break
                if 4 in frizez_result[i][vertical_axis_2]:
                    if 4 not in frizez_result[i][vertical_axis_1-1]:
                        is_vertical_sym = False
                        break
            #when i is finished, if it is true, then do the following judgement
            if is_vertical_sym:
                #second step is to judge whether it is vertical  , the range of judgement is repeat_len
                final_vertical_axis_1 = vertical_axis_1+repeat_len#move column number horizonly by one repeat_len
                final_vertical_axis_2 = final_vertical_axis_1+1
                #print('0', final_vertical_axis_1, final_vertical_axis_2)
                for k in range(1, repeat_len+1):#the range should +1
                    #print('k', k)
                    if final_vertical_axis_2+k < len_of_line and final_vertical_axis_1-k-1 >= 0:#is there should be <= ?
                        for i in range(height):
                            #print('i', i)
                            if frizez_result[i][final_vertical_axis_1-k] == [] and frizez_result[i][final_vertical_axis_2+k] == []:
                                continue
                            #for the first axis
                            if 1 in frizez_result[i][final_vertical_axis_1-k]:
                                if 1 not in frizez_result[i][final_vertical_axis_2+k]:
                                    is_vertical_sym = False
                                    break
                            if 2 in frizez_result[i][final_vertical_axis_1-k]:
                                if 8 not in frizez_result[i-1][final_vertical_axis_2+k-1]:
                                    is_vertical_sym = False
                                    break
                            if 4 in frizez_result[i][final_vertical_axis_1-k]:
                                if 4 not in frizez_result[i][final_vertical_axis_2+k-1]:
                                    is_vertical_sym = False
                                    break
                            if 8 in frizez_result[i][final_vertical_axis_1-k]:
                                if 2 not in frizez_result[i+1][final_vertical_axis_2+k-1]:
                                    is_vertical_sym = False
                                    break
                            #for the second axis
                            if 1 in frizez_result[i][final_vertical_axis_2+k]:
                                if 1 not in frizez_result[i][final_vertical_axis_1-k]:
                                    is_vertical_sym = False
                                    break
                            if 2 in frizez_result[i][final_vertical_axis_2+k]:
                                if 8 not in frizez_result[i-1][final_vertical_axis_1-k-1]:
                                    is_vertical_sym = False
                                    break
                            if 4 in frizez_result[i][final_vertical_axis_2+k]:
                                if 4 not in frizez_result[i][final_vertical_axis_1-k-1]:
                                    is_vertical_sym = False
                                    break
                            if 8 in frizez_result[i][final_vertical_axis_2+k]:
                                if 2 not in frizez_result[i+1][final_vertical_axis_1-k-1]:
                                    is_vertical_sym = False
                                    break
                    #else:
 #                      if
            if is_vertical_sym:
                #print(2)
                break
        #testing the odd case
        if not is_vertical_sym:
            #first step is to find the palce of vertical axis
            for j in range(1, repeat_len//2+1):#start with second column within one repeat_len
                vertical_axis = j#column number
                is_vertical_sym = True
                for i in range(height):
 #                   is_vertical_sym = True
                    if frizez_result[i][vertical_axis] == []:
                        continue
                    if 2 in frizez_result[i][vertical_axis]:
                        if 8 not in frizez_result[i-1][vertical_axis-1]:
                            is_vertical_sym = False
                            break
                    if 8 in frizez_result[i][vertical_axis]:
                        if 2 not in frizez_result[i+1][vertical_axis-1]:
                            is_vertical_sym = False
                            break
                    if 4 in frizez_result[i][vertical_axis]:
                        if 4 not in frizez_result[i][vertical_axis-1]:
                            is_vertical_sym = False
                            break
                if is_vertical_sym:
                    #second step is to judge whether it is vertical, the range of judgement is repeat_len
                    final_vertical_axis = vertical_axis+repeat_len#move column number horizonly by one repeat_len
                    for k in range(1, repeat_len + 1):#the range should +1
                        if final_vertical_axis+k < len_of_line and final_vertical_axis-k-1 >= 0:#is there should be <= ?
                            for i in range(height):
                                if frizez_result[i][final_vertical_axis-k] == [] and frizez_result[i][final_vertical_axis+k] == []:
                                    continue
                                #for the first axis
                                if 1 in frizez_result[i][final_vertical_axis-k]:
                                    if 1 not in frizez_result[i][final_vertical_axis+k]:
                                        is_vertical_sym = False
                                        break
                                if 2 in frizez_result[i][final_vertical_axis-k]:
                                    if 8 not in frizez_result[i-1][final_vertical_axis+k-1]:
                                        is_vertical_sym = False
                                        break
                                if 4 in frizez_result[i][final_vertical_axis-k]:
                                    if 4 not in frizez_result[i][final_vertical_axis+k-1]:
                                        is_vertical_sym = False
                                        break
                                if 8 in frizez_result[i][final_vertical_axis-k]:
                                    if 2 not in frizez_result[i+1][final_vertical_axis+k-1]:
                                        is_vertical_sym = False
                                        break
                                #for the second one
                                if 1 in frizez_result[i][final_vertical_axis+k]:
                                    if 1 not in frizez_result[i][final_vertical_axis-k]:
                                        is_vertical_sym = False
                                        break
                                if 2 in frizez_result[i][final_vertical_axis+k]:
                                    if 8 not in frizez_result[i-1][final_vertical_axis-k-1]:
                                        is_vertical_sym = False
                                        break
                                if 4 in frizez_result[i][final_vertical_axis+k]:
                                    if 4 not in frizez_result[i][final_vertical_axis-k-1]:
                                        is_vertical_sym = False
                                        break
                                if 8 in frizez_result[i][final_vertical_axis+k]:
                                    if 2 not in frizez_result[i+1][final_vertical_axis-k-1]:
                                        is_vertical_sym = False
                                        break
                if is_vertical_sym:
                    #print(1)
                    break
        return is_vertical_sym



    def is_rotation_sym(self, frizez_result, repeat_len):
        len_of_line = len(frizez_result[0])
        height = len(frizez_result)
        #print(height)
        is_rotation_sym = True
        if height%2 == 0:#the number of interval is odd
            #print('2*2')
            interval_line_num_1 = len(frizez_result)//2-1
            interval_line_num_2 = len(frizez_result)//2
            for j in range(1, repeat_len//2+1):#2*2
                sym_point_1_col = j
                sym_point_2_col = j+1
                is_rotation_sym = True#dont forget it!
                if 1 in frizez_result[interval_line_num_1][sym_point_1_col]:
                    if 1 not in frizez_result[interval_line_num_2+1][sym_point_2_col]:
                        is_rotation_sym = False
                if 2 in frizez_result[interval_line_num_1][sym_point_1_col]:
                    if 2 not in frizez_result[interval_line_num_2+1][sym_point_2_col-1]:
                        is_rotation_sym = False
                if 4 in frizez_result[interval_line_num_1][sym_point_1_col]:
                    if 4 not in frizez_result[interval_line_num_2][sym_point_2_col-1]:
                        is_rotation_sym = False
                #8 is fine itself for sym point1, do not need to be judged
                #for the second axis
                if 1 in frizez_result[interval_line_num_2][sym_point_2_col]:
                    if 1 not in frizez_result[interval_line_num_1+1][sym_point_1_col]:
                        is_rotation_sym = False
                if 2 in frizez_result[interval_line_num_2][sym_point_2_col]:
                    if 2 not in frizez_result[interval_line_num_1+1][sym_point_1_col-1]:
                        is_rotation_sym = False
                if 4 in frizez_result[interval_line_num_2][sym_point_2_col]:
                    if 4 not in frizez_result[interval_line_num_1][sym_point_1_col-1]:
                        is_rotation_sym = False
                if 8 in frizez_result[interval_line_num_2][sym_point_2_col]:
                    if 8 not in frizez_result[interval_line_num_1-1][sym_point_1_col-1]:
                        is_rotation_sym = False
                if is_rotation_sym:#if these 2 point is symmetric, to judge wether all point are symmetric about them
                    final_sym_point_1_col = sym_point_1_col+repeat_len
                    final_sym_point_2_col = final_sym_point_1_col+1
                    #print('final_sym_point_1_col:', final_sym_point_1_col)
                    for k in range(0, repeat_len+1):#the range should +1
                        #print('k: ', k)
                        if final_sym_point_2_col+k < len_of_line and final_sym_point_1_col-k-1 >= 0:#is there should be <= ????????????
                            #print('not out of range')
                            for row in range(height):#loop for half height is enough, otherwise it will range out of index
                                if frizez_result[row][final_sym_point_1_col-k] == [] and frizez_result[-(row+1)][final_sym_point_2_col+k] == []:
                                    continue
                                #first axis
                                if 1 in frizez_result[row][final_sym_point_1_col-k]:
                                    if 1 not in frizez_result[-(row+1)+1][final_sym_point_2_col+k]:
                                        #print(1)
                                        is_rotation_sym = False
                                        break
                                if 2 in frizez_result[row][final_sym_point_1_col-k]:
                                    if 2 not in frizez_result[-(row+1)+1][final_sym_point_2_col+k-1]:
                                        #print(2)
                                        is_rotation_sym = False
                                        break
                                if 4 in frizez_result[row][final_sym_point_1_col-k]:
                                    if 4 not in frizez_result[-(row+1)][final_sym_point_2_col+k-1]:
                                        #print(4)
                                        is_rotation_sym = False
                                        break
                                if 8 in frizez_result[row][final_sym_point_1_col-k]:
                                    if 8 not in frizez_result[-(row+1)-1][final_sym_point_2_col+k-1]:
                                        #print(8)
                                        is_rotation_sym = False
                                        break
                                #second axis
                                if 1 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                    if 1 not in frizez_result[row+1][final_sym_point_1_col-k]:
                                        #print(11)
                                        is_rotation_sym = False
                                        break
                                if 2 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                    if 2 not in frizez_result[row+1][final_sym_point_1_col-k-1]:
                                        #print(12)
                                        is_rotation_sym = False
                                        break
                                if 4 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                    if 4 not in frizez_result[row][final_sym_point_1_col-k-1]:
                                        #print(14)
                                        is_rotation_sym = False
                                        break
                                if 8 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                    if 8 not in frizez_result[row-1][final_sym_point_1_col-k-1]:
                                        #print(18)
                                        is_rotation_sym = False
                                        break
                        #elif (final_sym_point_1_col-k-1 < 0) and k < repeat_len//2:
 #                            is_rotation_sym = False
 #                            break
                if is_rotation_sym and k >= repeat_len//2:
                    break
            if not is_rotation_sym:#2*1
                #print('2*1')
                for j in range(1, repeat_len//2+1):
                    sym_point_col = j
                    is_rotation_sym = True#dont forget it!!
                    #first line point
                    if 1 in frizez_result[interval_line_num_1][sym_point_col]:
                        if 1 not in frizez_result[interval_line_num_2+1][sym_point_col]:
                            is_rotation_sym = False
                    if 2 in frizez_result[interval_line_num_1][sym_point_col]:
                        if 2 not in frizez_result[interval_line_num_2+1][sym_point_col-1]:
                            is_rotation_sym = False
                    if 4 in frizez_result[interval_line_num_1][sym_point_col]:
                        if 4 not in frizez_result[interval_line_num_2][sym_point_col-1]:
                            is_rotation_sym = False
                    if 8 in frizez_result[interval_line_num_1][sym_point_col]:
                        if 8 not in frizez_result[interval_line_num_2-1][sym_point_col-1]:
                            is_rotation_sym = False
                    #second line point
                    if 2 in frizez_result[interval_line_num_2][sym_point_col]:
                        if 2 not in frizez_result[interval_line_num_1+1][sym_point_col-1]:
                            is_rotation_sym = False
                    if 4 in frizez_result[interval_line_num_2][sym_point_col]:
                        if 4 not in frizez_result[interval_line_num_1][sym_point_col-1]:
                            is_rotation_sym = False
                    if 8 in frizez_result[interval_line_num_2][sym_point_col]:
                        if 8 not in frizez_result[interval_line_num_1-1][sym_point_col-1]:
                            is_rotation_sym = False
                    if is_rotation_sym:#if these 2 point is symmetric, to judge wether all point are symmetric about them
                        final_sym_point_col = sym_point_col+repeat_len
                        for k in range(0, repeat_len+1):#the range should +1
                            #print('k: ', k)
                            if final_sym_point_col+k < len_of_line and final_sym_point_col-k-1 >= 0:#is there should be <= ????????????
                                for row in range(height):#loop for half height is enough, otherwise it will range out of index
                                    if frizez_result[row][final_sym_point_col-k] == [] and frizez_result[-(row+1)][final_sym_point_col+k] == []:
                                        continue
                                    #for the first axis
                                    if 1 in frizez_result[row][final_sym_point_col-k]:
                                        if 1 not in frizez_result[-(row+1)+1][final_sym_point_col+k]:
                                            is_rotation_sym = False
                                            break
                                    if 2 in frizez_result[row][final_sym_point_col-k]:
                                        if 2 not in frizez_result[-(row+1)+1][final_sym_point_col+k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 4 in frizez_result[row][final_sym_point_col-k]:
                                        if 4 not in frizez_result[-(row+1)][final_sym_point_col+k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 8 in frizez_result[row][final_sym_point_col-k]:
                                        if 8 not in frizez_result[-(row+1)-1][final_sym_point_col+k-1]:
                                            is_rotation_sym = False
                                            break
                                    #second axis
                                    if 1 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                        if 1 not in frizez_result[row+1][final_sym_point_col-k]:
                                            is_rotation_sym = False
                                            break
                                    if 2 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                        if 2 not in frizez_result[row+1][final_sym_point_col-k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 4 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                        if 4 not in frizez_result[row][final_sym_point_col-k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 8 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                        if 8 not in frizez_result[row-1][final_sym_point_col-k-1]:
                                            is_rotation_sym = False
                                            break
                            #elif (final_sym_point_col-k-1 < 0) and k < repeat_len//2:
 #                                is_rotation_sym = False
                                # break
                    if is_rotation_sym and k >= repeat_len//2:
                        break
        else:
            interval_line_num = len(frizez_result)//2
            #print('1*1', height, len(frizez_result)//2)
            #to find the symmetric point
            for j in range(1, repeat_len//2+1):#1*1
                sym_point_col = j
                is_rotation_sym = True#dont forget it!
                if 1 in frizez_result[interval_line_num][sym_point_col]:
                    if 1 not in frizez_result[interval_line_num+1][sym_point_col]:
                        is_rotation_sym = False
                if 2 in frizez_result[interval_line_num][sym_point_col]:
                    if 2 not in frizez_result[interval_line_num+1][sym_point_col-1]:
                        is_rotation_sym = False
                if 4 in frizez_result[interval_line_num][sym_point_col]:
                    if 4 not in frizez_result[interval_line_num][sym_point_col-1]:
                        is_rotation_sym = False
                #8 is not fine itself for sym point1 in this case, so it is needed to be judged
                if 8 in frizez_result[interval_line_num][sym_point_col]:
                    if 8 not in frizez_result[interval_line_num-1][sym_point_col-1]:
                        is_rotation_sym = False
                if is_rotation_sym:#if these 2 point is symmetric, to judge wether all point are symmetric about them
                    #print('1*1',sym_point_col,len_of_line)
                    final_sym_point_col = sym_point_col+repeat_len
                    #print('1*1',final_sym_point_col)
                    for k in range(0, repeat_len+1):#the range should +1
                        #print('k: ', k)
                        if final_sym_point_col+k < len_of_line and final_sym_point_col-k-1 >= 0:#is there should be <= ????????????
                            for row in range(height):#loop for half height is enough, otherwise it will range out of index
                                if frizez_result[row][final_sym_point_col-k] == [] and frizez_result[-(row+1)][final_sym_point_col+k] == []:
                                    continue
                                #first axis point
                                if 1 in frizez_result[row][final_sym_point_col-k]:
                                    if 1 not in frizez_result[-(row+1)+1][final_sym_point_col+k]:
                                        is_rotation_sym = False
                                        break
                                if 2 in frizez_result[row][final_sym_point_col-k]:
                                    if 2 not in frizez_result[-(row+1)+1][final_sym_point_col+k-1]:
                                        is_rotation_sym = False
                                        break
                                if 4 in frizez_result[row][final_sym_point_col-k]:
                                    if 4 not in frizez_result[-(row+1)][final_sym_point_col+k-1]:
                                        is_rotation_sym = False
                                        break
                                if 8 in frizez_result[row][final_sym_point_col-k]:
                                    if 8 not in frizez_result[-(row+1)-1][final_sym_point_col+k-1]:
                                        is_rotation_sym = False
                                        break
                                #second axis point
                                if 1 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                    if 1 not in frizez_result[row+1][final_sym_point_col-k]:
                                        is_rotation_sym = False
                                        break
                                if 2 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                    if 2 not in frizez_result[row+1][final_sym_point_col-k-1]:
                                        is_rotation_sym = False
                                        break
                                if 4 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                    if 4 not in frizez_result[row][final_sym_point_col-k-1]:
                                        is_rotation_sym = False
                                        break
                                if 8 in frizez_result[-(row+1)][final_sym_point_col+k]:
                                    if 8 not in frizez_result[row-1][final_sym_point_col-k-1]:
                                        is_rotation_sym = False
                                        break
                        #elif (final_sym_point_col-k-1 < 0) and k < repeat_len//2:
 #                           is_rotation_sym = False
 #                          break
                    #print('k: ', is_rotation_sym, k)
                if is_rotation_sym and k >= repeat_len//2:
                    break
            #print('1*1',is_rotation_sym, k)
            if not is_rotation_sym:#1*2
                #print('1*2')
                for j in range(1, repeat_len//2+1):
                    sym_point_1_col = j
                    sym_point_2_col = j+1
                    is_rotation_sym = True#dont forget it!
                    if 1 in frizez_result[interval_line_num][sym_point_1_col]:
                        if 1 not in frizez_result[interval_line_num+1][sym_point_2_col]:
                            is_rotation_sym = False
                    if 2 in frizez_result[interval_line_num][sym_point_1_col]:
                        if 2 not in frizez_result[interval_line_num+1][sym_point_2_col-1]:
                            is_rotation_sym = False
                    if 8 in frizez_result[interval_line_num][sym_point_1_col]:
                        if 8 not in frizez_result[interval_line_num-1][sym_point_2_col-1]:
                            is_rotation_sym = False
                    #4 is fine itself for sym point1, do not need to be judged
                    if 1 in frizez_result[interval_line_num][sym_point_2_col]:
                        if 1 not in frizez_result[interval_line_num+1][sym_point_1_col]:
                            is_rotation_sym = False
                    if 2 in frizez_result[interval_line_num][sym_point_2_col]:
                        if 2 not in frizez_result[interval_line_num+1][sym_point_1_col-1]:
                            is_rotation_sym = False
                    if 8 in frizez_result[interval_line_num][sym_point_2_col]:
                        if 8 not in frizez_result[interval_line_num-1][sym_point_1_col-1]:
                            is_rotation_sym = False
                    if 4 in frizez_result[interval_line_num][sym_point_2_col]:
                        if 4 not in frizez_result[interval_line_num][sym_point_1_col-1]:
                            is_rotation_sym = False
                    if is_rotation_sym:#if these 2 point is symmetric, to judge wether all point are symmetric about them
                        final_sym_point_1_col = sym_point_1_col+repeat_len
                        final_sym_point_2_col = final_sym_point_1_col+1
                        #print('1*2',sym_point_1_col, final_sym_point_1_col)
                        for k in range(0, repeat_len+1):#the range should +1
                            #print('k: ', k)
                            if final_sym_point_2_col+k < len_of_line and final_sym_point_2_col-k-1 >= 0:#is there should be <= ??????
                                for row in range(height):#loop for half height is enough, otherwise it will range out of index
                                    if frizez_result[row][final_sym_point_1_col-k] == [] and frizez_result[-(row+1)][final_sym_point_2_col+k] == []:
                                        continue
                                    #first axis
                                    if 1 in frizez_result[row][final_sym_point_1_col-k]:
                                        #print(11111)
                                        if 1 not in frizez_result[-(row+1)+1][final_sym_point_2_col+k]:
                                            #print(22222)
                                            is_rotation_sym = False
                                            break
                                    if 2 in frizez_result[row][final_sym_point_1_col-k]:
                                        if 2 not in frizez_result[-(row+1)+1][final_sym_point_2_col+k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 4 in frizez_result[row][final_sym_point_1_col-k]:
                                        if 4 not in frizez_result[-(row+1)][final_sym_point_2_col+k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 8 in frizez_result[row][final_sym_point_1_col-k]:
                                        if 8 not in frizez_result[-(row+1)-1][final_sym_point_2_col+k-1]:
                                            is_rotation_sym = False
                                            break
                                    #second axis
                                    if 1 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                        #print(2111)
                                        if 1 not in frizez_result[row+1][final_sym_point_1_col-k]:
                                            #print(2_222)
                                            is_rotation_sym = False
                                            break
                                    if 2 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                        if 2 not in frizez_result[row+1][final_sym_point_1_col-k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 4 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                        if 4 not in frizez_result[row][final_sym_point_1_col-k-1]:
                                            is_rotation_sym = False
                                            break
                                    if 8 in frizez_result[-(row+1)][final_sym_point_2_col+k]:
                                        if 8 not in frizez_result[row-1][final_sym_point_1_col-k-1]:
                                            is_rotation_sym = False
                                            break
                            #elif (final_sym_point_col+k >= len_of_line or final_sym_point_2_col-k-1 < 0) and k < repeat_len//2:
 #                                is_rotation_sym = False
 #                                break
                    #print('1*2 k',is_rotation_sym, k)
                    if is_rotation_sym and k >= repeat_len//2:
                        break
        return is_rotation_sym

    def analyse(self):
        
        is_horizon_reflection = self.is_horizon_sym(self.frizez_result, self.repeat_len)
        is_vertical_reflection = self.is_vertical_sym(self.frizez_result, self.repeat_len)
        is_glid_horizon_reflection = self.is_glid_horizon_sym(self.frizez_result, self.repeat_len)
        is_rotation_reflection = self.is_rotation_sym(self.frizez_result, self.repeat_len)
        flag_list = {'H': is_horizon_reflection, 'G': is_glid_horizon_reflection, 'V': is_vertical_reflection, 'R': is_rotation_reflection}
        str_list = {'H': 'horizontal', 'V': 'vertical', 'G': 'glided horizontal', 'R': 'rotation'}
        true_count = 0
        for k in flag_list:
            if flag_list[k]:
                true_count += 1
        if true_count == 0:
            output_string = 'Pattern is a frieze of period ' + str(self.repeat_len) + ' that is invariant under translation only.'
        elif true_count == 1:
            output_string = 'Pattern is a frieze of period ' + str(self.repeat_len) + ' that is invariant under translation\n        and '
            if flag_list['H']:
                output_string += str_list['H'] + ' reflection only.'
            if flag_list['G']:
                output_string += str_list['G'] + ' reflection only.'
            if flag_list['V']:
                output_string += str_list['V'] + ' reflection only.'
            if flag_list['R']:
                output_string += str_list['R'] + ' only.'
        else:
            output_string = 'Pattern is a frieze of period ' + str(self.repeat_len) + ' that is invariant under translation,\n        '
            if (not is_horizon_reflection) and is_glid_horizon_reflection and is_vertical_reflection and is_rotation_reflection:
                output_string += 'glided horizontal and vertical reflections, and rotation only.'
            if (not is_glid_horizon_reflection) and is_horizon_reflection and is_vertical_reflection and is_rotation_reflection:
                output_string += 'horizontal and vertical reflections, and rotation only.'
        #print('h', is_horizon_reflection)
        #print('v', is_vertical_reflection)
        #print('g', is_glid_horizon_reflection)
        #print('r', is_rotation_reflection)
        
        print(output_string)
            
    def find_last_element(self, k, first_element):#recursively
        for item in self.frizez_dict[k]:
            if item[0] == first_element:
                if len(item[1]) == 2:
                    return item[1]
                else:
                    return self.find_last_element(k, item[1])#dont forget to add return

    def display(self):
        for k in self.frizez_dict:
            point_set = set()
            point_list = []
            for item in self.frizez_dict[k]:#seperate pair of coordinate to single pair
                point_set.add(item[0])#remove repeated coordinate
                point_list.append(item[0])
                point_set.add(item[1])
                point_list.append(item[1])
            for p_s in point_set:#to judge which coordinate is middle one 
                count = 0
                for p_l in point_list:
                    if p_l == p_s:
                        count += 1
                if count > 1:#mark the middle coordinate
                    for item in self.frizez_dict[k]:
                        if item[0] == p_s:
                            item[0] += (count,)
                        elif item[1] == p_s:
                            item[1] += (count,)

        frizez_cp_dict = defaultdict(list)
        frizez_cp_dict = {'N2S':[], 'NW2SE':[], 'W2E':[], 'SW2NE':[]} #record the final pair of coordinate
        for k in self.frizez_dict:#for every draw type
            for item in self.frizez_dict[k]:
                if len(item[0]) == 2 and len(item[1]) == 3:
                    flag = 0#wannna find first element equal to item[1](the last pair of coordinate)
                    temp = item[1]
                    frizez_cp_dict[k].append([item[0],self.find_last_element(k, temp)])#find the last coordinate recursively
                if len(item[0]) == 2 and len(item[1]) == 2:
                    frizez_cp_dict[k].append([item[0],item[1]])

        file_tex_name = 'my_' +self.filename.split('.')[0] + '.tex'
        file_tex = open(file_tex_name, 'w+')
        file_tex.write('\\documentclass[10pt]{article}\n\\usepackage{tikz}\n\\usepackage[margin=0cm]{geometry}\n\\pagestyle{empty}\n\n' +
                       '\\begin{document}\n\n' +
                       '\\vspace*{\\fill}\n\\begin{center}\n\\begin{tikzpicture}[x=0.2cm, y=-0.2cm, thick, purple]\n' +
                       '% North to South lines\n')
        for item in sorted(frizez_cp_dict['N2S']):
            file_tex.write('    \\draw ('+str(item[0][0])+','+str(item[0][1])+') -- ('+str(item[1][0])+','+str(item[1][1])+');\n')
        file_tex.write('% North-West to South-East lines\n')
        for item in sorted(frizez_cp_dict['NW2SE'], key = lambda x: (x[0][1],x[0][0])):
            file_tex.write('    \\draw ('+str(item[0][0])+','+str(item[0][1])+') -- ('+str(item[1][0])+','+str(item[1][1])+');\n')
        file_tex.write('% West to East lines\n')
        for item in sorted(frizez_cp_dict['W2E'], key = lambda x: (x[0][1],x[0][0])):
            file_tex.write('    \\draw ('+str(item[0][0])+','+str(item[0][1])+') -- ('+str(item[1][0])+','+str(item[1][1])+');\n')
        file_tex.write('% South-West to North-East lines\n')
        for item in sorted(frizez_cp_dict['SW2NE'], key = lambda x: (x[0][1],x[0][0])):
            file_tex.write('    \\draw ('+str(item[0][0])+','+str(item[0][1])+') -- ('+str(item[1][0])+','+str(item[1][1])+');\n')
        file_tex.write('\\end{tikzpicture}\n\\end{center}\n\\vspace*{\\fill}\n\n\\end{document}\n')
        file_tex.close()
