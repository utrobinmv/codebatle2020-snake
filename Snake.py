class Snake:
    def __init__(self):
        self.x = 0 # Координат X змеи
        self.y = 0 # Координат Y змеи
        self.SnakeEvil = 0 # Змея злая
        self.SnakeEvilStep = 0 # Количество остатка ходов ярости
        self.head = 0 # В какую сторону поворот головы
        self.slep = 0 # Змея спит или умерла
        self.Length = 0 #Длина змеи
        self.nearFury = []
        self.goto_TAIL = 0
        self.nextXY = []
        self.coordinates = [] #Координаты змеи от головы к хвосту

        self.EnemyLength = 0 #Длина остальных змей
        self.otherSnakeEvil = 0 #Если есть на поле другая злая змейка
        
    def copySnake(self, receiver):
       receiver.x = self.x
       receiver.y = self.y
       receiver.SnakeEvil = self.SnakeEvil # Змея злая
       receiver.SnakeEvilStep = self.SnakeEvilStep # Количество остатка ходов ярости
       receiver.head = self.head # В какую сторону поворот головы
       receiver.Length = self.Length #Длина змеи

       for i in range(len(self.nearFury)):
           receiver.nearFury.append(self.nearFury[i])

       for i in range(len(self.nextXY)):
           receiver.nextXY.append(self.nextXY[i])



if __name__ == '__main__':
    raise RuntimeError("This module is not expected to be ran from CLI")