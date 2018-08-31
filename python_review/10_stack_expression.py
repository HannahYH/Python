'''
Uses the Stack interface to evaluate an arithmetic expression written in postfix
and built from natural numbers using the binary +, -, * and / operators.             
'''
import re
from operator import add, sub, mul, truediv
from stack_adt import Stack, EmptyStackError
def evaluate(expression):
    if any(not (c.isdigit() or c.isspace() or c in '+-*/(){}[]') for c in expression):
        return
    # Tokens can be natural numbers, +, -, *, and /
    tokens = re.compile('(\d+|\+|-|\*|/|\(|\)|\[|\]|\{|\})').findall(expression)
    try:
        value = evaluate_expression(tokens)
        return value
    except ZeroDivisionError:
        return
def evaluate_expression(tokens):
    stack = Stack()
    parenthese = {')': '(', ']': '[', '}': '{'}
    for token in tokens:
        try:
            token = int(token)
        except ValueError:
            pass
        if token not in parenthese:
            stack.push(token)
        else:
            try:
                arg_2 = stack.pop()
                operator = stack.pop()
                arg_1 = stack.pop()
                former = stack.pop()
                if parenthese[token] == former:
                    stack.push({'+': add, '-': sub, '*': mul, '/': truediv}[operator](arg_1, arg_2))
                else:
                    return
            except EmptyStackError:
                return
    if stack.is_empty():
        return
    value = stack.pop()
    if not stack.is_empty():
        return
    return value
        




##
##
##
##'''
##Uses the Stack interface to evaluate an arithmetic expression written in postfix
##and built from natural numbers using the binary +, -, * and / operators.             
##'''
##
##
##import re
##from operator import add, sub, mul, truediv
##
##from stack_adt import Stack, EmptyStackError
##
##
##def evaluate(expression):
##    if any(not (c.isdigit() or c.isspace() or c in '(){}[]+-*/') for c in expression):
##        return
##    # Tokens can be natural numbers, +, -, *, and /
##    tokens = re.compile('(\d+|\+|-|\*|/|\]|\[|\}|\{|\(|\))').findall(expression)
##    #print(tokens)
##    try:
##        value = evaluate_expression(tokens)
##        return value
##    except ZeroDivisionError:
##        return
##
##def evaluate_expression(tokens):
##    kinds_of_parenthese = {')':'(', ']':'[', '}':'{'}
##    stack = Stack()
##    stack_of_parenthese = Stack()
##    for token in tokens:
##        try:
##            if token in '([{':
##                stack_of_parenthese.push(token)
##            elif token in ')]}':
##                #if ) top of stack should contain (
##                #if ] top of stack should contain [
##                #if } top of stack should contain {
##                try:
##                    if kinds_of_parenthese[token] != stack_of_parenthese.pop():#pop corresponding opening bracket from stack
##                        return False
##                except EmptyStackError:
##                    return False
##                
##                try:
##                    arg_3 = stack.pop()
##                    arg_2 = stack.pop()
##                    arg_1 = stack.pop()
##                    #print(arg_3,arg_2,arg_1)
##                    if (str(arg_1) in {'+','-','*','/'}) or (str(arg_3) in {'+','-','*','/'}):
##                        return
##                    else:
##                        stack.push({'+': add, '-': sub, '*': mul, '/': truediv}[arg_2](arg_1, arg_3))
##                except EmptyStackError:
##                    return
##                
##            else:
##                if token in {'+','-','*','/'}:
##                    stack.push(token)
##                else:
##                    token = int(token)#must transfer it in there, cos the mid-result would be a float number
##                    stack.push(token)
##        except ValueError:
##            return
##    if stack.is_empty() and stack_of_parenthese.is_empty():
##        return
##    value = stack.pop()
##    if not stack.is_empty():
##        return
##    return value
##
##
##if __name__ == '__main__':
##    import doctest
##    doctest.testmod()
