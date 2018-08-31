N = int(input('Enter a nonnegative integer: '))

pascal_triangle = [[1]]
pascal_triangle += [[1,1]]

for i in range(2, N):
    pascal_triangle += [[]]
    pascal_triangle[-1].append(1)
    for j in range(i-1):
        pascal_triangle[-1].append(pascal_triangle[-2][j]+pascal_triangle[-2][j+1])
    pascal_triangle[-1].append(1)

space = len(str(max(pascal_triangle[-1])))
for n in range(N):
    print(' ' * space * (N-n), end='')
    for k in range(n):
        print(f'{pascal_triangle[n][k]:{space}d}', end='')
        print(' ' * space, end='')
    print(f'{pascal_triangle[n][-1]:{space}d}')


