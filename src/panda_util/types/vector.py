from collections import namedtuple

class Vector(namedtuple('Vector', ['x', 'y'])):
    def __new__(cls, x, y):
        return super().__new__(cls, x, y)
    
    def __str__(self):
        return f"Vector({self.x}, {self.y})"
    
