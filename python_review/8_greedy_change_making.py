import sys

amount = int(input('Input the desired amount: '))

count = {'100': 0, '50': 0, '20': 0, '10': 0, '5': 0, '2': 0, '1': 0}

sum_count = 0
for k in count:
    if amount // int(k) != 0:
        count[k] = amount // int(k)
        amount %= int(k)
        sum_count += count[k]
print()
if sum_count == 1:
    print('1 banknote is needed.')
elif sum_count > 1:
    print(f'{sum_count} banknotes are needed.')
print('The detail is:')
for k in count:
    if count[k] != 0:
        print(' '*(3-len(k)), end='')
        print(f'${k}: {count[k]}')
