# Decodes all multiplications of the form
#
#                        *  *  *
#                   x       *  *
#                     ----------
#                     *  *  *  *
#                     *  *  *
#                     ----------
#                     *  *  *  *
#
# such that the sum of all digits in all 4 columns is constant.

# Insert your code here.
for i in range(100, 1000):
    for j in range(10, 100):
        if i * j > 1000 and i * j < 10000:
            result1 = i * (j % 10)
            if result1 >= 1000:
                result2 = i * (j // 10)
                if result2 < 1000:
                    str_1 = str('0'+str(i))
                    str_2 = str('00'+str(j))
                    str_3 = str(result1)
                    str_4 = str(result2*10)
                    str_5 = str(i*j)
                int_1 = int(str_1[0]) + int(str_2[0]) + int(str_3[0]) + int(str_4[0]) + int(str_5[0])
                int_2 = int(str_1[1]) + int(str_2[1]) + int(str_3[1]) + int(str_4[1]) + int(str_5[1])
                int_3 = int(str_1[2]) + int(str_2[2]) + int(str_3[2]) + int(str_4[2]) + int(str_5[2])
                int_4 = int(str_1[3]) + int(str_2[3]) + int(str_3[3]) + int(str_4[3]) + int(str_5[3])
                if int_1 == int_2 == int_3 == int_4:
                    print(f'{i} * {j} = {i*j}, all columns adding up to {int_1}.')
        else:
            break		
