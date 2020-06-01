from math import sqrt

from snakebattleclient.internals.Element import Element
from snakebattleclient.internals.Point import Point


class Board:
    """ Class describes the Board field for Bomberman game."""

    def __init__(self, board_string):
        self._string = board_string.replace('\n', '')
        self._len = len(self._string)  # the length of the string
        self._size = int(sqrt(self._len))  # size of the board

    def get_point_by_shift(self, shift):
        return Point(shift % self._size, shift / self._size)

    def find_first_element(self, *element_types):
        _result = []
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            for type in element_types:
                if self.has_element_at(point, type):
                    return point
        return None

    def get_my_head(self):
        return self.find_first_element(Element('HEAD_DOWN'), Element('HEAD_UP'),
                                       Element('HEAD_LEFT'), Element('HEAD_RIGHT'), Element('HEAD_EVIL'),
                                       Element('HEAD_FLY'), Element('HEAD_SLEEP'))

    def _find_all(self, *element_types):
        """ Returns the list of points for the given element type."""
        _points = []
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            for type in element_types:
                if self.has_element_at(point, type):
                    _points.append(point)
        return _points

    def get_walls(self):
        return self._find_all(Element('WALL'))

    def get_stones(self):
        return self._find_all(Element('STONE'))

    def get_barriers(self):
        """ Return the list of barriers Points."""
        points = set()
        points.update(self._find_all(Element('WALL'), Element('START_FLOOR'), Element('ENEMY_HEAD_SLEEP'),
                                     Element('ENEMY_TAIL_INACTIVE'), Element('TAIL_INACTIVE'), Element('STONE')))
        return list(points)

    def is_barrier_at(self, point):
        return self.get_barriers().__contains__(point)

    def get_apples(self):
        return self._find_all(Element('APPLE'))

    def am_i_evil(self):
        return self._find_all(Element('HEAD_EVIL')).__contains__(self.get_my_head())

    def am_i_flying(self):
        return self._find_all(Element('HEAD_FLY')).__contains__(self.get_my_head())

    def get_flying_pills(self):
        return self._find_all(Element('FLYING_PILL'))

    def get_furry_pills(self):
        return self._find_all(Element('FURY_PILLS'))

    def get_gold(self):
        return self._find_all(Element('GOLD'))

    def get_start_points(self):
        return self._find_all(Element('START_FLOOR'))

    def get_element_at(self, point):
        """ Return an Element object at coordinates x,y."""
        return Element(self._string[self._xy2strpos(point.get_x(), point.get_y())])

    def has_element_at(self, point, element_object):
        if point.is_out_of_board(self._size):
            return False
        return element_object == self.get_element_at(point)

    def find_element(self, type):
        for i in range(self._size * self._size):
            point = self.get_point_by_shift(i)
            if self.has_element_at(point, type):
                return point
        return None

    def get_shift_by_point(self, point):
        return point.get_y() * self._size + point.get_x()

    def _strpos2pt(self, strpos):
        return Point(*self._strpos2xy(strpos))

    def _strpos2xy(self, strpos):
        return (strpos % self._size, strpos // self._size)

    def _xy2strpos(self, x, y):
        return self._size * y + x

    def print_board(self):
        # f = 1
        print(self._line_by_line())

    def _line_by_line(self):
        return '\n'.join([self._string[i:i + self._size]
                          for i in range(0, self._len, self._size)])

    def to_string(self):
        return ("Board:\n{brd}".format(brd=self._line_by_line()))


if __name__ == '__main__':
    raise RuntimeError("This module is not designed to be ran from CLI")
