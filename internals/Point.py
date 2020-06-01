class Point:
    """ Describes a point on board."""
    def __init__(self, x=0, y=0):
        self._x = int(x)
        self._y = int(y)
    
    def __key(self):
        return self._x, self._y

    def __str__(self):
        return self.to_string()

    def __repr__(self):
        return self.to_string()

    def __eq__(self, other_point):
        return self.__key() == other_point.__key()

    def __hash__(self):
        return hash(self.__key())

    def get_x(self):
        return self._x

    def get_y(self):
        return self._y

    def to_string(self):
        return "[{},{}]".format(self._x, self._y)

    # Returns new BoardPoint object shifted bottom "delta" points
    def shift_bottom(self, delta):
        return Point(self._x, self._y + delta)

    # Returns new BoardPoint object shifted bottom 1 point ???? надо ли todo
    def shift_bottom(self):
        return self.shift_bottom(self, 1)

    # Returns new BoardPoint object shifted top "delta" points
    def shift_top(self, delta):
        return Point(self._x, self._y - delta)

    # Returns new BoardPoint object shifted top 1 point
    def shift_top(self):
        return self.shift_top(self, 1)

    # Returns new BoardPoint object shifted right to "delta" points
    def shift_right(self, delta):
        return Point(self._x + delta, self._y)

    # Returns new BoardPoint object shifted right to 1 point
    def shift_right(self):
        return self.shift_right(self, 1)

    # Returns new BoardPoint object shifted left to "delta" points
    def shift_left(self, delta):
        return Point(self._x - delta, self._y)

    # Returns new BoardPoint object shifted left to 1 point
    def shift_left(self):
        return self.shift_left(1)

    # Checks is current point on board or out of range.
    # @param boardSize Board size to compare
    def is_out_of_board(self, board_size):
        return self._x >= board_size or self._y >= board_size or self._x < 0 or self._y < 0

if __name__ == '__main__':
    raise RuntimeError("This module is not expected to be ran from CLI")