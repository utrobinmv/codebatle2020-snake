from snakebattleclient.internals.Board import Board
from snakebattleclient.internals.Element import Element
from snakebattleclient.internals.SnakeAction import SnakeAction
from snakebattleclient.internals.Point import Point
import numpy as np

from Snake import Snake
import datetime

from operator import itemgetter

# from Round import Round

import Mapping

import Constants

snake = Snake()
enemySnakes = []

debug = 0

def debugInfo(num):
    if debug != 0:
        print("debug = " + num.__str__())

# class Shadow:
#     def __init__(self):

#         # Слой расчета траектории
#         self._shadow = []
#         self._size = 0

#     def shadowInit(self, size):
#         self._shadow = []
#         self._size = size
#         for n in range(self._size * self._size):
#             self._shadow.append(0)

#     def shadowCopy(self, arr):
#         arr.clear()
#         for n in range(self._size * self._size):
#             arr[n] = self._shadow[n]


#     def shadowGetPos(self, x, y):
#         return self._shadow[x + y * self._size]

#     def shadowSetPos(self, x, y, value):
#         self._shadow[x + y * self._size] = value

#     def printShadow(self):
#         str = "\n"
#         for y in range(0, self._size):
#             for x in range(0, self._size):
#                 num = self._shadow[x + y * self._size]
#                 # numWall = pole._background[x + y * self._size]
#                 # if self.snake.x == x and self.snake.y == y:
#                 #     num_str = "@@@"
#                 # elif numWall == Constants.BACKGROUND_WALL:
#                 #     num_str = "###"
#                 if num == 0:
#                     num_str = "   "
#                 elif num > -10 and num < 0:
#                     num_str = " " + num.__str__()
#                 elif num < -99:
#                     num_str = "***"
#                 elif num <= -10:
#                     num_str = "" + num.__str__()
#                 elif num > 0 and num < 10:
#                     num_str = "  " + num.__str__()
#                 elif num > 9 and num < 100:
#                     num_str = " " + num.__str__()
#                 else:        
#                     num_str = num.__str__()
#                 str = str + num_str
#             str = str + '\n'
#         print(str)

class Round:
    def __init__(self):
        self.time = 0 # Количество пройденных тиков
        self.maxTime = 300 # Количество тиков в раунде

        self.snake = Snake()
        self.enemySnakes = []
        self.mode = 0

        self.lastCourse = Pole(Board(""))

    def newRound(self):
        self.time = 0
        self.mode = 0
        self.snake = Snake()
        self.enemySnakes = []

class Pole(Board):
    def __init__(self, brd: Board):
        self._string = brd._string
        self._len = brd._len
        self._size = brd._size

        self.time = 0        

        self.snake = Snake() #Моя змея
        self.enemySnake = [] #Объекты голов других змеек

        self.furyPill = [] #Координаты бутылок ярости

        self.stones = [] #Координаты камней
        self.apples = [] #Координаты яблок
        self.golds = [] #Координаты золота

        # Слой физических стен
        self._background = []
        for n in range(self._len + self._size):
            self._background.append(0)

        # Слой очков за клетку
        self._shores = []
        for n in range(self._len + self._size):
            self._shores.append(0)

        # Слой очков Зла за клетку
        self._shoresEvil = []
        for n in range(self._len + self._size):
            self._shoresEvil.append(0)

        # Слой объектов
        self._elements = []
        for n in range(self._len + self._size):
            self._elements.append(0)

        # Слой выбранной траектории движения
        self._trajectory = []
        for n in range(self._len + self._size):
            self._trajectory.append(0)

        # Слой расчета траектории
        self._shadow = []

        self._timeStart = 0


        self._map = []
        self._mapFind = []
        self._stone_x = 0
        self._stone_y = 0

        self.numSnake = 0 # Количество других змеек на поле
        self.numEvilSnake = 0 # Количество злых змеек на поле

        for n in range(self._len + self._size):
            self._map.append(0)

        for n in range(self._len + self._size):
            self._mapFind.append(0)

    def timeStart(self):
        self._timeStart = datetime.datetime.now()

    def timeFinish(self, name):
        timeFinish = datetime.datetime.now()
        raznica = timeFinish - self._timeStart

        print(name + "Start " + self._timeStart.__str__() + ", finish " + timeFinish.__str__() + " === " + raznica.microseconds.__str__()) 
    
 
    def fill(self):  # Данная процедура уже может подлежать оптимизации

        debugInfo(97)

        for x in range(0, self._len // self._size):
            for y in range(0, self._size):
                el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))._char

                if el == Constants.NONE:
                    continue
                
                #Заполнение Стен
                elif el == Constants.WALL or el == Constants.ENEMY_HEAD_DEAD:
                    self.backgroundSetPos(x, y, Constants.BACKGROUND_WALL)
                    self.elementsSetPos(x, y, Constants.WALL)
                
                elif (el == Constants.START_FLOOR or el == Constants.OTHER
                 or el == Constants.ENEMY_TAIL_INACTIVE or el == Constants.TAIL_INACTIVE
                 or el == Constants.ENEMY_HEAD_SLEEP or el == Constants.HEAD_SLEEP):
                    self.backgroundSetPos(x, y, Constants.BACKGROUND_WALL)
                    self.elementsSetPos(x, y, Constants.WALL)

                #Заполнение Элементов
                elif el == Constants.APPLE:
                    self.elementsSetPos(x, y, Constants.APPLE)
                elif el == Constants.STONE:
                    self.elementsSetPos(x, y, Constants.STONE)
                elif el == Constants.FURY_PILL:
                    self.elementsSetPos(x, y, Constants.FURY_PILL)
                elif el == Constants.GOLD:
                    self.elementsSetPos(x, y, Constants.GOLD)

                # Для меня моего хвоста не существует, так как зайдя на него я никак не смогу наткнуться на яблоко
                # elif (el == Constants.TAIL_END_DOWN or el == Constants.TAIL_END_UP
                #   or el == Constants.TAIL_END_DOWN or el == Constants.TAIL_END_UP):
                #     self.elementsSetPos(x, y, Constants.TAIL_INACTIVE) # Мой хвост на карте

                #Заполнение хвоста для неточно, так как нужно определить есть ли перед головой яблоко
                #Если оно есть, то хвост на следующем ходе не пропадет, в противном случае его отображать не нужно
                elif (el == Constants.HEAD_DOWN or el == Constants.HEAD_LEFT
                  or el == Constants.HEAD_RIGHT or el == Constants.HEAD_UP
                  or el == Constants.HEAD_EVIL or el == Constants.BODY_HORIZONTAL
                  or el == Constants.BODY_VERTICAL or el == Constants.BODY_LEFT_DOWN
                  or el == Constants.BODY_LEFT_UP or el == Constants.BODY_RIGHT_DOWN
                  or el == Constants.BODY_RIGHT_UP or el == Constants.HEAD_DEAD):
                    self.elementsSetPos(x, y, Constants.SNAKE_BODY) # Хвост противника на карте

                elif (el == Constants.ENEMY_TAIL_END_DOWN or el == Constants.ENEMY_TAIL_END_LEFT
                  or el == Constants.ENEMY_TAIL_END_UP or el == Constants.ENEMY_TAIL_END_RIGHT):
                    self.elementsSetPos(x, y, Constants.ENEMY_TAIL) # Хвост противника на карте

                elif (el == Constants.ENEMY_HEAD_DOWN or el == Constants.ENEMY_HEAD_LEFT
                  or el == Constants.ENEMY_HEAD_RIGHT or el == Constants.ENEMY_HEAD_UP
                  or el == Constants.ENEMY_HEAD_EVIL):
                    self.elementsSetPos(x, y, Constants.ENEMY_HEAD) # Голова противника на карте

                elif (el == Constants.ENEMY_BODY_HORIZONTAL or el == Constants.ENEMY_BODY_VERTICAL
                  or el == Constants.ENEMY_BODY_LEFT_DOWN or el == Constants.ENEMY_BODY_LEFT_UP
                  or el == Constants.ENEMY_BODY_RIGHT_DOWN or el == Constants.ENEMY_BODY_RIGHT_UP):
                    self.elementsSetPos(x, y, Constants.ENEMY_BODY) # Тело противника на карте
        
        debugInfo(156)

        self.calculateShoresStarting()

        self.changeMode()

        if round.time > 63:
            f = 1

        if round.time > 66:
            f = 1

        self.calculateShores()

        debugInfo(160)


        print("Round mode = " + round.mode.__str__())

        if round.time > 66:
            # self.printShores()
            f = 1

        # # Шаг 1) Сначала нужно бежать за змейй если я злой
        # if self.snake.SnakeEvilStep > 0:
        #     napravlenie = self.findOptimalElement(self.snake.SnakeEvilStep, 0)

        #     if napravlenie > 0:
        #         return napravlenie

        # Шаг 2) Расчитаем удаленность до каждой бутылки ярости
        ## Если нам добежать до неё быстрее но разница не велика, значит бежим туда

        debugInfo(254)

        # point = self.calculateNearFury()

        # if point != None:
        #     (x, y, step) = point
            
        #     # goto = self.calcShadowGoTo(x, y, self.snake.x, self.snake.y, (self.snake.SnakeEvilStep, self.snake.Length) , Constants.FURY_PILL_STEP_NUM, Constants.NUM_CALC_FIRS_STEP)
        #     goto = self.calcShadowGoToSnake(x, y, Constants.FURY_PILL_STEP_NUM, Constants.NUM_SHORE_FIRS_STEP)

        #     if goto != None:
        #         (x, y, napravlenie, Allshore) = goto

        #         if napravlenie > 0:
        #             return napravlenie


        # Шаг 3) Если змея в ярости расчитываем ходы на ходы в ярости

        if round.time > 1:
            # self.printShores()
            f = 1

        debugInfo(277)


        # Шаг 2) Если змея не в ярости расчитываем ходы
        napravlenie = self.findOptimalElement(max(Constants.NUM_CALC_MAX_STEP, self.snake.SnakeEvilStep), 0)

        if napravlenie > 0:
            return napravlenie


        debugInfo(285)

        # Шаг 3) нет выхода попытка расчитать погрешность до стен
        # napravlenieStrateg, x, y = self.findStrategElement(Constants.NUM_CALC_MAX_STEP_ALL, 0)

        # StrategShore = Constants.SHORE_WALL

        # # Перепроверим ход на оптимальность
        # if napravlenieStrateg > 0:
        #     StrategShore = self.shoresGetPos(x, y)

        # napravlenie = self.optimalHod(StrategShore, napravlenieStrateg)

        # if napravlenieStrateg == napravlenie:
        #     return napravlenie
        napravlenie, x, y = self.findStrategElement(Constants.NUM_CALC_MAX_STEP_ALL, 0)

        if napravlenie > 0:
            return napravlenie
 
        # Шаг 4) Если змея не в ярости расчитываем ходы
        napravlenie = self.findOptimalElement(max(Constants.NUM_CALC_MAX_STEP, self.snake.SnakeEvilStep), Constants.NUM_SHORE_FIRS_STEP)

        if napravlenie > 0:
            return napravlenie



        # Шаг 5) нет выхода попытка расчитать погрешность до стен
        napravlenieStrateg, x, y = self.findStrategElement(Constants.NUM_CALC_MAX_STEP_ALL, Constants.SHORE_WALL + 1)

        StrategShore = Constants.SHORE_WALL

        if napravlenieStrateg > 0:
            # StrategShore = self.shoresGetPos(x, y)
            f = 1    
        else:
            #Некуда ходить
            f = 1    

        #Некуда ходить
        # self.printShadow()
        # self.printShores()
        # self.print_board()
        
        f = 1

        napravlenie = self.optimalHod(x, y, napravlenieStrateg)


        if napravlenie == 0:
            f = 1 #лучшей клетки нет, ходи куда хочешь

        return napravlenie
        # return 0

        # debugInfo(500)


        # napravlenie = self.calcShadowRecursive(self.snake, 30, -110)


        # debugInfo(165)




        # a = 1

    # def find(self):
    
    #     napravlenie = self.calcShadowRecursive(self.snake, 100, -10)

    def optimalHod(self, strateg_x, strateg_y, napravlenieStrateg):
        
        StrategShore = self.shoresGetPos(strateg_x, strateg_y)
        element = self.elementsGetPos(strateg_x, strateg_y)
        if element == Constants.STONE: #Уберем преимущество в очках у камня
            if self.snake.SnakeEvilStep <= 0:
                StrategShore = StrategShore - Constants.SHORE_STONE - Constants.SHORE_STONE


        #Сюда добавить алгоритм хода в самую выгодную точку
        x = self.snake.x
        y = self.snake.y

        maxShore = Constants.SHORE_NEVER
        maxX = 0
        maxY = 0
        napravlenie = 0

        for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            shore = self.shoresGetPos(x + dx, y + dy)
            element = self.elementsGetPos(x + dx, y + dy)
            wall = self.backgroundGetPos(x + dx, y + dy)

            if element == Constants.STONE: #Уберем преимущество в очках у камня
                if self.snake.SnakeEvilStep <= 0:
                    shore = shore - Constants.SHORE_STONE - Constants.SHORE_STONE

            if wall !=0:
                shore = Constants.SHORE_NEVER
            if shore > maxShore:
                maxShore = shore
                maxX = x + dx
                maxY = y + dy

        # OptimalShore = self.shoresGetPos(maxX, maxY)

        if maxShore > StrategShore:
            napravlenie = self.GoToNapravlenie(x, y, maxX, maxY)
        else:
            napravlenie = napravlenieStrateg

        return napravlenie


    def changeMode(self):


        # if round.time < 30:
        round.mode = Mapping.MODE_NORMAL
        # elif round.time < 60:
        #     round.mode = Mapping.MODE_APPLE

        debugInfo(319)

        # Пока нет обработки режима MODE_FURYEVIL и MODE_FURY с точки зрения атаки, разницы нет
        # Если ты бежишь за змей и тебе до неё столько клеток, сколько её длина то не стоит

        if self.snake.SnakeEvilStep > 1: # Я злой, если другие змеи поблизости активируем режим поиска злости и атаки
            self.calcShadow(self.snake.x, self.snake.y, self.snake.SnakeEvilStep, Constants.NUM_SHORE_FIRS_STEP, 0)
            for indexSnake in range(len(self.enemySnake)):
                tmpSnake = self.enemySnake[indexSnake]
                
                min_step = 99999
                min_index = 99999 
                for indexCoordinates in range(len(tmpSnake.coordinates)):
                    enemysnake_x, enemysnake_y = tmpSnake.coordinates[indexCoordinates]
                    num_step = self.shadowGetPos(enemysnake_x, enemysnake_y)
                    if num_step > 0:
                        if num_step < min_step:
                            min_step = num_step
                            min_index = indexCoordinates

                if min_step < 99999:
                    if tmpSnake.SnakeEvilStep > self.snake.SnakeEvilStep:
                        # self.printShadow()
                        if self.snake.SnakeEvilStep < 2 and tmpSnake.Length < 3: #Самая худшая ситуация, коротыш погоня за хвостом
                            round.mode = Mapping.MODE_FURY
                            break
                        else:
                            # self.printShadow()
                            if min_index >= len(tmpSnake.coordinates)-1: # Гонюсь за хвостом
                                tmpSnake.goto_TAIL = 1
                                round.mode = Mapping.MODE_FURY
                            else:
                                round.mode = Mapping.MODE_FURYEVIL
                    else: 
                        if min_index >= len(tmpSnake.coordinates)-1: # Гонюсь за хвостом
                            round.mode = Mapping.MODE_FURY
                            tmpSnake.goto_TAIL = 1
                            break
                        else:
                            if num_step < 8 and self.snake.SnakeEvilStep - 2 >= num_step:
                                # self.printShadow() #Интересны вот эти ситуации
                                round.mode = Mapping.MODE_EVIL
                            else:
                                round.mode = Mapping.MODE_FURYEVIL
                


        elif self.snake.SnakeEvilStep <= 0: # Я не злой, если рядом злые змеи ищем елексир зла

            debugInfo(337)

            self.shadowInit()
            for indexSnake in range(len(self.enemySnake)):
                tmpSnake = self.enemySnake[indexSnake]
                if tmpSnake.SnakeEvilStep > 1:
                    self.calcShadow(tmpSnake.x, tmpSnake.y, tmpSnake.SnakeEvilStep, Constants.NUM_SHORE_ENEMY_STEP, 0, 1)
                for indexCoordinates in range(len(self.snake.coordinates)):
                    my_x, my_y = self.snake.coordinates[indexCoordinates]
                    if self.shadowGetPos(my_x, my_y) > 0:
                    #    round.mode = Mapping.MODE_FURY  
                       round.mode = Mapping.MODE_FURYEVIL  
                       break

            if round.mode < Mapping.MODE_FURY_NORMAL:

                debugInfo(352)

                self.shadowInit() # Я не злой, если рядом обычные змеи включаем усиленный поиск бутылок зла
                for indexSnake in range(len(self.enemySnake)):
                    tmpSnake = self.enemySnake[indexSnake]
                    # if tmpSnake.SnakeEvil == 0:
                    self.calcShadow(tmpSnake.x, tmpSnake.y, Constants.FURY_PILL_STEP_NUM - 2, Constants.NUM_SHORE_ENEMY_STEP, 0, 1)
                    for indexCoordinates in range(len(self.snake.coordinates)):
                        my_x, my_y = self.snake.coordinates[indexCoordinates]
                        if self.shadowGetPos(my_x, my_y) > 0:
                            round.mode = Mapping.MODE_FURY_NORMAL  
                            break

        if round.mode == Mapping.MODE_NORMAL:

            debugInfo(367)

            
            for indexSnake in range(len(self.enemySnake)):
                tmpSnake = self.enemySnake[indexSnake]
                if tmpSnake.Length > self.snake.Length:
                    if round.time < 200:
                        # Проверим есть ли яблоки по близости
                        self.calcShadow(self.snake.x, self.snake.y, Constants.NUM_CALC_MAX_STEP, Constants.NUM_SHORE_FIRS_STEP, 0)
                        for indexApple in range(len(self.apples)):
                            x, y = self.apples[indexApple]
                            if self.shadowGetPos(x, y) > 0:
                                # round.mode = Mapping.MODE_APPLE
                                round.mode = Mapping.MODE_NORMAL
                                break
                    else:    
                        round.mode = Mapping.MODE_FURY_NORMAL
                    break

        if round.mode == Mapping.MODE_FURY:
            # Проверим есть ли бутылки ярости по близости
            self.calcShadow(self.snake.x, self.snake.y, Constants.NUM_CALC_MAX_STEP, Constants.NUM_SHORE_FIRS_STEP, 0)
            find = 0
            for index in range(len(self.furyPill)):
                x, y = self.furyPill[index]
                if self.shadowGetPos(x, y) > 0:
                    find = 1
                    break
            if find == 0:
                round.mode = Mapping.MODE_FURY_NORMAL


        debugInfo(385)


        # Если рядом много зелья зла спасения

        # Если рядом много зелья и я злой режим зла
        #
        # Если рядом враг, режим спасения

        # Если рядом никого, режим сбора яблок



    def calcShadowGoToSnake(self, x, y, numCalculate, shoreBreak):
        return self.calcShadowGoTo(x, y, self.snake.x, self.snake.y, (self.snake.SnakeEvilStep, self.snake.Length) , numCalculate, shoreBreak)

    def findOptimalElement(self, numCalculate, shoreBreak):

        elements = [] #Массив элементов на поле
        # elementsRez = [] #Массив элементов на поле
         
        # Закрасим тень, чтобы понять, как далеко до каждой ячейки
        points = self.calcShadow(self.snake.x, self.snake.y, numCalculate, shoreBreak, 1)

        summShore = 0

        # Поиск ближайших элементов на карте и запись в массивы
        for indexNum in range(len(points)):
            x, y, shadow = points[indexNum]
            # for x in range(0, self._len // self._size):
            #     for y in range(0, self._size):
            # shadow = self.shadowGetPos(x, y)
            if shadow != 0:
                shore = self.shoresGetPos(x, y)
                if shore > shoreBreak:
                    elements.append((x, y, shore, shore + (shadow * Constants.SHORE_HOD), shadow, numCalculate - shadow))
                    summShore = summShore + shore

        # Сортируем и берем выборку допустим не больше 20
        if self.snake.SnakeEvilStep > 0:
            elements.sort(key=itemgetter(3, 5), reverse=True)
        else:    
            elements.sort(key=itemgetter(5, 3), reverse=True)

        # Возможно стоит тоже расчитать направления, и определить куда лучше бежать, для выборки первого элемента, пока это ближайший

        el = None

        for indexNum in range(len(elements)):
            x, y, shore, maxShore, step, invertStep = elements[indexNum]

            if shore >= Constants.SHORE_APPLE and step < Constants.NUM_CALC_MAX_STEP // 2: # Если до элемента бежать не далеко и элемент один
                el = (x, y, step)
            elif(summShore > Constants.NUM_SHORE_NEXT_LOCATION): # Если в окруше еще много вкусного, бежим к первому
                el = (x, y, step)
                # return el

            if el != None:
                x, y, step = el
                goto = self.calcShadowGoToSnake(x, y, step, shoreBreak)

                if goto != None:
                    (x, y, napravlenie, Allshore) = goto

                    if napravlenie > 0:
                        return napravlenie

        return 0                    

    def findStrategElement(self, numCalculate, shoreBreak):

        # Ещем дальше, определяем направление движения

        elements = [] #Массив элементов на поле
        # Закрасим тень, чтобы понять, как далеко до каждой ячейки

        self.timeStart()

        points = self.calcShadow(self.snake.x, self.snake.y, Constants.NUM_CALC_MAX_STEP_ALL, shoreBreak, 1)

        self.timeFinish("Расчет тени: ")

        if round.time == 119:
            f = 1
            # self.printShadow()

        # Поиск ближайших элементов на карте и запись в массивы
        for indexNum in range(len(points)):
            x, y, shadow = points[indexNum]
            # for x in range(0, self._len // self._size):
            #     for y in range(0, self._size):
            # shadow = self.shadowGetPos(x, y)
            if shadow > 0:
                shore = self.shoresGetPos(x, y)
                if shore > Constants.SHORE_WALL:
                    elements.append((x, y, shore, shore + (shadow * Constants.SHORE_HOD), shadow, numCalculate - shadow, 0))

        divider = 8
        maxX = self._size // divider
        maxY = self._size // divider

        matrixDiv = []

        for dx in range((maxX + 1) * (maxY + 1)):
            matrixDiv.append(0)

        # matrixDiv = [maxX][maxY]

        # self.printShadow()

        # Определяем очковый квадрат :-)
        for indexNum in range(len(elements)):
            el = elements[indexNum]
            x, y, shore, maxShore, step, invertStep, sort = el

            dx = x // divider
            dy = y // divider

            matrixDiv[dx + dy * maxY] = matrixDiv[dx + dy * maxY] + maxShore

        maxDx = 0
        maxDy = 0
        maxShore = matrixDiv[maxDx + maxDy * maxY]
        for dx in range(maxX):
            for dy in range(maxY):
                if maxShore < matrixDiv[dx + dy * maxY]:
                    maxDx = dx
                    maxDy = dy
                    maxShore = matrixDiv[maxDx + maxDy * maxY]



        # maxDx и maxDy это лучший квадрат
        for indexNum in range(len(elements)):
            el = elements[indexNum]
            x, y, shore, maxShore, step, invertStep, sort = el



            dx = x // divider
            dy = y // divider

            if dx == maxDx and dy == maxDy:
                sort = 1

            elements[indexNum] = (x, y, shore, maxShore, step, invertStep, sort)


        # Сортируем по ближайшему
        # elements.sort(key=itemgetter(6, 4), reverse=True)

        # Сортируем по ближайшему
        elements.sort(key=itemgetter(6, 2), reverse=True)

        # Для определения направления
        naprShore = [0,0,0,0,0]

        MAX_STEPS = Constants.NUM_CALC_MAX_ELEMENTS

        kolvo = min(MAX_STEPS, len(elements))
        for indexNum in range(0, kolvo):
            el = elements[indexNum]

            x, y, shore, maxShore, step, invertStep, sort = el

            self.timeStart()
            # goto = self.calcShadowGoToSnake(x, y, step, shoreBreak)     
            goto = self.calcShadowGoToSnake(x, y, step, shoreBreak)     
            self.timeFinish("Тест похода до клетки: ")

            if goto != None:
                (x, y, napravlenie, Allshore) = goto

                return (napravlenie, x, y)

                # elementsRez.append((x, y, napravlenie, Allshore, step))

                # naprShore[napravlenie] = naprShore[napravlenie] = Allshore

            else:
                f = 1


        # Сортируем по ближайшему
        # elementsRez.sort(key=itemgetter(4), reverse=True)

        # maxIndex = 1
        # max = naprShore[maxIndex]
        # for index in range(1,4):
        #     if naprShore[index] > max:
        #         maxIndex = index
        #         max = naprShore[index]

        # for indexNum in range(len(elementsRez)):
        #     x, y, napravlenie, Allshore, step = elementsRez[indexNum]
        #     if napravlenie == maxIndex:
        #         return napravlenie
        #         # el = (x, y, step)
        #         # return el

        return (0, 0, 0)



        # self.printShadow()

        # f = 1




    # def calcShadowRecursive(self, snake, numCalculate, shoreBreak):

    #     debugInfo(188)

    #     # shadow = Shadow()
    #     # shadow.shadowInit(self._size)
    
    #     debugInfo(192)

    #     points = []

    #     hod = 1
    #     # points.append((snake.x, snake.y, snake.x, snake.y, 0, (snake.SnakeEvilStep, snake.Length)))
    #     # shadow.shadowSetPos(snake.x, snake.y, hod)

    #     napravlenie = 0
    #     VesHoda = 0

    #     evilStep = snake.SnakeEvilStep

    #     x = snake.x
    #     y = snake.y    

    #     point = (x, y, hod, 0)

    #     pointRez = self._calcShadowRecursiveStep(point, (snake.SnakeEvilStep, snake.Length), points, numCalculate, shoreBreak, evilStep, VesHoda)

    #     # x, y, prev_x, prev_y, maxShore, minShoreBreak, maxHod, maxTrajectory = pointRez[0]

    #     maxShore, minShoreBreak, maxHod, maxTrajectory = pointRez

    #     if(maxHod > 1):
    #         dx, dy = maxTrajectory[len(maxTrajectory)-1] #Получаем предпоследний ход
 
    #         if(x - 1 == dx and y == dy):
    #             napravlenie = Mapping.SNAKE_LEFT
    #         elif(x + 1 == dx and y == dy):
    #             napravlenie = Mapping.SNAKE_RIGHT
    #         elif(x == dx and y - 1 == dy):
    #             napravlenie = Mapping.SNAKE_UP
    #         elif(x == dx and y + 1 == dy):
    #             napravlenie = Mapping.SNAKE_DOWN

    #     debugInfo(223)



    #     self.saveTrajectry(maxTrajectory)

    #     debugInfo(228)

    #     self.printShores()

    #     debugInfo(231)

    #     print("Оптимальных ход Очков = ", maxShore, ", количество ходов = ", maxHod)
 

    #     # pointRez = self._calcShadowRecursiveStep(points, hod, numCalculate, -70, evilStep, VesHoda)

    #     # x2, y2, prev_x2, prev_y2, maxShore2, minShoreBreak2, maxHod2, maxTrajectory2 = pointRez[0]

    #     # print("Расчет траектории закончен = ", maxShore, maxHod, nextNapr)

    #     return napravlenie

    # def saveTrajectry(self, maxTrajectory):
    #     max = len(maxTrajectory)
    #     for indexNum in range(len(maxTrajectory)):
    #         x, y = maxTrajectory[indexNum]
    #         self._trajectory[x + y * self._size] = max - indexNum

    # def shadowReadPoint(self, points, x, y):
    #     for indexNum in range(len(points)):
    #         point = points[indexNum]
    #         _x, _y, _hod, _ves = point
    #         if x == _x and y ==_y:
    #             return _hod
    #     return 0    


    def calculateShoresStarting(self):

        # Своя змея
        for index in range(len(self.snake.coordinates)): 
            x, y = self.snake.coordinates[index]
            shoreBody = 0
            if index == 0: # Это голова
                self.addShore(x, y, 0)
            elif index == 1:
                #Следующая ячейка после головы всегда стена, так как нельзя развернуться на 180 градусов
                self.setShore(x, y, Constants.SHORE_WALL)
            elif index < len(self.snake.coordinates)-1:
                # shoreBody = Constants.SHORE_SNAKE_BODY * (self.snake.Length - index)
                shoreBody = Constants.SHORE_WALL + 1
                self.setShore(x, y, shoreBody)
            else:
                self.addShore(x, y, Constants.SHORE_SNAKE_TAIL) #Пока про хвост рандомно, но на самом деле можно проверить есть ли перед головой яблоко тогда цена равна цене тела




    def calculateShores(self):


        debugInfo(676)

        # Шаг 1) Заполним зону боя под злыми змейками
        ## Нужно еще подумать как посчитать зону злых змеек если я тоже злой
        for indexSnake in range(len(self.enemySnake)): 
            tmpSnake = self.enemySnake[indexSnake]
            # if tmpSnake.SnakeEvil == 1: # Если змея в ярости
                ####### Если у меня количество ярости столько же шагов или больше то мне не страшна эта змея
                # if self.snake.SnakeEvil == 0 or tmpSnake.SnakeEvilStep > self.snake.SnakeEvilStep:
            self.calculateShoresEnemyEvilSnakes(tmpSnake, tmpSnake.x, tmpSnake.y, tmpSnake.SnakeEvilStep)

        debugInfo(403)



        f = 1

        # Чужие змеи расчет очков
        self.calcShadow(self.snake.x, self.snake.y, max(Constants.NUM_CALC_MAX_STEP, self.snake.SnakeEvilStep), Constants.NUM_SHORE_FIRS_STEP)
        # else:
        #     self.calcShadow(self.snake.x, self.snake.y, Constants.FURY_PILL_STEP_NUM, Constants.NUM_SHORE_FIRS_STEP)

        debugInfo(699)


        for indexSnake in range(len(self.enemySnake)): 
            tmpSnake = self.enemySnake[indexSnake]
            #
            if ((tmpSnake.SnakeEvilStep <= 0 and self.snake.SnakeEvilStep <= 0) 
              or (tmpSnake.SnakeEvilStep > 0 and self.snake.SnakeEvilStep > 0)): # Если змеи не в ярости, или обе в ярости
                
                # Сравниваем длины
                if (self.snake.Length - tmpSnake.Length)  > 2: # Одна единица длины в запасе на яблоко по пути

                    if tmpSnake.goto_TAIL == 1:
                        continue

                    
                    # Нужно расчитать веса для тела вражеской змейки
                    for index in range(1, len(tmpSnake.coordinates)): 
                        x, y = tmpSnake.coordinates[index]
                        # Но конечно нужно выделять не все клетки а только в пределах досигаемости ярости
                        if self.shadowGetPos(x, y) > 0:
                            if self.snake.SnakeEvilStep > 0:
                                self.setShore(x, y, Constants.SHORE_ENEMY_SNAKE_BODY)
                            else:
                                self.addShore(x, y, Constants.SHORE_ENEMY_SHORE_EVIL)    

                    # Бьем только в голову, если моя змея не злая
                    # Здесь еще важно бежит змея в твоем направлении или нет если в твоем, то можно догнать. пока не знаю как
                    self.setShore(tmpSnake.x, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD)

                    if tmpSnake.head == Mapping.SNAKE_UP:
                        self.setCheckShore(tmpSnake.x, tmpSnake.y-1, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(tmpSnake.x-1, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(tmpSnake.x+1, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                    elif tmpSnake.head == Mapping.SNAKE_DOWN:
                        self.setCheckShore(tmpSnake.x, tmpSnake.y+1, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(tmpSnake.x-1, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(tmpSnake.x+1, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                    elif tmpSnake.head == Mapping.SNAKE_LEFT:
                        self.setCheckShore(tmpSnake.x-1, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(tmpSnake.x, tmpSnake.y-1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(tmpSnake.x, tmpSnake.y+1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                    elif tmpSnake.head == Mapping.SNAKE_RIGHT:
                        self.setCheckShore(tmpSnake.x+1, tmpSnake.y, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(tmpSnake.x, tmpSnake.y-1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(tmpSnake.x, tmpSnake.y+1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг

                    # Здесь нужно еще добавить две\три точки в направлении рядом с головой
                else: # У нас нет преимущества, нужно держать голову подальше
                    self.addShore(tmpSnake.x, tmpSnake.y, Constants.SHORE_ENEMY_SHORE_EVIL)
                    # Здесь нужно еще добавить две\три точки в направлении рядом с головой
                
                    if tmpSnake.SnakeEvilStep > 0 and self.snake.SnakeEvilStep > 0: # Если обе злые значит можно нападать на тело за головой
                        for index in range(1, len(tmpSnake.coordinates)): 
                            x, y = tmpSnake.coordinates[index]
                            self.setShore(x, y, Constants.SHORE_ENEMY_SNAKE_BODY)
                    else:
                        for index in range(1, len(tmpSnake.coordinates)): 
                            x, y = tmpSnake.coordinates[index]
                            self.addShore(x, y, Constants.SHORE_ENEMY_SHORE_EVIL)

            elif tmpSnake.SnakeEvilStep > 0 and self.snake.SnakeEvilStep <= 0: # Если вражеская, то нужно держаться подальше
                # Нужно расчитать веса для тела вражеской змейки
                for index in range(len(tmpSnake.coordinates)): 
                    x, y = tmpSnake.coordinates[index]
                    # Но конечно нужно выделять не все клетки а только в пределах досигаемости ярости
                    self.addShore(x, y, Constants.SHORE_ENEMY_SHORE_EVIL) #но это уже ранее сделано
            
            elif tmpSnake.SnakeEvilStep <= 0 and self.snake.SnakeEvilStep > 0: # Если моя, то кусать за все

                if tmpSnake.goto_TAIL == 1:
                    continue

                # Нужно расчитать веса для тела вражеской змейки
                for index in range(len(tmpSnake.coordinates)): 
                    x, y = tmpSnake.coordinates[index]
                    # Но конечно нужно выделять не все клетки а только в пределах досигаемости ярости
                    if self.shadowGetPos(x, y) > 0:
                        self.setShore(x, y, Constants.SHORE_ENEMY_SNAKE_BODY)

                x = tmpSnake.x
                y = tmpSnake.y
                if self.shadowGetPos(x, y) > 0:
                    if tmpSnake.head == Mapping.SNAKE_UP:
                        self.setCheckShore(x, y-1, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(x-1, y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(x+1, y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                    elif tmpSnake.head == Mapping.SNAKE_DOWN:
                        self.setCheckShore(x, y+1, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(x-1, y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(x+1, y, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                    elif tmpSnake.head == Mapping.SNAKE_LEFT:
                        self.setCheckShore(x-1, y, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(x, y-1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(x, y+1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                    elif tmpSnake.head == Mapping.SNAKE_RIGHT:
                        self.setCheckShore(x+1, y, Constants.SHORE_ENEMY_SNAKE_HEAD) #Точка перед змеей
                        self.setCheckShore(x, y-1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг
                        self.setCheckShore(x, y+1, Constants.SHORE_ENEMY_SNAKE_HEAD // 2) #Точка вокруг

        debugInfo(765)

        # Закрасим тень, чтобы понять, как далеко до каждой ячейки
        self.calcShadow(self.snake.x, self.snake.y, Constants.NUM_CALC_MAX_STEP_ALL, Constants.NUM_SHORE_FIRS_STEP)

        # Шаг 3) Заполнение игрового поля очками
        
        if round.mode == Mapping.MODE_APPLE or round.mode == Mapping.MODE_NORMAL or round.mode == Mapping.MODE_FURY_NORMAL:
            # Яблоки
            for index in range(len(self.apples)): 
                x, y = self.apples[index]
                if self.chechXYtrap(x, y):
                    self.addShore(x, y, Constants.SHORE_APPLE)

        debugInfo(412)

        if round.mode == Mapping.MODE_NORMAL or round.mode == Mapping.MODE_FURY_NORMAL:
            # Камни 
            for index in range(len(self.stones)): 
                x, y = self.stones[index]
                step = self.shoresGetPos(x, y)
                # Расставляем очки только для камней поблизости
                if ((self.snake.SnakeEvil == 1 and step <= self.snake.SnakeEvilStep) or self.snake.Length >= Constants.SNAKE_LEN_GOTO_STONE): 
                    if self.chechXYtrap(x, y):
                        self.addShore(x, y, Constants.SHORE_STONE)
        # else:
        #     for index in range(len(self.stones)): 
        #         x, y = self.stones[index]
        #         step = self.shoresGetPos(x, y)
        #         # Расставляем очки только для камней поблизости
        #         if ((self.snake.SnakeEvil == 1 and step <= self.snake.SnakeEvilStep) or self.snake.Length >= Constants.SNAKE_LEN_GOTO_STONE): 
        #             if self.chechXYtrap(x, y):
        #                 self.addShore(x, y, Constants.SHORE_STONE)


        debugInfo(420)

        if round.mode == Mapping.MODE_NORMAL or round.mode == Mapping.MODE_FURY or round.mode == Mapping.MODE_FURY_NORMAL or round.mode == Mapping.MODE_FURYEVIL:
            # Бутылка ярости
            for index in range(len(self.furyPill)): 
                x, y = self.furyPill[index]
                if self.chechXYtrap(x, y):
                    self.addShore(x, y, Constants.SHORE_FURY)
                    if round.mode == Mapping.MODE_FURY or round.mode == Mapping.MODE_FURY_NORMAL or round.mode == Mapping.MODE_FURYEVIL:
                        self.addShore(x, y, Constants.SHORE_FURY)

        debugInfo(427)

        # Золото
        if round.mode == Mapping.MODE_NORMAL or round.mode == Mapping.MODE_FURY_NORMAL or round.mode == Mapping.MODE_APPLE:
            for index in range(len(self.golds)): 
                x, y = self.golds[index]
                if self.chechXYtrap(x, y):
                    self.addShore(x, y, Constants.SHORE_GOLD)

        debugInfo(435)

        # Пересчет очков за бутылку ближайшую
        self.calculateNearFury()

        # Вес хода должен определять срочность события. если срочность высокая значит вес хода больше

        # Если к твоему телу или хвосту приближается злая змея. А змея очень длинная.
        # То иногда имеет смысл откусить себя
        # Можно дописать этот алгоритм

    def chechXYtrap(self, x, y):

        # Поиск приманок убиец
        rez = 0

        for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:

            wall = self.backgroundGetPos(x + dx, y + dy)
            # shadow = self.shadowGetPos(x + dx, y + dy)
            shore = self.shoresGetPos(x + dx, y + dy)
            # element = self.elementsGetPos(x + dx, y + dy)

            if wall == 0 and shore >= Constants.NUM_SHORE_TRAP_STEP: #Пока преграда только стена и отрицательные очки
                rez = rez + 1

        if rez < 2:
            return False
        return True         

    def addShore(self, x, y, shore):
        self.shoresSetPos(x, y, self.shoresGetPos(x, y) + shore)

    def setShore(self, x, y, shore):
        self.shoresSetPos(x, y, shore)

    def setCheckShore(self, x, y, shore):
        element = self.elementsGetPos(x, y) #Если какие то посторонние предметы не заполняем ячейки
        if element == 0 or element == Constants.APPLE or element == Constants.GOLD or element == Constants.FURY_PILL:
            self.shoresSetPos(x, y, shore)

    def calculateNearFury(self):

        results = []    

        debugInfo(534)

        furies = []

        distanceMax = Constants.FURY_PILL_STEP_NUM / 2 #Если разница между добежать мне и добежать противнику не больше N ходов

        numCalculate = Constants.FURY_PILL_STEP_NUM + 5 #Количество просчитываемых ходов
        # Можно брать либо размер ходов FURY_PILL либо максимальное количество ходов ярости Других змей                                                      

        self.calcShadow(self.snake.x, self.snake.y, numCalculate, Constants.NUM_SHORE_FIRS_STEP)
        for indexFury in range(len(self.furyPill)): 
            x_fury, y_fury = self.furyPill[indexFury]
            if self.shadowGetPos(x_fury, y_fury) > 0:
               furies.append((x_fury, y_fury)) 

        for indexFury in range(len(furies)): 
            x_fury, y_fury = furies[indexFury]

            self.calcShadow(x_fury, y_fury, numCalculate, Constants.NUM_SHORE_FIRS_STEP)

            stepMySnake = self.shadowGetPos(self.snake.x, self.snake.y)

            # self.printShadow()

            for indexSnake in range(len(self.enemySnake)): 
                tmpSnake = self.enemySnake[indexSnake]
                stepTmpSnake = self.shadowGetPos(tmpSnake.x, tmpSnake.y)

                delta = stepTmpSnake - stepMySnake

                if delta > 0 and delta <= distanceMax:
                    results.append((x_fury, y_fury, stepMySnake))

        debugInfo(558)


        if len(results) == 0:
            return None

        min = results[0]
        for indexResult in range(len(results)):
            x_fury, y_fury, stepMySnake = results[indexResult]
            self.addShore(x_fury, y_fury, Constants.SHORE_FURY_EVIL)  # Точка до которой нужно бежать    

            tmp_x, tmp_y, tmp_step = min
            if tmp_step > stepMySnake: # Выбирается самая ближайшая точка
                min = results[indexResult]


        debugInfo(574)


        tmp_x, tmp_y, tmp_step = min
        # self.addShore(tmp_x, tmp_y, Constants.SHORE_FURY_EVIL_NEAR)  # Ближайшая точка до которой нужно бежать в первую очередь (в два раза больше веса)  
        return min


    def calcShadowGoTo(self, x_fury, y_fury, x_start, y_start, snake, numCalculate, shoreBreak):
        pointsNew = []
        # pointsNewNum = 0

        debugInfo(586)


        points = []
        shore = self.shoresGetPos(x_fury, y_fury)
        points.append((x_fury, y_fury, shore))

        pointsFinish = []

        (snake_evilstep, snake_length) = snake

        # pointsNum = 1

        hod = 1

        self.shadowInit()
        self.shadowSetPos(x_fury, y_fury, hod)

        debugInfo(598)

        while hod <= numCalculate:

            end = 0    

            for indexNum in range(len(points)):
                x, y, prev_shore = points[indexNum]
                for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    wall = self.backgroundGetPos(x + dx, y + dy)
                    shadow = self.shadowGetPos(x + dx, y + dy)
                    shore = self.shoresGetPos(x + dx, y + dy)
                    element = self.elementsGetPos(x + dx, y + dy)

                    if element == Constants.STONE and (snake_evilstep == 0 and snake_length < Constants.SNAKE_LEN_GOTO_STONE) and shoreBreak >= Constants.NUM_SHORE_FIRS_STEP: # Пропускаем камни если не злой или длна малая
                        propus = 1
                    elif wall == 0 and shadow == 0 and shore >= shoreBreak: #Пока преграда только стена и отрицательные очки
                        self.shadowSetPos(x + dx, y + dy, hod)
                        pointsNew.append((x + dx, y + dy, prev_shore + shore))
                        # pointsNewNum = pointsNewNum + 1

                        if x + dx == x_start and y + dy == y_start:
                            end = 1
                            pointsFinish.append((x, y, prev_shore + shore, shore))

            debugInfo(961)


            if end == 1: # Дошли до точки, решим в какую точку выгодней пойти

                if len(pointsFinish) > 1:    
                    # for indexNum in range(len(pointsFinish)):
                    #     x, y, prev_shore = pointsFinish[indexNum]
                    #     # shore = self.shoresGetPos(x + dx, y + dy)
                    #     pointsFinish[indexNum] = (x, y, shore)

                    #Сортировка по колонке prev_shore
                    pointsNew.sort(key=itemgetter(2), reverse=True)

                x, y, Allshore, hodShore = pointsFinish[0]

                # if round.time == 11:
                #     self.printShadow()
                #     self.printShores() 

                napravlenie = self.GoToNapravlenie(x_start, y_start, x, y)
                return (x, y, napravlenie, Allshore)


            if len(pointsNew) == 0:
                return None

            hod = hod + 1
            points = pointsNew
            # pointsNum = pointsNewNum


    def GoToNapravlenie(self, x_start, y_start, x_finish, y_finish):

            if(x_start - 1 == x_finish and y_start == y_finish):
                return Mapping.SNAKE_LEFT
            elif(x_start + 1 == x_finish and y_start == y_finish):
                return Mapping.SNAKE_RIGHT
            elif(x_start == x_finish and y_start - 1 == y_finish):
                return Mapping.SNAKE_UP
            elif(x_start == x_finish and y_start + 1 == y_finish):
                return Mapping.SNAKE_DOWN

            return 0    


    def calcShadow(self, x_fury, y_fury, numCalculate, shoreBreak, returnpoint = 0, clearShadow = 1):
        pointsNew = []
        pointsNewNum = 0

        debugInfo(586)

        pointsNum = 1

        hod = 1

        pointsHod = []

        points = []
        points.append((x_fury, y_fury))

        # if returnpoint == 1:
        #     pointsHod.append((x_fury, y_fury, hod))
 
        if clearShadow == 1:
            self.shadowInit()

        self.shadowSetPos(x_fury, y_fury, hod)

        debugInfo(598)

        # self.printShadow()

        while hod <= numCalculate:
            for indexNum in range(len(points)):
                x, y = points[indexNum]
                for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    wall = self.backgroundGetPos(x + dx, y + dy)
                    
                    if wall == 0:
                        shadow = self.shadowGetPos(x + dx, y + dy)
                        if shadow == 0:
                            shore = self.shoresGetPos(x + dx, y + dy)
                            if shore >= shoreBreak: #Пока преграда только стена и отрицательные очки

                                self.shadowSetPos(x + dx, y + dy, hod)
                                pointsNew.append((x + dx, y + dy))
                                pointsNewNum = pointsNewNum + 1

                                if returnpoint == 1:
                                    pointsHod.append((x + dx, y + dy, hod))

            if pointsNewNum == 0:
                break

            hod = hod + 1
            points = pointsNew
            pointsNum = pointsNewNum

        if returnpoint == 1:
            return pointsHod


    def calculateShoresEnemyEvilSnakes(self, enemy_snake, x_start, y_start, evil_step):
        evilShoresNum = 20 # Даже если ходов больше, обсчитывать будет не больше 20
        evilShores = [-30,-18,-16,-14,-12,-10,-8,-6,-4,-2,-1,-1,-1,-1,-1,-1,-1,-1,-1,-1]

        debugInfo(1057)


        if enemy_snake.SnakeEvilStep <= 0 and self.snake.SnakeEvilStep < 2 and enemy_snake.Length - 2 > self.snake.Length:
            evil_step = 3 #Если змея не злая, и её длина больше, все равно нужно боятся
        elif enemy_snake.SnakeEvilStep > 0 and self.snake.SnakeEvilStep > evil_step:
            return #Если змея злая, но у меня больше злости не убегать
        elif enemy_snake.SnakeEvilStep <= 0 and self.snake.SnakeEvilStep > 0:
            return
            # Если я злой, а противник нет, повернуть все в лучшую сторону
            evil_step = max(self.snake.SnakeEvilStep, 2)           
            evil_step = min(evil_step, 5)           
            evilShores = [10,5,4,3,2]
        else:
            f = 1 #Штатный режим, когда змея злая    

        pointsAll = []

        pointsNew = []
        pointsNewNum = 0

        debugInfo(627)

        points = []
        points.append((x_start, y_start))
        # pointsNum = 1

        hod = 1

        if round.time > 17:
            f = 1

        # self.shoresSetPos(x_start, y_start, evilShores[hod-1])
        self.shadowInit()
        self.shadowSetPos(x_start, y_start, hod)
        self.shoresSetPos(x_start, y_start, self.shoresGetPos(x_start, y_start) + evilShores[0])

        debugInfo(641)

        while hod <= min(evil_step, evilShoresNum):
            shore = evilShores[hod-1]
            for indexNum in range(len(points)):
                x, y = points[indexNum]
                for dx, dy in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                    wall = self.backgroundGetPos(x + dx, y + dy)
                    shadow = self.shadowGetPos(x + dx, y + dy)
                    
                    if wall == 0 and shadow == 0:
                        self.shadowSetPos(x + dx, y + dy, hod)
                        pointsNew.append((x + dx, y + dy))
                        pointsNewNum = pointsNewNum + 1
                        self.shoresSetPos(x + dx, y + dy, self.shoresGetPos(x + dx, y + dy) + shore)

                        pointsAll.append((x + dx, y + dy, hod))

            if pointsNewNum == 0:
                break

            hod = hod + 1
            points = pointsNew
            # pointsNum = pointsNewNum

        # self.printShadow()

        #Если до хвоста недалеко, то рассмотреть возможность откусить хвост
        find = 0
        minHod = 100
        minX2 = 0
        minY2 = 0
        minIndex = 100
        if self.snake.Length > 2:
            for index in range(0, len(self.snake.coordinates)): 
                x, y = self.snake.coordinates[index]
                for indexNum in range(len(pointsAll)): 
                    x2, y2, hod = pointsAll[indexNum]
                    if x2 == x and y2 == y:
                        if hod <= minHod:
                            minX2 = x2
                            minY2 = y2
                            find = 1
                            minIndex = min(minIndex, index)
                            minHod = hod
            if find == 1:      
                DlinaOtkusa = self.snake.Length - minIndex - minHod
                
                if minHod < 4 and minHod > 1: 
                    for index2 in range(3, len(self.snake.coordinates)): 
                        x, y = self.snake.coordinates[index2]
                        self.shoresSetPos(x + dx, y + dy, self.shoresGetPos(x + dx, y + dy) + Constants.SHORE_MY_SNAKE_OTKUS)
                #Это лишнее так как вокруг змеи и так будут отрицательные очки        
                # if minHod < 6 and (DlinaOtkusa > (self.snake.Length // 2)):
                #     for index2 in range(3, len(self.snake.coordinates)): 
                #         x, y = self.snake.coordinates[index]
                #         self.shoresSetPos(x + dx, y + dy, self.shoresGetPos(x + dx, y + dy) + Constants.SHORE_MY_SNAKE_OTKUS)




    def shadowInit(self):
        self._shadow.clear() 
        for n in range(self._len):
            self._shadow.append(0)

    def shadowGetPos(self, x, y):
        return self._shadow[x + y * self._size]

    def shadowSetPos(self, x, y, value):
        self._shadow[x + y * self._size] = value

    def backgroundGetPos(self, x, y):
        return self._background[x + y * self._size]

    def backgroundSetPos(self, x, y, value):
        self._background[x + y * self._size] = value

    def elementsGetPos(self, x, y):
        return self._elements[x + y * self._size]

    def elementsSetPos(self, x, y, value):
        self._elements[x + y * self._size] = value

    def shoresGetPos(self, x, y):
        return self._shores[x + y * self._size]

    def shoresSetPos(self, x, y, value):
        self._shores[x + y * self._size] = value

    def shoresEvilGetPos(self, x, y):
        return self._shores[x + y * self._size]

    def shoresvSetPos(self, x, y, value):
        self._shores[x + y * self._size] = value


    def snakeDirectionOfHead(self, enemySnake):
        debugInfo(695)
        for i, j in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            elSnake = self.get_element_at(self._strpos2pt(self._xy2strpos(enemySnake.x + i, enemySnake.y + j)))._char
            #Поиск где возможные следующие координаты
            if ((i, j) == (-1, 0) 
                and ((elSnake == Constants.ENEMY_BODY_RIGHT_UP or elSnake == Constants.ENEMY_BODY_RIGHT_DOWN
                or elSnake == Constants.ENEMY_BODY_HORIZONTAL or elSnake == Constants.ENEMY_TAIL_END_LEFT
                or elSnake == Constants.BODY_RIGHT_UP or elSnake == Constants.BODY_RIGHT_DOWN
                or elSnake == Constants.BODY_HORIZONTAL or elSnake == Constants.TAIL_END_LEFT))): 
                enemySnake.head = Mapping.SNAKE_RIGHT
            elif ((i, j) == (+1, 0)
                and ((elSnake == Constants.ENEMY_BODY_HORIZONTAL or elSnake == Constants.ENEMY_TAIL_END_RIGHT 
                or elSnake == Constants.ENEMY_BODY_LEFT_UP or elSnake == Constants.ENEMY_BODY_LEFT_DOWN
                or elSnake == Constants.BODY_HORIZONTAL or elSnake == Constants.TAIL_END_RIGHT
                or elSnake == Constants.BODY_LEFT_UP or elSnake == Constants.BODY_LEFT_DOWN))): 
                enemySnake.head = Mapping.SNAKE_LEFT
            elif ((i, j) == (0, -1)
                and ((elSnake == Constants.ENEMY_BODY_VERTICAL or elSnake == Constants.ENEMY_TAIL_END_UP 
                or elSnake == Constants.ENEMY_BODY_LEFT_DOWN or elSnake == Constants.ENEMY_BODY_RIGHT_DOWN
                or elSnake == Constants.BODY_VERTICAL or elSnake == Constants.TAIL_END_UP
                or elSnake == Constants.BODY_LEFT_DOWN or elSnake == Constants.BODY_RIGHT_DOWN))): 
                enemySnake.head = Mapping.SNAKE_DOWN
            elif ((i, j) == (0, +1)
                and ((elSnake == Constants.ENEMY_BODY_VERTICAL or elSnake == Constants.ENEMY_TAIL_END_DOWN 
                or elSnake == Constants.ENEMY_BODY_LEFT_UP or elSnake == Constants.ENEMY_BODY_RIGHT_UP
                or elSnake == Constants.BODY_VERTICAL or elSnake == Constants.TAIL_END_DOWN
                or elSnake == Constants.BODY_LEFT_UP or elSnake == Constants.BODY_RIGHT_UP))): 
                enemySnake.head = Mapping.SNAKE_UP


    def snakeCalulateLen(self, snake):
        tmpLenght = 1
        debugInfo(727)
        lastFind = snake.head
        x = snake.x
        y = snake.y

        snake.coordinates.append((x, y))

        while 1 == 1:
            if lastFind == Mapping.SNAKE_UP:
                dx, dy = (0, 1)
            elif lastFind == Mapping.SNAKE_DOWN:
                dx, dy = (0, -1)    
            elif lastFind == Mapping.SNAKE_LEFT:
                dx, dy = (1, 0)    
            elif lastFind == Mapping.SNAKE_RIGHT:
                dx, dy = (-1, 0)
            else:
                snake.Length = max(tmpLenght, 2)
                break

            x = x + dx
            y = y + dy

            elSnake = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))._char

            findNext = 0

            if (lastFind == Mapping.SNAKE_RIGHT
                and (elSnake == Constants.ENEMY_BODY_RIGHT_UP or elSnake == Constants.ENEMY_BODY_RIGHT_DOWN
                or elSnake == Constants.ENEMY_BODY_HORIZONTAL or elSnake == Constants.ENEMY_TAIL_END_LEFT
                or elSnake == Constants.BODY_RIGHT_UP or elSnake == Constants.BODY_RIGHT_DOWN
                or elSnake == Constants.BODY_HORIZONTAL or elSnake == Constants.TAIL_END_LEFT)): 
                    findNext = 1
                    snake.coordinates.append((x, y))
                    if elSnake == Constants.ENEMY_BODY_RIGHT_UP:
                        lastFind = Mapping.SNAKE_DOWN
                    elif elSnake == Constants.ENEMY_BODY_RIGHT_DOWN:
                        lastFind = Mapping.SNAKE_UP
                    elif elSnake == Constants.BODY_RIGHT_UP:
                        lastFind = Mapping.SNAKE_DOWN
                    elif elSnake == Constants.BODY_RIGHT_DOWN:
                        lastFind = Mapping.SNAKE_UP
            elif (lastFind == Mapping.SNAKE_LEFT
                and (elSnake == Constants.ENEMY_BODY_HORIZONTAL or elSnake == Constants.ENEMY_TAIL_END_RIGHT 
                or elSnake == Constants.ENEMY_BODY_LEFT_UP or elSnake == Constants.ENEMY_BODY_LEFT_DOWN
                or elSnake == Constants.BODY_HORIZONTAL or elSnake == Constants.TAIL_END_RIGHT
                or elSnake == Constants.BODY_LEFT_UP or elSnake == Constants.BODY_LEFT_DOWN)):
                    findNext = 1
                    snake.coordinates.append((x, y))
                    if elSnake == Constants.ENEMY_BODY_LEFT_UP:
                        lastFind = Mapping.SNAKE_DOWN
                    elif elSnake == Constants.ENEMY_BODY_LEFT_DOWN:
                        lastFind = Mapping.SNAKE_UP
                    elif elSnake == Constants.BODY_LEFT_UP:
                        lastFind = Mapping.SNAKE_DOWN
                    elif elSnake == Constants.BODY_LEFT_DOWN:
                        lastFind = Mapping.SNAKE_UP
            elif (lastFind == Mapping.SNAKE_DOWN
                and (elSnake == Constants.ENEMY_BODY_VERTICAL or elSnake == Constants.ENEMY_TAIL_END_UP 
                or elSnake == Constants.ENEMY_BODY_LEFT_DOWN or elSnake == Constants.ENEMY_BODY_RIGHT_DOWN
                or elSnake == Constants.BODY_VERTICAL or elSnake == Constants.TAIL_END_UP
                or elSnake == Constants.BODY_LEFT_DOWN or elSnake == Constants.BODY_RIGHT_DOWN)):
                    findNext = 1  
                    snake.coordinates.append((x, y))
                    if elSnake == Constants.ENEMY_BODY_RIGHT_DOWN:
                        lastFind = Mapping.SNAKE_LEFT
                    elif elSnake == Constants.ENEMY_BODY_LEFT_DOWN:
                        lastFind = Mapping.SNAKE_RIGHT
                    elif elSnake == Constants.BODY_RIGHT_DOWN:
                        lastFind = Mapping.SNAKE_LEFT
                    elif elSnake == Constants.BODY_LEFT_DOWN:
                        lastFind = Mapping.SNAKE_RIGHT
            elif (lastFind == Mapping.SNAKE_UP
                and (elSnake == Constants.ENEMY_BODY_VERTICAL or elSnake == Constants.ENEMY_TAIL_END_DOWN 
                or elSnake == Constants.ENEMY_BODY_LEFT_UP or elSnake == Constants.ENEMY_BODY_RIGHT_UP
                or elSnake == Constants.BODY_VERTICAL or elSnake == Constants.TAIL_END_DOWN
                or elSnake == Constants.BODY_LEFT_UP or elSnake == Constants.BODY_RIGHT_UP)):
                    findNext = 1  
                    snake.coordinates.append((x, y))
                    if elSnake == Constants.ENEMY_BODY_LEFT_UP:
                        lastFind = Mapping.SNAKE_RIGHT
                    elif elSnake == Constants.ENEMY_BODY_RIGHT_UP:
                        lastFind = Mapping.SNAKE_LEFT
                    elif elSnake == Constants.BODY_LEFT_UP:
                        lastFind = Mapping.SNAKE_RIGHT
                    elif elSnake == Constants.BODY_RIGHT_UP:
                        lastFind = Mapping.SNAKE_LEFT

            if findNext > 0:
                tmpLenght = tmpLenght + 1
            else:
                break    

            # Если элемент хвост, значит дальше считать не нужно        
            if (elSnake == Constants.ENEMY_TAIL_END_LEFT or elSnake == Constants.ENEMY_TAIL_END_RIGHT 
              or elSnake == Constants.ENEMY_TAIL_END_UP or elSnake == Constants.ENEMY_TAIL_END_DOWN
              or elSnake == Constants.TAIL_END_LEFT or elSnake == Constants.TAIL_END_RIGHT
              or elSnake == Constants.TAIL_END_UP or elSnake == Constants.TAIL_END_DOWN):
                break


        debugInfo(828)

        snake.Length = tmpLenght

        # self._shadowInit()

        # # Поиск элементов на карте и запись в массивы
        # for x in range(0, self._len // self._size):
        #     for y in range(0, self._size):
        #         el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))

        # self.shadowSetPos(snake.x, snake.y, 1)

        # len = 1

    # def __copy__(self):
    #     new = Pole
    #     new._string = self._string
    #     new._map = []
    #     new._len = self._len
    #     new._size = self._size
    #     for n in range(self._len):
    #         new._map.append(self._map[n])
    #     return new   

    def getValueMapPos(self, x, y):
        return self.get_element_at(self._strpos2pt(self._xy2strpos(x, y))).get_char()

    def read(self):

        round.time = round.time + 1 # Необходимо считать время раунда  

        numSnakeMySleep = 0 #Моя спит
        numSnakeEnemySleep = 0 #Чужая спит
        numSnakeMyEvil = 0 #Чужая яростная
        numSnakeEnemyEvil = 0 #Количетсво чужик в ярости
        numSnakeMy = 0 #Моя ползает
        numSnakeEnemy = 0 #Количество чужих ползает в обычном состоянии

        lengthSnakeMy = 0 #Длина моей змейки

        #Еще есть состояния змеек убиты - я их пока не подсчитываю, так как не нужно

        numFuryPill = 0 #Количество ярости на поле
        # numStone = 0 #Количество камней на поле
        # numAplle = 0 #Количество яблок на поле

        # Поиск элементов на карте и запись в массивы
        for x in range(0, self._len // self._size):
            for y in range(0, self._size):
                el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))

                if el._char == Constants.NONE:
                    а = 1
                elif el == Element('WALL'):
                    а = 1
                # Моя змея
                elif el == Element('HEAD_SLEEP') or el == Element('HEAD_DEAD'):
                    numSnakeMySleep = numSnakeMySleep + 1
                    self.snake.x = x
                    self.snake.y = y
                    self.snake.slep = 1
                    lengthSnakeMy = lengthSnakeMy + 1 # Длина

                elif (el == Element('HEAD_DOWN') or el == Element('HEAD_LEFT')
                  or el == Element('HEAD_RIGHT') or el == Element('HEAD_UP')): #С поворотом головы отдельно может пригодится
                    numSnakeMy = numSnakeMy + 1
                    lengthSnakeMy = lengthSnakeMy + 1 # Длина
                    self.snake.x = x
                    self.snake.y = y
                    # if el == Element('HEAD_DOWN'):
                    #     self.snake.head = Mapping.SNAKE_DOWN
                    # elif el == Element('HEAD_UP'):
                    #     self.snake.head = Mapping.SNAKE_UP
                    # elif el == Element('HEAD_LEFT'):
                    #     self.snake.head = Mapping.SNAKE_LEFT
                    # elif el == Element('HEAD_RIGHT'):
                    #     self.snake.head = Mapping.SNAKE_RIGHT

                elif el == Element('HEAD_EVIL'):
                    lengthSnakeMy = lengthSnakeMy + 1 # Длина
                    numSnakeMyEvil = numSnakeMyEvil + 1
                    self.snake.x = x
                    self.snake.y = y
                    self.snake.SnakeEvil = 1

                elif (el == Element('TAIL_END_DOWN') or el == Element('TAIL_END_LEFT')
                 or el == Element('TAIL_END_UP') or el == Element('TAIL_END_RIGHT')
                 or el == Element('BODY_HORIZONTAL') or el == Element('BODY_VERTICAL')
                 or el == Element('BODY_LEFT_DOWN') or el == Element('BODY_LEFT_UP')
                 or el == Element('BODY_RIGHT_DOWN') or el == Element('BODY_RIGHT_UP')):
                    lengthSnakeMy = lengthSnakeMy + 1 # Длина


                # Чужие змеи
                elif el == Element('START_FLOOR') or el == Element('ENEMY_HEAD_SLEEP'):
                    numSnakeEnemySleep = numSnakeEnemySleep + 1


                elif (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT')
                 or el == Element('ENEMY_HEAD_RIGHT') or el == Element('ENEMY_HEAD_UP')):
                    numSnakeEnemy = numSnakeEnemy + 1
                    enemySnake = Snake()
                    enemySnake.x = x
                    enemySnake.y = y
                    # if el == Element('ENEMY_HEAD_DOWN'):
                    #     enemySnake.head = Mapping.SNAKE_DOWN
                    # elif el == Element('ENEMY_HEAD_UP'):
                    #     enemySnake.head = Mapping.SNAKE_UP
                    # elif el == Element('ENEMY_HEAD_LEFT'):
                    #     enemySnake.head = Mapping.SNAKE_LEFT
                    # elif el == Element('ENEMY_HEAD_RIGHT'):
                    #     enemySnake.head = Mapping.SNAKE_RIGHT
                    self.enemySnake.append(enemySnake)

                elif el == Element('ENEMY_HEAD_EVIL'):
                    numSnakeEnemyEvil = numSnakeEnemyEvil + 1
                    enemySnake = Snake()
                    enemySnake.x = x
                    enemySnake.y = y
                    enemySnake.SnakeEvil = 1
                    self.enemySnake.append(enemySnake)

                elif el == Element('FURY_PILL'):
                    numFuryPill = numFuryPill + 1
                    newFury = (x, y)
                    self.furyPill.append(newFury)

                elif el == Element('APPLE'):
                    newApple = (x, y)
                    self.apples.append(newApple)

                elif el == Element('STONE'):
                    newStone = (x, y)
                    self.stones.append(newStone)

                elif el == Element('GOLD'):
                    newGold = (x, y)
                    self.golds.append(newGold)

        if numSnakeMySleep > 0:
            round.newRound()

        #Запишем время раунда
        self.time = round.time

        #Если нет живой змеи, выходим    
        if self.snake.x == 0 and self.snake.y == 0:
            return

        # Получить для других змей остаток ходов ярости с прошлого хода
        for indexSnake in range(len(self.enemySnake)): 
            tmpSnake = self.enemySnake[indexSnake]
            if tmpSnake.SnakeEvilStep > 0: # Если змея в ярости
                for indexOldSnake in range(len(round.enemySnakes)):
                    tmpOldSnake = round.enemySnakes[indexOldSnake]
                    if tmpOldSnake.SnakeEvil == 1: # Если змея в прошлом ходу была в ярости

                        # Получение ранее сохраненных возможных перемещений    
                        for numXY in range(len(tmpOldSnake.nextXY)):
                            x, y = tmpOldSnake.nextXY[numXY]
                            if tmpSnake.x == x and tmpSnake.y == y:
                                tmpSnake.SnakeEvilStep = tmpSnake.SnakeEvilStep + tmpOldSnake.SnakeEvilStep
                                break

                    # Проверяем если на месте змеи раньше была бутылка ярости  
                    for numFury in range(len(tmpOldSnake.nearFury)):
                        x, y = tmpOldSnake.nearFury[numFury]
                        if tmpSnake.x == x and tmpSnake.y == y:
                            tmpSnake.SnakeEvilStep = tmpSnake.SnakeEvilStep + Constants.FURY_PILL_STEP_NUM
                            break

                # Каждый ход вычитаем по одной единице ярости                
                tmpSnake.SnakeEvilStep = tmpSnake.SnakeEvilStep - 1

        # Получить для своей змеи остаток ходов ярости с прошлого хода
        if self.snake.SnakeEvil == 1:
            # Каждый ход вычитаем по одной единице ярости               
            self.snake.SnakeEvilStep = self.snake.SnakeEvilStep - 1

            if round.snake.SnakeEvil == 1: # Если змея в прошлом ходу была в ярости
                # Получение ранее сохраненных возможных перемещений    
                self.snake.SnakeEvilStep = self.snake.SnakeEvilStep + round.snake.SnakeEvilStep

            # Проверяем если на месте змеи раньше была бутылка ярости  
            for numFury in range(len(round.snake.nearFury)):
                x, y = round.snake.nearFury[numFury]
                if self.snake.x == x and self.snake.y == y:
                    # На этом шаге остаток получается 9 ходов возможно нужно прибавлять один
                    self.snake.SnakeEvilStep = self.snake.SnakeEvilStep + Constants.FURY_PILL_STEP_NUM 
                    break


        # X - по горизонтали Y - по вертикали
        # Определим направление змей
        # Запишем возможные координаты на следующий ход, их направление
        # Запишем есть ли рядом бутылочки ярости
        for indexSnake in range(len(self.enemySnake)): 
            enemySnake = self.enemySnake[indexSnake]
            
            self.snakeDirectionOfHead(enemySnake)

            for i, j in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
                elSnake = self.get_element_at(self._strpos2pt(self._xy2strpos(enemySnake.x + i, enemySnake.y + j)))
                #Поиск где возможные следующие координаты
                # if ((i, j) == (-1, 0) 
                #   and ((elSnake == Element('ENEMY_BODY_RIGHT_UP') or elSnake == Element('ENEMY_BODY_RIGHT_DOWN')
                #   or elSnake == Element('ENEMY_BODY_HORIZONTAL') or elSnake == Element('ENEMY_TAIL_END_LEFT')))): 
                #     enemySnake.head = Mapping.SNAKE_RIGHT
                # elif ((i, j) == (+1, 0)
                #   and ((elSnake == Element('ENEMY_BODY_HORIZONTAL') or elSnake == Element('ENEMY_TAIL_END_RIGHT') 
                #   or elSnake == Element('ENEMY_BODY_LEFT_UP') or elSnake == Element('ENEMY_BODY_LEFT_DOWN')))):
                #     enemySnake.head = Mapping.SNAKE_LEFT
                # elif ((i, j) == (0, -1)
                #   and ((elSnake == Element('ENEMY_BODY_VERTICAL') or elSnake == Element('ENEMY_TAIL_END_UP') 
                #   or elSnake == Element('ENEMY_BODY_LEFT_DOWN') or elSnake == Element('ENEMY_BODY_RIGHT_DOWN')))):
                #     enemySnake.head = Mapping.SNAKE_DOWN
                # elif ((i, j) == (0, +1)
                #   and ((elSnake == Element('ENEMY_BODY_VERTICAL') or elSnake == Element('ENEMY_TAIL_END_DOWN') 
                #   or elSnake == Element('ENEMY_BODY_LEFT_UP') or elSnake == Element('ENEMY_BODY_RIGHT_UP')))):
                #     enemySnake.head = Mapping.SNAKE_UP
                # else:
                enemySnake.nextXY.append((enemySnake.x + i, enemySnake.y + j))
                if elSnake == Element('FURY_PILL'):
                    enemySnake.nearFury.append((enemySnake.x + i, enemySnake.y + j))
        
        # Определим направление моей змеи
        self.snakeDirectionOfHead(self.snake)
        
        # Запишем есть ли рядом бутылочки ярости с моей змейкой
        for i, j in [(-1, 0), (+1, 0), (0, -1), (0, +1)]:
            elSnake = self.get_element_at(self._strpos2pt(self._xy2strpos(self.snake.x + i, self.snake.y + j)))
            if elSnake == Element('FURY_PILL'):
                self.snake.nearFury.append((self.snake.x + i, self.snake.y + j))

        if round.time > 40:
            f = 1

        # Написать функцию класса, которая подсчитывает длину змеи на карте
        self.snake.Length = lengthSnakeMy # Длина моей змеи
        if self.snake.slep == 0:
            self.snakeCalulateLen(self.snake)
        if (self.snake.Length != lengthSnakeMy):
            print("Не совпадает расчетная длина змеи подсчитанная двумя разными способами")

        for indexSnake in range(len(self.enemySnake)): 
            tmpSnake = self.enemySnake[indexSnake]
            self.snakeCalulateLen(tmpSnake)

        # Запишем данные для использования в следующем ходу
        self.snake.copySnake(round.snake)
        round.enemySnakes.clear() 
        for i in range(len(self.enemySnake)):
            tmpSnake = Snake()
            self.enemySnake[i].copySnake(tmpSnake)
            round.enemySnakes.append(tmpSnake)

    def printSnakesInfo(self):
        print("Round time = ", round.time)
        print("My snake x = ", self.snake.x, ", y = ", self.snake.y, " len = ", self.snake.Length, " evil = ", self.snake.SnakeEvil, ", stepOverEvil = ", self.snake.SnakeEvilStep)

        for indexSnake in range(len(self.enemySnake)): 
            tmpSnake = self.enemySnake[indexSnake]
            print("Snake Enemy (",indexSnake,") x = ", tmpSnake.x, ", y = ", tmpSnake.y, " len = ", tmpSnake.Length, " evil = ", tmpSnake.SnakeEvil, ", stepOverEvil = ", tmpSnake.SnakeEvilStep)

    def full_map(self):
        if snake.SnakeEvil == 1:
           snake.SnakeEvilStep = snake.SnakeEvilStep - 1                     

        # Проверка змейки
        snake.otherSnakeEvil = 0 
        for x in range(0, self._len // self._size):
            for y in range(0, self._size):
                el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))

                if el == Element('HEAD_EVIL'):
                    if snake.SnakeEvil == 0:
                        snake.SnakeEvil = 1
                        snake.SnakeEvilStep = 10

                if (el == Element('HEAD_DOWN') or el == Element('HEAD_LEFT')
                     or el == Element('HEAD_RIGHT') or el == Element('HEAD_UP')):
                    snake.SnakeEvil = 0
                    snake.SnakeEvilStep = 0

                if el == Element('ENEMY_HEAD_EVIL'):
                    snake.otherSnakeEvil = 1

        if snake.SnakeEvil == 1:
            print("================================ ++++++++++++++++++++", snake.SnakeEvilStep) 


        #подсчет длины змей
        snake.Length = 0
        snake.EnemyLength = 0
        for x in range(0, self._len // self._size):
            for y in range(0, self._size):
                el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))

                if (el == Element('HEAD_DOWN') or el == Element('HEAD_LEFT')
                     or el == Element('HEAD_RIGHT') or el == Element('HEAD_UP')
                     or el == Element('HEAD_EVIL') or el == Element('TAIL_END_DOWN')
                     or el == Element('TAIL_END_LEFT') or el == Element('TAIL_END_UP')
                     or el == Element('TAIL_END_RIGHT') or el == Element('BODY_HORIZONTAL')
                     or el == Element('BODY_VERTICAL') or el == Element('BODY_LEFT_DOWN')
                     or el == Element('BODY_LEFT_UP') or el == Element('BODY_RIGHT_DOWN')
                     or el == Element('BODY_RIGHT_UP')):
                        snake.Length = snake.Length + 1
                     
                if (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT')
                     or el == Element('ENEMY_HEAD_RIGHT') or el == Element('ENEMY_HEAD_UP')
                     or el == Element('ENEMY_HEAD_DEAD') or el == Element('ENEMY_HEAD_EVIL')
                     or el == Element('ENEMY_TAIL_END_DOWN') or el == Element('ENEMY_TAIL_END_LEFT')
                     or el == Element('ENEMY_TAIL_END_UP') or el == Element('ENEMY_TAIL_END_RIGHT')
                     or el == Element('ENEMY_BODY_HORIZONTAL') or el == Element('ENEMY_BODY_VERTICAL')
                     or el == Element('ENEMY_BODY_LEFT_DOWN') or el == Element('ENEMY_BODY_LEFT_UP')
                     or el == Element('ENEMY_BODY_RIGHT_DOWN') or el == Element('ENEMY_BODY_RIGHT_UP')):
                        snake.EnemyLength = snake.EnemyLength + 1
                     
        # Проверим необходимость выбросить камень             


        # заполнение поля
        for x in range(0, self._len // self._size):
            for y in range(0, self._size):
                el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))

                if el == Element('WALL') or el == Element('HEAD_DEAD') or el == Element('START_FLOOR'):
                    self._setPos(x, y, Mapping.MAP_WALL)
                    self._setPosE(x, y, Mapping.MAP_WALL)

                if el == Element('STONE'):
                    self._setPos(x, y, -1)
                    self._setPosE(x, y, -1)

                if (el == Element('HEAD_DOWN') or el == Element('HEAD_LEFT')
                     or el == Element('HEAD_RIGHT') or el == Element('HEAD_UP')):
                    self._setPos(x, y, Mapping.MAP_SNAKE_HEAD)
                    self._setPosE(x, y, Mapping.MAP_SNAKE_HEAD)


                if (el == Element('HEAD_EVIL')
                     or el == Element('HEAD_FLY') or el == Element('HEAD_SLEEP')):
                    self._setPos(x, y, Mapping.MAP_WALL)
                    self._setPosE(x, y, Mapping.MAP_WALL)


                if (el == Element('BODY_HORIZONTAL') or el == Element('BODY_VERTICAL')
                     or el == Element('BODY_LEFT_DOWN') or el == Element('BODY_LEFT_UP')
                         or el == Element('BODY_RIGHT_DOWN') or el == Element('BODY_RIGHT_UP')):
                    self._setPos(x, y, 99)
                    self._setPosE(x, y, 99)

                # Туловише и хвост тебя
                if (el == Element('TAIL_END_DOWN') or el == Element('TAIL_END_LEFT') or el == Element('TAIL_END_UP')
                    or el == Element('TAIL_END_RIGHT') or el == Element('TAIL_INACTIVE')
                    or el == Element('BODY_HORIZONTAL') or el == Element('BODY_VERTICAL')
                    or el == Element('BODY_LEFT_DOWN') or el == Element('BODY_LEFT_UP')
                    or el == Element('BODY_RIGHT_DOWN') or el == Element('BODY_RIGHT_UP')):
                    self._setPos(x, y, 99)
                    self._setPosE(x, y, 99)

                # Головы противников
                if (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT') or el == Element('ENEMY_HEAD_RIGHT')
                    or el == Element('ENEMY_HEAD_UP') or el == Element('ENEMY_HEAD_DEAD')
                    or el == Element('ENEMY_HEAD_EVIL') or el == Element('ENEMY_HEAD_FLY')
                    or el == Element('ENEMY_HEAD_SLEEP') or el == Element('ENEMY_HEAD_FLY')):
                    self._setPos(x, y, -2)
                    self._setPosE(x, y, -2)

                # Хвосты и Туловища противников
                if (el == Element('ENEMY_TAIL_END_DOWN') or el == Element('ENEMY_TAIL_END_LEFT') or el == Element('ENEMY_TAIL_END_UP')
                    or el == Element('ENEMY_TAIL_END_RIGHT') or el == Element('ENEMY_TAIL_INACTIVE')
                    or el == Element('ENEMY_BODY_HORIZONTAL') or el == Element('ENEMY_BODY_VERTICAL')
                    or el == Element('ENEMY_BODY_LEFT_DOWN') or el == Element('ENEMY_BODY_LEFT_UP')
                    or el == Element('ENEMY_BODY_RIGHT_DOWN') or el == Element('ENEMY_BODY_RIGHT_UP')):
                    self._setPos(x, y, -2)
                    self._setPosE(x, y, -2)

                if (snake.Length - snake.EnemyLength > 4) and snake.EnemyLength > 4: #Режим змейки-убийцы нет смысла гонятся за маленькой змейкой


                    if snake.SnakeEvil == 1 and snake.SnakeEvilStep > 1:
                        if el == Element('APPLE'):
                            self._setPos(x, y, Mapping.MAP_ZERO)
                            self._setPosE(x, y, Mapping.MAP_ZERO)

                        if el == Element('GOLD'):
                            self._setPos(x, y, Mapping.MAP_ZERO)
                            self._setPosE(x, y, Mapping.MAP_ZERO)

                        if el == Element('FURY_PILL'):
                            self._setPos(x, y, Mapping.MAP_APPLE)
                            self._setPosE(x, y, Mapping.MAP_APPLE)

                        if el == Element('STONE'):
                            self._setPos(x, y, Mapping.MAP_APPLE)
                            self._setPosE(x, y, Mapping.MAP_APPLE)

                        if (el == Element('ENEMY_BODY_HORIZONTAL') or el == Element('ENEMY_BODY_VERTICAL') 
                          or el == Element('ENEMY_BODY_LEFT_DOWN') or el == Element('ENEMY_BODY_LEFT_UP')
                          or el == Element('ENEMY_BODY_RIGHT_DOWN') or el == Element('ENEMY_BODY_RIGHT_UP')):
                                self._setPos(x, y, Mapping.MAP_APPLE)
                                self._setPosE(x, y, Mapping.MAP_APPLE)

                        if (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT') 
                          or el == Element('ENEMY_HEAD_RIGHT') or el == Element('ENEMY_HEAD_UP')):
                                self._setPos(x, y, Mapping.MAP_APPLE)
                                self._setPosE(x, y, Mapping.MAP_APPLE)

                        if (snake.SnakeEvil == 1 and snake.SnakeEvilStep > 1 and
                            (el == Element('ENEMY_TAIL_END_DOWN') or el == Element('ENEMY_TAIL_END_LEFT') 
                                or el == Element('ENEMY_TAIL_END_UP') or el == Element('ENEMY_TAIL_END_RIGHT'))):
                                    self._setPos(x, y, Mapping.MAP_ZERO)
                                    self._setPosE(x, y, Mapping.MAP_ZERO)


                    else:

                        if el == Element('APPLE'):
                            self._setPos(x, y, Mapping.MAP_APPLE)
                            self._setPosE(x, y, Mapping.MAP_APPLE)

                        if el == Element('GOLD'):
                            self._setPos(x, y, Mapping.MAP_APPLE)
                            self._setPosE(x, y, Mapping.MAP_APPLE)

                        if el == Element('STONE'):
                            self._setPos(x, y, Mapping.MAP_APPLE)
                            self._setPosE(x, y, Mapping.MAP_APPLE)

                        if el == Element('FURY_PILL'):
                            self._setPos(x, y, Mapping.MAP_APPLE)
                            self._setPosE(x, y, Mapping.MAP_APPLE)

                        if snake.otherSnakeEvil == 0:
                            if (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT') 
                            or el == Element('ENEMY_HEAD_RIGHT') or el == Element('ENEMY_HEAD_UP')):
                                    self._setPos(x, y, Mapping.MAP_APPLE)
                                    self._setPosE(x, y, Mapping.MAP_APPLE)
                            # if (el == Element('ENEMY_BODY_HORIZONTAL') or el == Element('ENEMY_BODY_VERTICAL') 
                            #   or el == Element('ENEMY_BODY_LEFT_DOWN') or el == Element('ENEMY_BODY_LEFT_UP')
                            #   or el == Element('ENEMY_BODY_RIGHT_DOWN') or el == Element('ENEMY_BODY_RIGHT_UP')):
                            #         self._setPos(x, y, Mapping.MAP_APPLE)
                            #         self._setPosE(x, y, Mapping.MAP_APPLE)

                else:    

                    # Тестово расставил яблоки
                    if snake.SnakeEvil == 0 and el == Element('APPLE'):
                        self._setPos(x, y, Mapping.MAP_APPLE)
                        self._setPosE(x, y, Mapping.MAP_APPLE)
                    else:
                        self._setPos(x, y, Mapping.MAP_ZERO)
                        self._setPosE(x, y, Mapping.MAP_ZERO)

                    if snake.SnakeEvil == 0 and el == Element('GOLD'):
                        self._setPos(x, y, Mapping.MAP_APPLE)
                        self._setPosE(x, y, Mapping.MAP_APPLE)
                    else:
                        self._setPos(x, y, Mapping.MAP_ZERO)
                        self._setPosE(x, y, Mapping.MAP_ZERO)

                    # if snake.SnakeEvil == 0 and el == Element('FURY_PILL'):
                    if el == Element('FURY_PILL'):
                        self._setPos(x, y, Mapping.MAP_APPLE)
                        self._setPosE(x, y, Mapping.MAP_APPLE)

                    if snake.SnakeEvil == 1 and snake.SnakeEvilStep > 1 and el == Element('STONE'):
                        self._setPos(x, y, Mapping.MAP_APPLE)
                        self._setPosE(x, y, Mapping.MAP_APPLE)

                    if (snake.SnakeEvil == 1 and snake.SnakeEvilStep > 2 and
                        (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT') 
                            or el == Element('ENEMY_HEAD_RIGHT') or el == Element('ENEMY_HEAD_UP')
                            or el == Element('ENEMY_BODY_HORIZONTAL') or el == Element('ENEMY_BODY_VERTICAL')
                            or el == Element('ENEMY_BODY_LEFT_DOWN') or el == Element('ENEMY_BODY_LEFT_UP')
                            or el == Element('ENEMY_BODY_RIGHT_DOWN') or el == Element('ENEMY_BODY_RIGHT_UP')
                            or el == Element('ENEMY_BODY_RIGHT_DOWN') or el == Element('ENEMY_BODY_RIGHT_UP'))):
                                self._setPos(x, y, Mapping.MAP_APPLE)
                                self._setPosE(x, y, Mapping.MAP_APPLE)

                    if (snake.SnakeEvil == 1 and snake.SnakeEvilStep > 1 and
                        (el == Element('ENEMY_TAIL_END_DOWN') or el == Element('ENEMY_TAIL_END_LEFT') 
                            or el == Element('ENEMY_TAIL_END_UP') or el == Element('ENEMY_TAIL_END_RIGHT'))):
                                self._setPos(x, y, Mapping.MAP_ZERO)
                                self._setPosE(x, y, Mapping.MAP_ZERO)


        # Поиск приманок убиец
        for x in range(0, self._len // self._size):
            for y in range(0, self._size):
                if self._getPos(x,y) == Mapping.MAP_APPLE:
                    rez = self._checkNearWall(x , y)
                    if rez < 2:
                        self._setPos(x, y, Mapping.MAP_WALLDOWN)
                        self._setPosE(x, y, Mapping.MAP_WALLDOWN)
                        
        # Поиск убиец голов обычных змей и злых змеек
        if snake.SnakeEvil == 1 and snake.SnakeEvilStep > 2 and snake.otherSnakeEvil == 0:
            f = 1 #Ничего не делаем
        else:    
            for x in range(0, self._len // self._size):
                for y in range(0, self._size):
                    el = self.get_element_at(self._strpos2pt(self._xy2strpos(x, y)))

                    if (el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT') 
                        or el == Element('ENEMY_HEAD_RIGHT') or el == Element('ENEMY_HEAD_UP') or el == Element('ENEMY_HEAD_EVIL')):
                            self._setPos(x-1, y, Mapping.MAP_WALL)
                            self._setPosE(x-1, y, Mapping.MAP_WALL)
                            self._setPos(x+1, y, Mapping.MAP_WALL)
                            self._setPosE(x+1, y, Mapping.MAP_WALL)
                            self._setPos(x, y-1, Mapping.MAP_WALL)
                            self._setPosE(x, y-1, Mapping.MAP_WALL)
                            self._setPos(x, y+1, Mapping.MAP_WALL)
                            self._setPosE(x, y+1, Mapping.MAP_WALL)


    def _checkNearWall(self, x , y):
        rez = 0
        # try:
        if (self._getPos(x-1,y) == 0 or self._getPos(x-1,y) == Mapping.MAP_SNAKE_HEAD or self._getPos(x-1,y) == Mapping.MAP_APPLE):
            rez = rez + 1
        if (self._getPos(x+1,y) == 0 or self._getPos(x+1,y) == Mapping.MAP_SNAKE_HEAD or self._getPos(x+1,y) == Mapping.MAP_APPLE):
            rez = rez + 1
        if (self._getPos(x,y-1) == 0 or self._getPos(x,y-1) == Mapping.MAP_SNAKE_HEAD or self._getPos(x,y-1) == Mapping.MAP_APPLE):
            rez = rez + 1
        if (self._getPos(x,y+1) == 0 or self._getPos(x,y+1) == Mapping.MAP_SNAKE_HEAD or self._getPos(x,y+1) == Mapping.MAP_APPLE):
            rez = rez + 1
        #     except Exception as ex:
        #         print("!!!!!!!!!!!!", ex)
        return rez    


    def findElement(self, x_start, y_start):
        hod = 1
        self._setPosE(x_start, y_start, hod)
        while 0 == 0:
            goNext = 0
            for y in range(0, self._len // self._size):
                for x in range(0, self._size):
                    if self._getPosE(x,y) == hod:

                        if self._getPosE(x-1,y) == 0:
                            self._setPosE(x-1,y, hod + 1)
                            goNext = 1
                        elif self._getPosE(x-1,y) == Mapping.MAP_APPLE: # Еда 
                            return Point(x-1, y)

                        if self._getPosE(x+1,y) == 0:
                            self._setPosE(x+1,y, hod + 1)
                            goNext = 1
                        elif self._getPosE(x+1,y) == Mapping.MAP_APPLE:
                            # self.print_map()
                            return Point(x+1,y)

                        if self._getPosE(x,y-1) == 0:
                            self._setPosE(x,y-1, hod + 1)
                            goNext = 1
                        elif self._getPosE(x,y-1) == Mapping.MAP_APPLE:
                            # self.print_map()
                            return Point(x,y-1)

                        if self._getPosE(x,y+1) == 0:
                            self._setPosE(x,y+1, hod + 1)
                            goNext = 1
                        elif self._getPosE(x,y+1) == Mapping.MAP_APPLE:
                            # self.print_map()
                            return Point(x,y+1)
            if goNext == 0:
                return None

            hod = hod + 1
            if hod > 50:
                return None # слишком далеко

    def _getPos(self, x,y):
        return self._map[x + y * self._size]

    def _setPos(self, x,y, value):
        self._map[x + y * self._size] = value

    def _getPosE(self, x,y):
        return self._mapFind[x + y * self._size]

    def _setPosE(self, x,y, value):
        self._mapFind[x + y * self._size] = value

    # def _checkFinish(self, )

    def goto_finish(self, x_start, y_start, x_finish, y_finish):
        self._setPos(x_start, y_start, 92)
        hod = 1
        self._setPos(x_finish, y_finish, hod)
        while 0 == 0:
            goNext = 0
            lastAction = None
            for y in range(0, self._len // self._size):
                for x in range(0, self._size):
                    if self._getPos(x,y) == hod:

                        if self._getPos(x-1,y) == 0:
                            self._setPos(x-1,y, hod + 1)
                            goNext = 1
                        elif self._getPos(x-1,y) == 92: # Голова змеи 
                            lastAction = SnakeAction.RIGHT
                            # self.print_map()
                            return (hod + 1, lastAction)

                        if self._getPos(x+1,y) == 0:
                            self._setPos(x+1,y, hod + 1)
                            goNext = 1
                        elif self._getPos(x+1,y) == 92:
                            lastAction = SnakeAction.LEFT
                            # self.print_map()
                            return (hod + 1, lastAction)

                        if self._getPos(x,y-1) == 0:
                            self._setPos(x,y-1, hod + 1)
                            goNext = 1
                        elif self._getPos(x,y-1) == 92:
                            lastAction = SnakeAction.DOWN
                            # self.print_map()
                            return (hod + 1, lastAction)

                        if self._getPos(x,y+1) == 0:
                            self._setPos(x,y+1, hod + 1)
                            goNext = 1
                        elif self._getPos(x,y+1) == 92:
                            lastAction = SnakeAction.UP
                            # self.print_map()
                            return (hod + 1, lastAction)

                        # if goNext == 1 and (
                        #    ((x-1 == x_start and y == y_start) or
                        #    (x+1 == x_start and y == y_start) or
                        #     (x == x_start and y-1 == y_start) or
                        #     (x == x_start and y+1 == y_start))):
                        #         self.print_map()
                        #         return (hod + 1, lastAction)

            if goNext == 0:
                return (-1, None)

            hod = hod + 1
            if hod > 90:
                return (-2, None) # слишком далеко

    def print_map(self):
        print(self._map_by_line(0))

    def print_map_find(self):
        print(self._map_by_line(1))

    def printShores(self):
        str = "\n"
        for y in range(0, self._len // self._size):
            for x in range(0, self._size):
                num = self._shores[x + y * self._size]
                track = self._trajectory[x + y * self._size]
                numWall = self._background[x + y * self._size]

                if track > 0:
                    num = track                

                if self.snake.x == x and self.snake.y == y:
                    num_str = "@@@"
                elif numWall == Constants.BACKGROUND_WALL:
                    num_str = "###"
                elif num == 0:
                    num_str = "   "
                elif num > -10 and num < 0:
                    num_str = " " + num.__str__()
                elif num < -99:
                    num_str = "***"
                elif num <= -10:
                    num_str = "" + num.__str__()
                elif num > 0 and num < 10:
                    num_str = "  " + num.__str__()
                elif num > 9 and num < 100:
                    num_str = " " + num.__str__()
                else:        
                    num_str = num.__str__()
                str = str + num_str
            str = str + '\n'
        print(str)
 

    def printShadow(self):
        str = "\n"
        for y in range(0, self._len // self._size):
            for x in range(0, self._size):
                num = self._shadow[x + y * self._size]
                numWall = self._background[x + y * self._size]
                if self.snake.x == x and self.snake.y == y:
                    num_str = "@@@"
                elif numWall == Constants.BACKGROUND_WALL:
                    num_str = "###"
                elif num == 0:
                    num_str = "   "
                elif num > -10 and num < 0:
                    num_str = " " + num.__str__()
                elif num < -99:
                    num_str = "***"
                elif num <= -10:
                    num_str = "" + num.__str__()
                elif num > 0 and num < 10:
                    num_str = "  " + num.__str__()
                elif num > 9 and num < 100:
                    num_str = " " + num.__str__()
                else:        
                    num_str = num.__str__()
                str = str + num_str
            str = str + '\n'
        print(str)

    def _map_by_line(self, info):
        str = "\n"
        for y in range(0, self._len // self._size):
            for x in range(0, self._size):
                if info == 0:
                    num = self._map[x + y * self._size]
                else:    
                    num = self._mapFind[x + y * self._size]
                num_str = "   "
                if num == -1:
                   num_str = "###"
                elif num == -2:
                   num_str = "***"
                elif num == -9:
                   num_str = "@@@"
                elif num == 0:
                   num_str = "   "
                elif num > 0 and num < 10:
                   num_str = "  " + num.__str__()
                elif num > 9 and num < 100:
                   num_str = " " + num.__str__()
                else:
                   num_str = num.__str__()
                str = str + num_str
            str = str + '\n'    
        return str

    def may(self):
        print("Мяу!")

round = Round()
