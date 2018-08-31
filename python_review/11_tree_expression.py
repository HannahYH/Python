
import re

from stack_adt import Stack, EmptyStackError
from binary_tree_adt import BinaryTree


'''
Uses the Stack and BinaryTree interfaces to build an expression tree and evaluate
an arithmetic expression written in infix, fully parenthesised with parentheses,
brackets and braces, and built from natural numbers using the binary +, -, * and / operators.
'''
def parse_tree(expression):#equal to evaluate(expression)#below are my code
    if any(not (c.isdigit() or c.isspace() or c in '+-*/(){}[]') for c in expression):
        return
    tokens = re.compile('(\d+|\+|-|\*|/|\(|\)|\[|\]|\{|\})').findall(expression)
    try:
        value = parse_expression(tokens)
        return value
    except ZeroDivisionError:
        return 
def parse_expression(tokens):#equal to evaluate_expression(tokens)#below are my code
    parenthese = {')':'(','}':'{',']':'['}
    stack = Stack()
    for token in tokens:
        try:
            token = BinaryTree(int(token))
        except ValueError:
            pass
        if token not in parenthese:
            stack.push(token)
        else:
            try:
                arg_2 = stack.pop()
                operater = stack.pop()
                arg_1 = stack.pop()
                former = stack.pop()
                if parenthese[token] == former:
                    my_tree = BinaryTree(operater)
                    my_tree.left_node = arg_1
                    my_tree.right_node = arg_2
                    stack.push(my_tree)
                else:
                    return
            except EmptyStackError:
                return
    if stack.is_empty():
        return
    my_tree = stack.pop()
    if not stack.is_empty():
        return
    return my_tree


if __name__ == '__main__':
    import doctest
    doctest.testmod()
