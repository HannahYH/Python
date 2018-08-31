
'''
A max priority queue abstract data type to insert pairs of the form (datum, priority).
If a pair is inserted with a datum that already occurs in the priority queue, then
the priority is (possibly) changed to the (possibly) new value.
'''


class EmptyPriorityQueueError(Exception):
    def __init__(self, message):
        self.message = message


class PriorityQueue():
    min_capacity = 10

    def __init__(self, capacity = min_capacity):
        self.min_capacity = capacity
        self._data = [None] * capacity
        self._length = 0
        self._locations = {}
        # Replace pass above with your code
        
    def __len__(self):#equal to tree's size()
        return self._length
        # Replace pass above with your code

    def is_empty(self):
        return self._length == 0
        # Replace pass above with your code

    def insert(self, element):
        datum = element[0]
        priority = element[1]
        if datum in self._locations:
            self._change_priority(datum, priority)
            return
        if self._length + 1 == len(self._data):
            self._resize(2 * len(self._data))
        self._length += 1
        self._data[self._length] = [datum, priority]
        self._locations[datum] = self._length
        self._bubble_up(self._length)
        # Replace pass above with your code
            
    def delete(self):
        if self.is_empty():
            raise EmptyPriorityQueueError('Cannot delete element from empty priority queue')
        max_element = self._data[1][0]
        del self._locations[max_element]
        self._data[1], self._data[self._length] = self._data[self._length], self._data[1]
        self._length -= 1
        # When the priority queue is one quarter full, we reduce its size to make it half full,
        # provided that it would not reduce its capacity to less than the minimum required.
        if self.min_capacity <= self._length <= len(self._data) // 4:
            self._resize(len(self._data) // 2)
        self._bubble_down(1)
        return max_element
        # Replace pass above with your code

    # Define helper functions
    def _change_priority(self, datum, priority):
        i = self._locations[datum]
        if priority > self._data[i][1]:
            self._data[i][1] = priority
            self._bubble_up(i)
        elif priority < self._data[i][1]:
            self._data[i][1] = priority
            self._bubble_down(i)

    def _bubble_up(self, position):
        if position == 1:
            return
        parent_positon = position // 2
        if self._data[position][1] > self._data[parent_positon][1]:
            self._data[position], self._data[parent_positon] = self._data[parent_positon], self._data[position]
            self._locations[self._data[position][0]] = position
            self._locations[self._data[parent_positon][0]] = parent_positon
            self._bubble_up(parent_positon)

    def _bubble_down(self, position):
        largest_child_position = 2 * position
        if largest_child_position < self._length and self._data[largest_child_position + 1][1] > self._data[largest_child_position][1]:
            largest_child_position += 1
        if largest_child_position <= self._length and self._data[largest_child_position][1] > self._data[position][1]:
            self._data[position], self._data[largest_child_position] = self._data[largest_child_position], self._data[position]
            self._locations[self._data[position][0]] = position
            self._locations[self._data[largest_child_position][0]] = largest_child_position
            self._bubble_down(largest_child_position)

    def _resize(self, new_size):
        self._data = list(self._data[: self._length + 1]) + [None] * (new_size - self._length - 1)

            
