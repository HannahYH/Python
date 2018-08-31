# Prompts the user to input an integer N at least equal to 10 and computes N!
# in three different ways.


import sys
from math import factorial

# Insert your code here
try:
    factor = int(input('Input a nonnegative integer: '))
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    if factor <= 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

# method 1
num_of_zero_1 = 0
factorial_num = factorial(factor)
while not factorial_num % 10:
    num_of_zero_1 += 1
    factorial_num //= 10
        
# method 2
num_of_zero_2 = 0
factorial_num = factorial(factor)
for e in reversed(str(factorial_num)):
    if e == '0':
        num_of_zero_2 += 1
    else:
        break
        
# method 3
num_of_zero_3 = 0
i = 1
while pow(5, i) < factor:
    power = pow(5, i)
    for j in range(power, factor+1, 1):
        if j % power == 0:
            num_of_zero_3 += 1
    i += 1
    
print(f'Computing the number of trailing 0s in {factor}! by dividing by 10 for long enough:',
      num_of_zero_1)
print(f'Computing the number of trailing 0s in {factor}! by converting it into a string:',
      num_of_zero_2)
print(f'Computing the number of trailing 0s in {factor}! the smart way:',
      num_of_zero_3)
