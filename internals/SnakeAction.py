from enum import Enum


class SnakeAction(Enum):
    LEFT = 'left'
    RIGHT = 'right'
    UP = 'up'
    DOWN = 'down'
    STOP = 'stop'
    ACT_LEFT = 'act,left'
    ACT_RIGHT = 'act,right'
    ACT_UP = 'act,up'
    ACT_DOWN = 'act,down'
