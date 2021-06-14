from v2 import v2
from Constants import WIDTH, HEIGHT, DIR, SEGMENT_SIZE
from random import randrange


class Segment:
    def __init__(self, _pos, _next, _dir=DIR.LEFT):
        self.pos = _pos
        self.next = _next
        self.dir = _dir

    def update(self):
        self.pos += self.dir
        if self.next is not None:
            self.dir = self.next.dir

    def set_dir(self, _dir):
        self.dir = _dir


class Head(Segment):
    def __init__(self, _pos=v2(int(WIDTH / 2), int(HEIGHT / 2))):
        super().__init__(_pos, None)


class Food:
    def __init__(self, _pos):
        self.pos = _pos

    def eaten(self):
        self.pos = v2(randrange(WIDTH), randrange(HEIGHT))


class Snake:
    body = []
    food = Food(v2(randrange(WIDTH), randrange(HEIGHT)))

    def __init__(self, n=0):
        self.body.append(Head())
        for i in range(n):
            self.body.append(Segment(self.body[0].pos + (i + 1) * DIR.RIGHT, self.body[i]))

    def head_is_off_screen(self):
        head = self.body[0]
        return (head.pos.x < 0) or (head.pos.x >= WIDTH) or (head.pos.y < 0) or (head.pos.y >= HEIGHT)

    def iterate(self):
        if self.body[0].pos + self.body[0].dir == self.food.pos:
            self.food.eaten()
            self.body.append(Segment(self.body[len(self.body) - 1].pos,
                                     self.body[len(self.body) - 1],
                                     self.body[len(self.body) - 1].dir))
        else:
            self.body[len(self.body) - 1].update()

        for i in range(len(self.body) - 2, -1, -1):
            self.body[i].update()

        if self.head_is_off_screen():
            return False

        for i in range(1, len(self.body)):
            if self.body[0].pos == self.body[i].pos:
                return False

        return True

    def update_head_dir(self, _dir):
        self.body[0].set_dir(_dir)

    def get_head_dir(self):
        return self.body[0].dir
