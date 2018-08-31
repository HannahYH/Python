characters_triangle_list = [[65]]
characters_triangle_list
N = int(input('Enter strictly positive number: '))

A_code = 65
start_num = 64
for i in range(N):
    print(' '*(N-1-i), end='')
    for j in range(start_num+1, start_num+i+2):
        chr_ch = j
        while chr_ch > 90:
            chr_ch -= 26
        print(chr(chr_ch), end='')
        
    for k in range(start_num+i, start_num, -1):
        chr_ch = k
        while chr_ch > 90:
            chr_ch -= 26
        print(chr(chr_ch), end='')
    print()
    start_num += i+1
