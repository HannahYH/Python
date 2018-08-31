# Randomly generates a binary search tree whose number of nodes
# is determined by user input, with labels ranging between 0 and 999,999,
# displays it, and outputs the maximum difference between consecutive leaves.
#
# Written by *** and Eric Martin for COMP9021

import sys
from random import seed, randrange
from binary_tree_adt import *

# Possibly define some functions
leaves_list = []
def traversal_tree(tree):
    global leaves_list
    if tree.value is None:
        return []
    if tree.left_node.value is None and tree.right_node.value is None:
        leaves_list.append(tree.value)
    traversal_tree(tree.left_node)
    traversal_tree(tree.right_node)
    return leaves_list

def max_diff_in_consecutive_leaves(tree):
    leaves_list = traversal_tree(tree)
    difference_list = []
    if leaves_list and len(leaves_list) > 1:
        for i in range(len(leaves_list)-1):
            difference_list.append(leaves_list[i+1]-leaves_list[i])
        return max(difference_list)
    else:
        return 0


provided_input = input('Enter two integers, the second one being positive: ')
try:
    arg_for_seed, nb_of_nodes = provided_input.split()
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
try:
    arg_for_seed, nb_of_nodes = int(arg_for_seed), int(nb_of_nodes)
    if nb_of_nodes < 0:
        raise ValueError
except ValueError:
    print('Incorrect input, giving up.')
    sys.exit()
seed(arg_for_seed)
tree = BinaryTree()
for _ in range(nb_of_nodes):
    datum = randrange(1000000)
    tree.insert_in_bst(datum)
print('Here is the tree that has been generated:')
tree.print_binary_tree()
print('The maximum difference between consecutive leaves is: ', end = '')
print(max_diff_in_consecutive_leaves(tree))
