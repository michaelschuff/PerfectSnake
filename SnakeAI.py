from Constants import HEIGHT
from Snake import Snake
from v2 import v2
from Constants import HEIGHT, WIDTH
import time


# class Node:
#     def __init__(self, parent=None, position=None):
#         self.parent = parent
#         self.position = position
#         self.g = 0
#         self.h = 0
#         self.f = 0
#
#     def __eq__(self, other):
#         return self.position == other.position
#
#
# def a_star(_maze, _start, _end):
#     start_node = Node(None, _start)
#     start_node.g = start_node.h = start_node.f = 0
#     end_node = Node(None, _end)
#     end_node.g = end_node.h = end_node.f = 0
#
#     open_list = [start_node]
#     closed_list = []
#
#     while len(open_list) > 0:
#         current_node = open_list[0]
#         current_index = 0
#         for index, item in enumerate(open_list):
#             if item.f < current_node.f:
#                 current_node = item
#                 current_index = index
#
#         # Pop current off open list, add to closed list
#         open_list.pop(current_index)
#         closed_list.append(current_node)
#
#         if current_node == end_node:
#             path = []
#             current = current_node
#             while current is not None:
#                 path.append(current.position)
#                 current = current.parent
#             return path[::-1]
#
#         # Generate children
#         children = []
#         for new_position in [v2(0, -1), v2(0, 1), v2(-1, 0), v2(1, 0)]:
#             # Get node position
#             node_position = current_node.position + new_position
#
#             if node_position.y >= len(_maze) or node_position.y < 0 or node_position.x >= len(
#                     _maze[len(_maze) - 1]) or node_position.x < 0:
#                 continue
#             if _maze[node_position.y][node_position.x] != ".":
#                 continue
#
#             # Create new node
#             new_node = Node(current_node, node_position)
#
#             # Append
#             children.append(new_node)
#
#         # Loop through children
#         for child in children:
#             # Child is on the closed list
#             for closed_child in closed_list:
#                 if child == closed_child:
#                     continue
#
#             # Create the f, g, and h values
#             child.g = current_node.g + 1
#             # child.h = abs(child.position.x - end_node.position.x) + abs(child.position.y - end_node.position.y)
#             child.h = (child.position.x - end_node.position.x)**2 + (child.position.y - end_node.position.y)**2
#             child.f = child.g + child.h
#
#             # Child is already in the open list
#             for open_node in open_list:
#                 if child == open_node and child.g > open_node.g:
#                     continue
#
#             open_list.append(child)
def a_star(m,startp,endp):
    w,h = WIDTH,HEIGHT
    sx,sy = startp
    ex,ey = endp
    #[parent node, x, y,g,f]
    node = [None,sx,sy,0,abs(ex-sx)+abs(ey-sy)]
    closeList = [node]
    createdList = {}
    createdList[sy*w+sx] = node
    k=0
    while(closeList):
        node = closeList.pop(0)
        x = node[1]
        y = node[2]
        l = node[3]+1
        k+=1
        #find neighbours
        #make the path not too strange
        if k&1:
            neighbours = ((x,y+1),(x,y-1),(x+1,y),(x-1,y))
        else:
            neighbours = ((x+1,y),(x-1,y),(x,y+1),(x,y-1))
        for nx,ny in neighbours:
            if nx==ex and ny==ey:
                path = [(ex,ey)]
                while node:
                    path.append((node[1],node[2]))
                    node = node[0]
                return list(reversed(path))
            if 0<=nx<w and 0<=ny<h and m[ny][nx]==".":
                if ny*w+nx not in createdList:
                    nn = (node,nx,ny,l,l+abs(nx-ex)+abs(ny-ey))
                    createdList[ny*w+nx] = nn
                    #adding to closelist ,using binary heap
                    nni = len(closeList)
                    closeList.append(nn)
                    while nni:
                        i = (nni-1)>>1
                        if closeList[i][4]>nn[4]:
                            closeList[i],closeList[nni] = nn,closeList[i]
                            nni = i
                        else:
                            break

def print_board(board):
    for y in board:
        for x in y:
            print(x, end="")
        print()


def duplicate_board(board):
    new_board = []
    for y in range(HEIGHT):
        new_board.append([])
        for x in range(WIDTH):
            new_board[y].append(board[y][x])
    return new_board


def get_fastest_path(snake):
    head = snake.body[0].pos
    food = snake.food.pos
    seg_positions = []
    for i in snake.body:
        seg_positions.append(i.pos)
    board = []
    for y in range(HEIGHT):
        board.append([])
        for x in range(WIDTH):
            t = v2(x, y)
            if t in seg_positions:
                board[y].append("X")
            else:
                board[y].append(".")

    # remove "walls" that will have moved by the time the head of the snake gets to them
    removable_segments = []
    for seg in range(len(snake.body)-1, 0, -1):
        n = snake.body[seg]
        n_board = duplicate_board(board)
        n_board[n.pos.y][n.pos.x] = "."
        if len(a_star(n_board, (head.x, head.y), (n.pos.x, n.pos.y))) > len(snake.body) - n.index:
            removable_segments.append(n.pos)

    new_board = duplicate_board(board)
    for i in removable_segments:
        new_board[i.y][i.x] = "."

    fastest_path_tuples = a_star(new_board, (head.x, head.y), (food.x, food.y))
    fastest_path = []
    for square in range(1, len(fastest_path_tuples)):
        diff = v2(fastest_path_tuples[square][0] - fastest_path_tuples[square-1][0],fastest_path_tuples[square][1] - fastest_path_tuples[square-1][1])
        fastest_path.append(diff)

    return fastest_path


if __name__ == "__main__":
    # board = [[".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."],
    #          [".", ".", ".", ".", ".", ".", ".", ".", ".", "."]]
    #
    # start = v2(0, 0)
    # end = v2(7, 6)
    #
    # path = a_star(maze, start, end)
    # print(path)
    print_board(get_fastest_path(Snake(14)))
