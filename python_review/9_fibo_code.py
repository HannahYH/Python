def encode(n):
    fibo_list = fibonacci_numbers_up_to_n(n+1)
    code = ''
    for e in reversed(fibo_list[2:]):
        if n >= e:
            code += '1'
            n -= e
        else:
            code += '0'
    for i in range(len(code)):
        if code[i] == '1':
            print(''.join(reversed(code[i:]))+'1')
            break


def decode(code):
    if code[-1] != '1':
        return 0
    if '11' in code[:-1]:
         return 0
    fibo_list = fibonacci_numbers_up_to_n(len(code))
    num = 0
    print(fibo_list)
    for i in range(len(code)-1):
        if code[i] == '1':
            num += fibo_list[i+2]
    print(num)
    

def fibonacci_numbers_up_to_n(n):
    fibo_list = []
    fibo_list.append(0)
    fibo_list.append(1)
    for _ in range(2, n+1):
        fibo_list.append(fibo_list[-1] + fibo_list[-2])
    return fibo_list
