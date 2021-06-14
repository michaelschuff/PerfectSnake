from v2 import v2

WIDTH = 30
HEIGHT = 20
SEGMENT_SIZE = 20
SCREEN_SIZE = (WIDTH * SEGMENT_SIZE, HEIGHT * SEGMENT_SIZE)
CAPTION = "Snek"


class DIR:
    UP = v2(0, 1)
    DOWN = v2(0, -1)
    LEFT = v2(-1, 0)
    RIGHT = v2(1, 0)
    NONE = v2(0, 0)
