__author__ = 'liscju'

class GridInfo:
    def __init__(self, size, conductor_x_pos, conductor_y_pos, conductor_size, conductor_value):
        self.size = size
        self.conductor_x_pos = conductor_x_pos
        self.conductor_y_pos = conductor_y_pos
        self.conductor_size = conductor_size
        self.conductor_value = conductor_value

    def get_size(self):
        return self.size
    
    def get_conductor_value(self):
        return self.conductor_value

    def is_border_point(self, x, y):
        return y == 0 or y == self.size - 1 or \
               x == 0 or x == self.size - 1

    def is_conductor_point(self, x, y):
        return self.conductor_x_pos <= x < self.conductor_x_pos + self.conductor_size and \
            self.conductor_y_pos <= y < self.conductor_y_pos + self.conductor_size