from math import sqrt

class PointError(Exception):
    def __init__(self, message):
        self.message = message

class Point():
    def __init__(self, x = None, y = None):
        if x is None and y is None:
            self.x = 0
            self.y = 0
        elif x and y:
            self.x = x
            self.y = y
        else:
            raise PointError('Need two coordinates, point not created.')


class TriangleError(Exception):
    def __init__(self, message):
        self.message = message

class Triangle():
    def __init__(self, *, point_1, point_2, point_3):
        if 
