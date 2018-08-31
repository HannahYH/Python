from math import sqrt

def is_prime(N):#ji xia lai
    max_nb=round(sqrt(N))
    for i in range(2,max_nb+1):
        if N%i==0:
            return False
    return True

prime_list = []
sequence_list = []
for i in range(10001, 99998, 2):
    if is_prime(i):
        prime_list.append(i)

for i in range(len(prime_list)-5):
    if prime_list[i]+2==prime_list[i+1] and \
        prime_list[i+1]+4==prime_list[i+2] and \
        prime_list[i+2]+6==prime_list[i+3] and \
        prime_list[i+3]+8==prime_list[i+4] and \
        prime_list[i+4]+10==prime_list[i+5]:
            sequence_list.append([prime_list[i],prime_list[i+1],prime_list[i+2],prime_list[i+3], \
                                 prime_list[i+4],prime_list[i+5]])
print('The solutions are:\n')
for line in sequence_list:
    for i in range(len(line)):
        line[i] = str(line[i])
    print('  '.join(line))
