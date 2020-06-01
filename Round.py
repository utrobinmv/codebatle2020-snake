from snakebattleclient.internals.Board import Board
from Snake import Snake
from Strateg import Pole

class Round:
    def __init__(self):
        self.time = 0 # Количество пройденных тиков
        self.maxTime = 300 # Количество тиков в раунде
        self.numSnake = 0 # Количество других змеек на поле
        self.numEvilSnake = 0 # Количество злых змеек на поле

        self.snake = Snake()
        self.enemySnake = []

        self.lastCourse = Pole(Board(""))

    def newRound(self):
        self.time = 0
        self.numSnake = 0
        self.snake = Snake()


if __name__ == '__main__':
    raise RuntimeError("This module is not expected to be ran from CLI")