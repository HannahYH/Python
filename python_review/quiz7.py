from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def rearrange(self):
        old_head_node = self.head
        node = self.head
        smallest_node = self.head
        while node and node.next_node:
            if smallest_node.value > node.next_node.value:
                smallest_node = node.next_node
            node = node.next_node
        node.next_node = old_head_node
        node = old_head_node
        while True:
            if node.next_node.value == smallest_node.value:
                break
            else:
                node = node.next_node
                
        self.head = node.next_node
        flag_id = id(node)
        while id(node.next_node.next_node) != flag_id:
            forward_node = node.next_node.next_node
            node.next_node.next_node = node
            node.next_node = forward_node.next_node
            node = forward_node

        #forward_node = node.next_node.next_node
        node.next_node.next_node = node
        node.next_node = None
