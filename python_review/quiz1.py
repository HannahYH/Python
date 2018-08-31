
import sys
from random import seed, randint


try:
    arg_for_seed, upper_bound, length = input('Enter three nonnegative integers: ').split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, upper_bound, length = int(arg_for_seed), int(upper_bound), int(length)
    if arg_for_seed < 0 or upper_bound < 0 or length < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()

seed(arg_for_seed)
L = [randint(0, upper_bound) for _ in range(length)]
print('\nThe generated list L is:')
print('  ', L)

L_1 = []
L_2 = []
L_3 = []
elements_to_keep = []

L2 = sorted(list(set(L)))
elements_to_keep = L2[::2]

for e in L:
    if e in elements_to_keep:
        L_1.append(e)

for e in L:
    if (e in elements_to_keep) and (e not in L_2):
        L_2.append(e)

def is_consecutive(L):
    LL = sorted(list(set(L)))
    for i in range(len(LL)-1):#zhu yi bian jie -1
        if LL[i+1] != LL[i] + 1:
            return False
    return True

consecutive_sublists = []
for i in range(len(L)):
    for j in range(i+1, len(L)+1):#zhu yi bian jie
        if is_consecutive(L[i:j]):
            consecutive_sublists.append(L[i:j])

if consecutive_sublists != []:
    L_3 = consecutive_sublists[0]
    for i in range(1, len(consecutive_sublists)):
        if len(L_3) < len(consecutive_sublists[i]):
            L_3 = consecutive_sublists[i]

print('\nThe elements to keep in L_1 and L_2 are:')
print('  ', elements_to_keep)
print('\nHere is L_1:')
print('  ', L_1)
print('\nHere is L_2:')
print('  ', L_2)
print('\nHere is L_3:')
print('  ', L_3)

##length = len(L)
##if L:
##    while not L_3:
##        for start in range(len(L) - length + 1):
##            candidate_list = L[start: start + length]
##            candidate_set = set(candidate_list)
##            if max(candidate_set) - min(candidate_set) == len(candidate_set) - 1:
##                L_3 = candidate_list
##                break
##        length -= 1
