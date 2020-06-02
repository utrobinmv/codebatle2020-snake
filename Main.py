from snakebattleclient.SnakeBattleClient import GameClient
import random
import logging
import time
import datetime

import Mapping

from snakebattleclient.internals.SnakeAction import SnakeAction
from snakebattleclient.internals.Board import Board
from snakebattleclient.internals.Element import Element
from snakebattleclient.internals.Point import Point

from Strateg import Pole

emul = 0
timeStart = 0
timeFinish = 0

fileRound = 0
fileRoundOpen = 0

logging.basicConfig(format='%(asctime)s %(levelname)s:%(message)s',
                    level=logging.INFO)


def goTo(gcb: Pole, finish: Point): # Функция перемещения из точки в точку
    if gcb.snake.x > 0: 
        print("element x = ", gcb.snake.x,", y = ", gcb.snake.y)
        # gcb._setPos(finish._x, finish._y)
        # gcb.full_map()
        # gcb.print_map()
        goLen, lastAction = gcb.goto_finish(gcb.snake.x, gcb.snake.y, finish._x, finish._y)
        # goLen, lastAction = gcb.goto_finish(gcb.snake.x, gcb.snake.y, 28, 2)
        # gcb.print_map()
        print("Go to x=", finish._x, ", y=", finish._y, "golen = ", goLen, " ======= goto " + lastAction.__str__())

        return lastAction
        # return None
   


def turn(gcb: Board):

    global fileRoundOpen
    global fileRound


    if emul == 0: #Save state
        f = open("pole.txt", "w")
        # Записываем данные доски
        f.write(gcb._string + "\n")
        f.write(gcb._size.__str__() + "\n")
        f.write(gcb._len.__str__() + "\n")
        f.close()

    else:
       gcb.print_board()     

    timeStart = datetime.datetime.now()

    try:
        pole = Pole(gcb)
    except ValueError:
        print('Ошибка1')

    try:
        pole.read() # считываем данные с поля
    except ValueError:
        print('Ошибка2')

    if emul == 0:
        if pole.time == 1:
            fileRoundOpen = 1
            fileRound = open("raunds/" + timeStart.__str__() + ".txt", "w")

        if fileRoundOpen == 1:    
            # Записываем данные доски
            fileRound.write(gcb._string + "\n")
            fileRound.write(gcb._size.__str__() + "\n")
            fileRound.write(gcb._len.__str__() + "\n")

        if fileRoundOpen == 1 and pole.time < 1:
            fileRound.close()
            fileRoundOpen = 0
        

    print("Finish " + datetime.datetime.now().__str__())

    try:
        pole.printSnakesInfo()
    except ValueError:
        print('Ошибка3')

    firstAction = SnakeAction.RIGHT

    if pole.snake.slep == 0 or not(pole.snake.x == 0 and pole.snake.y == 0):
        # try:
            napravlenie = pole.fill()
        
            if napravlenie == Mapping.SNAKE_LEFT:
                firstAction = SnakeAction.LEFT
            elif napravlenie == Mapping.SNAKE_RIGHT:
                firstAction = SnakeAction.RIGHT
            elif napravlenie == Mapping.SNAKE_UP:
                firstAction = SnakeAction.UP
            elif napravlenie == Mapping.SNAKE_DOWN:
                firstAction = SnakeAction.DOWN
        
        # except ValueError:
        #     print('Ошибка4')
    else:
        firstAction = SnakeAction.STOP    



    # return random.choice(list(SnakeAction))
    
    # point = gcb.get_point_by_shift(SnakeAction.UP)
    # wormHead = gcb.get_my_head()


    # firstAction = None

    # if pole.snake.x > 0:
    # # if isinstance(wormHead, Point): 
    #     print("head x = ", pole.snake.x,", y = ", pole.snake.y)


    #     pole.full_map()


    #     nextElement = pole.findElement(pole.snake.x, pole.snake.y)    

    #     if isinstance(nextElement, Point):
    #         firstAction = goTo(pole, nextElement)
    #     else:
    #         print("Not find next element")    


    # point = gcb.find_first_element(Element.get_char.STONE)
    # print(head)

    # nextElement = gcb.find_first_element(Element('APPLE'), Element('FURY_PILL'),
    #                                    Element('GOLD'), Element('FLYING_PILL'), Element('FURY_PILL'))

    # if isinstance(nextElement, Point): 
    #     # el = gcb.get_element_at(nextElement)
    #     print("element x = ", nextElement._x,", y = ", nextElement._y)



    if isinstance(firstAction, SnakeAction):
        nextAction = firstAction

        max = len(pole.snake.coordinates)
        if max > 1:
            x, y = pole.snake.coordinates[max - 1]
            el_tail = pole.get_element_at(pole._strpos2pt(pole._xy2strpos(x, y)))
            stone = 0
            if el_tail == Element('TAIL_END_DOWN'):
                dx = 0
                dy = +1
                stone = 1
            elif el_tail == Element('TAIL_END_LEFT'):
                dx = -1
                dy = 0
                stone = 1
            elif el_tail == Element('TAIL_END_UP'):
                dx = 0
                dy = -1
                stone = 1
            elif el_tail == Element('TAIL_END_RIGHT'):
                dx = +1
                dy = 0
                stone = 1
            if stone == 1:
                el = pole.get_element_at(pole._strpos2pt(pole._xy2strpos(x + dx, y + dy)))
                if el == Element('ENEMY_HEAD_DOWN') or el == Element('ENEMY_HEAD_LEFT')  or el == Element('ENEMY_HEAD_RIGHT')  or el == Element('ENEMY_HEAD_UP'):
                    # Бросим камень
                    if nextAction == SnakeAction.RIGHT:
                        nextAction == SnakeAction.ACT_RIGHT
                    elif nextAction == SnakeAction.LEFT:
                        nextAction == SnakeAction.ACT_LEFT
                    elif nextAction == SnakeAction.UP:
                        nextAction == SnakeAction.ACT_UP
                    elif nextAction == SnakeAction.DOWN:
                        nextAction == SnakeAction.ACT_DOWN


    else: 
        nextAction = SnakeAction.RIGHT

    if pole.snake.x <= 0:
        nextAction = SnakeAction.STOP

    print("sent: " + nextAction.__str__())

    # poleLastCourse = pole

    # nextAction = SnakeAction.LEFT

    timeFinish = datetime.datetime.now()
    raznica = timeFinish - timeStart

    print("Start " + timeStart.__str__() + ", finish " + timeFinish.__str__() + " === " + raznica.microseconds.__str__()) 
 
    if emul == 2:
        time.sleep(0)

    return nextAction


def main():

    fileRoundOpen = 0

    if emul == 1: #Load state
        f = open("pole.txt", "r")
        # Читаем данные доски
        strPole = f.readline()
        gcb = Board(strPole)
        f.close()

        turn(gcb)
    elif emul == 2: #Load state
        startStep = 0
        # f = open("raunds/2020-05-29 13:16:23.298915.txt", "r")

        #На этой карте воспроизводится какой то косяк
        # f = open("/home/joefox/Documents/2020-05-30-15-00/codebattle-snakebattle-joefox/snakebattleclient/Проиграл на -110/2020-05-30 18:35:59.508320.txt", "r")

    #Столнулись два яростных червя
    #/home/joefox/data/nextcloud/Programming/competitions/codebattle-snakebattle-joefox/snakebattleclient/raunds/2020-05-31 17:09:37.519811.txt

    #В конце не убежал от яростных змей
    
        f = open("/home/joefox/data/nextcloud/Programming/competitions/codebattle-snakebattle-joefox/snakebattleclient/raunds/2020-06-02 13:14:02.206479.txt", "r")

    #    f = open("/home/joefox/data/nextcloud/Programming/competitions/codebattle-snakebattle-joefox/snakebattleclient/raunds/2020-05-31 16:52:43.514781.txt", "r")

        num = 0
        for line in f:
            num = num + 1
            if num == 1:
                if startStep == 0:
                    gcb = Board(line)
                    turn(gcb)
                else:
                    startStep = startStep - 1    
            if num == 3:
                num = 0
            
        f.close()

        # turn(gcb)

        # strPole = f.readline()
        # strPole = f.readline()

    else:    
        gcb = GameClient(
            "http://codebattle-pro-2020s1.westeurope.cloudapp.azure.com/codenjoy-contest/board/player/tdakkyau1nxihybx7jrk?code=8348432615981863614&gameName=snakebattle")
        gcb.run(turn)

if __name__ == '__main__':
    main()