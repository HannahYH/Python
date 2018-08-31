
'''
Dispatches the integers from 0 to 8, with 0 possibly changed to None,
as a list of 3 lists of size 3, to represent a 9 puzzle.
For instance, [[4, 0, 8], [1, 3, 7], [5, 2, 6]] or [[4, None ,8], [1, 3, 7], [5, 2, 6]]
represents the 9 puzzle   4     8
                          1  3  7
                          5  2  6
with the 8 integers being printed on 8 tiles that are placed in a frame
with one location being tile free.
The aim is to slide tiles horizontally or vertically
so as to eventually reach the configuration
                          1  2  3
                          4  5  6
                          7  8
It can be shown that the puzzle is solvable iff the permutation of
the integers 1,..., 8, determined by reading those integers off the puzzle
from top to bottom and from left to right, is even.
This is clearly a necessary condition since:
- sliding a tile horizontally does not change the number of inversions;
- sliding a tile vertically changes the number of inversions by -2, 0 or 2;
- the parity of the identity is even.

'''


from itertools import chain
from collections import deque

def validate_9_puzzle(grid):
    grid_t = []
    have_0 = False
    for line in grid:
        for e in line:
            if e is None or e == 0:
                have_0 = True
                grid_t.append(0)
            else:
                grid_t.append(e)
    move_step = 0
    if have_0:
        for i in range(len(grid_t)):
            for j in range(i+1, len(grid_t)):
                if grid_t[j] != 0 and grid_t[i] > grid_t[j]:
                    move_step += 1

    if have_0 and move_step % 2 == 0:
        print('This is a valid 9 puzzle, and it is solvable')
    else:
        print('This is an invalid or unsolvable 9 puzzle')

