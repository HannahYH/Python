from random import seed, randint


# Prompts the user for a seed for the random number generator,
# and for a strictly positive number, nb_of_elements.
arg_for_seed = input('Input a seed for the random number generator: ')
try:
    arg_for_seed = int(arg_for_seed)
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()   
nb_of_elements = input('How many elements do you want to generate? ')
try:
    nb_of_elements = int(nb_of_elements)
except ValueError:
    print('Input is not an integer, giving up.')
    sys.exit()
if nb_of_elements <= 0:
    print('Input should be strictly positive, giving up.')
    sys.exit()
# Generates a list of nb_of_elements random integers between 0 and 99.
seed(arg_for_seed)
L = [randint(0, 99) for _ in range(nb_of_elements)]
# Prints out the list, computes the maximum element of the list, and prints it out.
print('\nThe list is:', L)

max_num = L[0]
min_num = L[0]
for item in L:
    if item > max_num:
        max_num = item
    if item < min_num:
        min_num = item

print(max_num, max(L))
print(max_num-min_num, max(L)-min(L))
