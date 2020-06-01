_ELEMENTS = dict(

    NONE=' ',  # пустое место
    WALL='☼',  # а это стенка
    START_FLOOR='#', ##+ # место старта змей
    OTHER='?', # этого ты никогда не увидишь:)
    APPLE='○', # яблоки надо кушать от них становишься длинее
    STONE='●', # а это кушать не стоит - от этого укорачиваешься
    FLYING_PILL='©', # таблетка полета - дает суперсилы
    FURY_PILL='®',##+ # таблетка ярости - дает суперсилы
    GOLD='$', # золото - просто очки

    # голова твоей змеи в разных состояниях и напрвлениях
    HEAD_DOWN='▼',##+ 
    HEAD_LEFT='◄',##+ 
    HEAD_RIGHT='►',##+ 
    HEAD_UP='▲',##+ 
    HEAD_DEAD='☻', # этот раунд ты проиграл
    HEAD_EVIL='♥', # ты скушал таблетку ярости
    HEAD_FLY='♠', # ты скушал таблетку полета
    HEAD_SLEEP='&', ##+ # твоя змейка ожидает начала раунда

    # хвост твоей змейки
    TAIL_END_DOWN='╙',
    TAIL_END_LEFT='╘',
    TAIL_END_UP='╓',
    TAIL_END_RIGHT='╕',
    TAIL_INACTIVE='~',

    # туловище твоей змейки
    BODY_HORIZONTAL='═',
    BODY_VERTICAL='║',
    BODY_LEFT_DOWN='╗',
    BODY_LEFT_UP='╝',
    BODY_RIGHT_DOWN='╔',
    BODY_RIGHT_UP='╚',

    # змейки противников
    ENEMY_HEAD_DOWN='˅',##+
    ENEMY_HEAD_LEFT='<',##+
    ENEMY_HEAD_RIGHT='>',##+
    ENEMY_HEAD_UP='˄',##+
    ENEMY_HEAD_DEAD='☺', # этот раунд противник проиграл
    ENEMY_HEAD_EVIL='♣',##+ # противник скушал таблетку ярости
    ENEMY_HEAD_FLY='♦', # противник скушал таблетку полета
    ENEMY_HEAD_SLEEP='ø', # змейка противника ожидает начала раунда

    # хвосты змеек противников
    ENEMY_TAIL_END_DOWN='¤',
    ENEMY_TAIL_END_LEFT='×',
    ENEMY_TAIL_END_UP='æ',
    ENEMY_TAIL_END_RIGHT='ö',
    ENEMY_TAIL_INACTIVE='*', ##+

    # туловище змеек противников
    ENEMY_BODY_HORIZONTAL='─',
    ENEMY_BODY_VERTICAL='│',
    ENEMY_BODY_LEFT_DOWN='┐',
    ENEMY_BODY_LEFT_UP='┘',
    ENEMY_BODY_RIGHT_DOWN='┌',
    ENEMY_BODY_RIGHT_UP='└')

def value_of(char):
    """ Test whether the char is valid Element and return it's name."""
    for value, c in _ELEMENTS.items():
        if char == c:
            return value
    else:
        raise AttributeError("No such Element: {}".format(char))


class Element:
    """ Class describes the Element objects for Bomberman game."""

    def __init__(self, n_or_c):
        """ Construct an Element object from given name or char."""
        for n, c in _ELEMENTS.items():
            if n_or_c == n or n_or_c == c:
                self._name = n
                self._char = c
                break
        else:
            raise AttributeError("No such Element: {}".format(n_or_c))

    def get_char(self):
        """ Return the Element's character."""
        return self._char

    def __eq__(self, otherElement):
        return (self._name == otherElement._name and
                self._char == otherElement._char)


if __name__ == '__main__':
    raise RuntimeError("This module is not intended to be ran from CLI")
