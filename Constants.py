
BACKGROUND_WALL = 1


SNAKE_LEN_GOTO_STONE = 50 #При какой длине змея начнет есть камни, без ярости

SHORE_APPLE = 10
SHORE_STONE = 3
SHORE_GOLD = 10
SHORE_FURY = 9 #Просто за бутылку
SHORE_FURY_EVIL = 20 #Количество очков до бутылки ярости до которой можно добежать
SHORE_FURY_EVIL_NEAR = 20 #Количество очков плюсом до ближайшей бутылки ярости
SHORE_WALL = -1000
SHORE_NEVER = -10000

SHORE_HOD = -1 #Вес одного хода
FURY_PILL_STEP_NUM = 10 # Количество ходов дающиъся за выписваание бутылки ярости
NUM_SHORE_FIRS_STEP = -110 #Какие преграды не рассматривать при первом шаге, не ходить на клетку меньше очков чем
NUM_SHORE_TRAP_STEP = 0 #Какие очки преграды рассматриваются у ловушек, если подарок рядом не имеет проходов меньше очков, то очки не присуждаем, больше нуля нельзя, так как пустая клетка 0
NUM_SHORE_NEXT_LOCATION = 12 # Количество очков в округе, при которым ищем куда бежать
NUM_CALC_MAX_STEP = 15 #Количество просчитываемых ходов поблизости
NUM_CALC_MAX_STEP_ALL = 60 #Количество просчитываемых ходов при траектории движения
NUM_CALC_MAX_ELEMENTS = 5 #Количество элементов взятых в выборку просчитывания ходов


# Очки - штрафы
SHORE_SNAKE_HEAD = -120
SHORE_SNAKE_BODY = -120 #Раньше было минус 10
SHORE_SNAKE_TAIL = -10

# Очки - штрафы
SHORE_ENEMY_SNAKE_HEAD = 80 #Очки за голову другйо змей
SHORE_ENEMY_SNAKE_BODY = 80 #Очки за начисление укус клетки другой змеи
SHORE_ENEMY_SHORE_EVIL = -120
SHORE_MY_SNAKE_OTKUS = 20 #Очки за откусывание тела моей змеи если самому откусить



#My Enemy
ENEMY_TAIL = '~'
ENEMY_HEAD = '♦'
ENEMY_BODY = '-'
SNAKE_BODY = '='


NONE=' '  # пустое место
WALL='☼'  # а это стенка
START_FLOOR='#' ##+ # место старта змей
OTHER='?' # этого ты никогда не увидишь:)
APPLE='○' # яблоки надо кушать от них становишься длинее
STONE='●' # а это кушать не стоит - от этого укорачиваешься
FLYING_PILL='©' # таблетка полета - дает суперсилы
FURY_PILL='®'##+ # таблетка ярости - дает суперсилы
GOLD='$' # золото - просто очки

# голова твоей змеи в разных состояниях и напрвлениях
HEAD_DOWN='▼'##+ 
HEAD_LEFT='◄'##+ 
HEAD_RIGHT='►'##+ 
HEAD_UP='▲'##+ 
HEAD_DEAD='☻' # этот раунд ты проиграл
HEAD_EVIL='♥' # ты скушал таблетку ярости
HEAD_FLY='♠' # ты скушал таблетку полета
HEAD_SLEEP='&' ##+ # твоя змейка ожидает начала раунда

# хвост твоей змейки
TAIL_END_DOWN='╙'
TAIL_END_LEFT='╘'
TAIL_END_UP='╓'
TAIL_END_RIGHT='╕'
TAIL_INACTIVE='~'

# туловище твоей змейки
BODY_HORIZONTAL='═'
BODY_VERTICAL='║'
BODY_LEFT_DOWN='╗'
BODY_LEFT_UP='╝'
BODY_RIGHT_DOWN='╔'
BODY_RIGHT_UP='╚'

# змейки противников
ENEMY_HEAD_DOWN='˅'##+
ENEMY_HEAD_LEFT='<'##+
ENEMY_HEAD_RIGHT='>'##+
ENEMY_HEAD_UP='˄'##+
ENEMY_HEAD_DEAD='☺' # этот раунд противник проиграл
ENEMY_HEAD_EVIL='♣'##+ # противник скушал таблетку ярости
ENEMY_HEAD_FLY='♦' # противник скушал таблетку полета
ENEMY_HEAD_SLEEP='ø' # змейка противника ожидает начала раунда

# хвосты змеек противников
ENEMY_TAIL_END_DOWN='¤'
ENEMY_TAIL_END_LEFT='×'
ENEMY_TAIL_END_UP='æ'
ENEMY_TAIL_END_RIGHT='ö'
ENEMY_TAIL_INACTIVE='*' ##+

# туловище змеек противников
ENEMY_BODY_HORIZONTAL='─'
ENEMY_BODY_VERTICAL='│'
ENEMY_BODY_LEFT_DOWN='┐'
ENEMY_BODY_LEFT_UP='┘'
ENEMY_BODY_RIGHT_DOWN='┌'
ENEMY_BODY_RIGHT_UP='└'

