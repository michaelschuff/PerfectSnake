from v2 import v2
from Constants import WIDTH, HEIGHT, DIR, SEGMENT_SIZE
from random import randrange


class Segment:
    def __init__(self, _pos, _next, _index, _dir=DIR.LEFT):
        self.pos = _pos
        self.next = _next
        self.dir = _dir
        self.index = _index

    def update(self):
        self.pos += self.dir
        if self.next is not None:
            self.dir = self.next.dir

    def set_dir(self, _dir):
        self.dir = _dir


class Head(Segment):
    def __init__(self, _pos=v2(int(WIDTH / 2), int(HEIGHT / 2))):
        super().__init__(_pos, None, 0)


class Food:
    def __init__(self, body):
        self.sorted_segments = []
        self.board = []
        for y in range(HEIGHT):
            for x in range(WIDTH):
                self.board.append(v2(x, y))
        self.pos = v2(0, 0)
        self.new_position(body)

    def new_position(self, body):
        self.sorted_segments = []
        for i in body:
            self.sorted_segments.append(i.pos)
        self.pos = v2(randrange(WIDTH), randrange(HEIGHT))
        while self.pos in self.sorted_segments:
            self.pos = v2(randrange(WIDTH), randrange(HEIGHT))
        # never mind this is fucking slow
        # get body positions into a sorted list of how far
        # they are from 0,0 based on up->down then left->right
        # self.sorted_segments = []
        # for seg in range(len(body)):
        #     p_num = body[seg].pos.y*WIDTH + body[seg].pos.x
        #     put_in = False
        #     for i in range(len(self.sorted_segments)):
        #         if self.sorted_segments[i].y*WIDTH + self.sorted_segments[i].x > p_num:
        #             self.sorted_segments.insert(i, body[seg].pos)
        #             put_in = True
        #     if not put_in:
        #         self.sorted_segments.append(body[seg].pos)

        # n is a random number between 1 and number of free spaces
        # so find the nth free space
        # n = randrange(WIDTH * HEIGHT - len(body))
        # for i in range(len(self.board)):
        #     if self.board[i] not in self.sorted_segments:
        #         n -= 1
        #         if n == 0:
        #             self.pos = self.board[i]


class Snake:
    didEat = True

    def __init__(self, n=0):
        self.body = []
        self.body.append(Head())
        for i in range(n):
            self.body.append(Segment(self.body[0].pos + (i+1) * DIR.RIGHT, self.body[i], i+1))

        self.food = Food(self.body)

    def head_is_off_screen(self):
        head = self.body[0]
        return (head.pos.x < 0) or (head.pos.x >= WIDTH) or (head.pos.y < 0) or (head.pos.y >= HEIGHT)

    def iterate(self):
        if self.body[0].pos + self.body[0].dir == self.food.pos:
            self.didEat = True
            self.food.new_position(self.body)
            self.body.append(Segment(self.body[len(self.body) - 1].pos,
                                     self.body[len(self.body) - 1],
                                     len(self.body),
                                     DIR.NONE))
        else:
            self.didEat = False

        for i in range(len(self.body) - 1, -1, -1):
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
