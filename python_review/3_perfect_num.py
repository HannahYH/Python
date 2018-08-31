# Prompts the user for an integer N and finds all perfect numbers up to N.
# Quadratic complexity, can deal with small values only.


import sys

# Insert your code here
from math import factorial, sqrt

try:
    num = int(input('Input an integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
	
for n in range(2, num + 1):	
    sum_num = 0
    for i in range(1, n):#zhao neng bei zhe ge shu zheng chu de yin zi,jiu shi divisors
        if n % i == 0:
            sum_num += i      
    if sum_num == n:
        print(n, 'is a perfect number.')
