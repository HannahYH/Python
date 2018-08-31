# Given a positive integer n, a magic square of order n is a matrix of size n x n
# that stores all numbers from 1 up to n^2 and such that the sum of the n rows,
# the sum of the n columns, and the sum of the two diagonals is constant,
# hence equal to n(n^2+1)/2.
	
def print_square(grid):
    for line in grid:
        for e in line[:-1]:
            print(str(e) + ' ', end='')
        print(line[-1])

def is_magic_square(grid):
    n = len(grid)
    sum_rows = []
    sum_columns = []
    sum_diagonal1 = 0
    sum_diagonal2 = 0

    for i in range(n):
        sum_rows.append(sum(grid[i]))
        sum_diagonal1 += grid[i][i]
        sum_diagonal2 += grid[i][n-i-1]

    for j in range(n):
        sum_columns.append(0)
        for i in range(n):
            sum_columns[j] += grid[i][j]

    is_magic = True
    if sum_diagonal1 == sum_diagonal2:
        for i in range(n):
            if sum_rows[i] != sum_diagonal1 or sum_columns[i] != sum_diagonal1:
                is_magic = False
                break

    print(is_magic)
