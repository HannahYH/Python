from linked_list_adt import *

class ExtendedLinkedList(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def remove_duplicates(self):
        if not self.head:
            return
        first_appeared_node = self.head
        while first_appeared_node:
            node = first_appeared_node
            while node.next_node:
                if node.next_node.value == first_appeared_node.value:
                    node.next_node = node.next_node.next_node
                else:
                    node = node.next_node
            first_appeared_node = first_appeared_node.next_node

#hen bang !
class ExtendedLinkedList2(LinkedList):
    def __init__(self, L = None):
        super().__init__(L)

    def remove_duplicates(self):
        if self.head is None:
            return
        node_set = set()
        node = self.head
        node_set.add(node.value)
        while node.next_node:
            if node.next_node.value not in node_set:
                node_set.add(node.next_node.value)
                node = node.next_node
            else:
                node.next_node = node.next_node.next_node
                
