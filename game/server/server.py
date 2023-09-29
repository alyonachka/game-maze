import socket
import _thread
import pickle
from random import choice
import time

RES = WIDTH, HEIGHT = 800, 700
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE
        
class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {'top': True, 'right': True, 'bottom': True, 'left': True}
        self.visited = False

    def check_cell(self, x, y, cells):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return cells[find_index(x, y)]

    def check_neighbors(self, cells):
        neighbors = []
        top = self.check_cell(self.x, self.y - 1, cells)
        right = self.check_cell(self.x + 1, self.y, cells)
        bottom = self.check_cell(self.x, self.y + 1, cells)
        left = self.check_cell(self.x - 1, self.y, cells)
        if top and not top.visited:
            neighbors.append(top)
        if right and not right.visited:
            neighbors.append(right)
        if bottom and not bottom.visited:
            neighbors.append(bottom)
        if left and not left.visited:
            neighbors.append(left)
        return choice(neighbors) if neighbors else False
    
    def remove_walls(self, next):
        dx = self.x - next.x
        if dx == 1:
            self.walls['left'] = False
            next.walls['right'] = False
        elif dx == -1:
            self.walls['right'] = False
            next.walls['left'] = False
        dy = self.y - next.y
        if dy == 1:
            self.walls['top'] = False
            next.walls['bottom'] = False
        elif dy == -1:
            self.walls['bottom'] = False
            next.walls['top'] = False

class Maze:

    def __init__(self):
        self.count = 0
        
    def labirint(self):
        cells = [Cell(col, row) for row in range(rows) for col in range(cols)]
        stack = []
        current_cell = cells[0]
        current_cell.visited = True
        while self.check(cells):
            next_cell=current_cell.check_neighbors(cells)
            if next_cell:
               next_cell.visited=True
               stack.append(current_cell)
               current_cell.remove_walls(next_cell)
               current_cell=next_cell
            elif stack:
               current_cell=stack.pop()
        return cells
    
    def check(self, cells):
        k=False
        for cell in cells:
            if not cell.visited:
                k = True
        if not k:
            self.count += 1
        if self.count == 1:
            k = True
        return k
        
g = Maze()
xyi = []
cells = g.labirint()
for cell in cells:
    x = [cell.x, cell.y, cell.walls['top'], cell.walls['right'], cell.walls['bottom'], cell.walls['left']]
    xyi.append(x)

server = "localhost"
port = 8888
sckt = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

try:
    sckt.bind((server, port))
except socket.error as error:
    print(str(error))

sckt.listen(10)
print("Waiting for a connection, Server Started")

class Game:
    def __init__(self):
        self.players = [[25, 25], [775, 675]]
        self.current_players = 0
        self.win = 0
        self.i = 0
    
    def check(self):
        flag = True
        if self.players[0][0] == 775 and self.players[0][1] == 675:
            flag = False
            self.win = 1
        if self.players[1][0] == 25 and self.players[1][1] == 25:
            flag = False
            self.win = 2
        return flag

def threadedClient(conn, player, game, xyi):
    conn.send(pickle.dumps(game.players[player-1])) #начальные позиции игроков
    try:
        conn.send(pickle.dumps(xyi)) #отправляем лабиринт
    except:
        print("oh you tach my tralala")
        conn.close()
    while game.current_players == 1:
        try:
            time.sleep(0.5)
            conn.send(b"Wait")
        except:
            print("Idi nax")
            conn.close()
            break 
    time.sleep(0.3)        
    conn.sendall(b"okok")
    while game.check():
        reply = ""
        try:
            data = pickle.loads(conn.recv(2048)) #получаем новые позиции
            game.players[player-1] = data 
            if not data:
                conn.close()
                print("Disconnected")
                break
            else:
                if player == 1:
                    reply = game.players[1]
                else:
                    reply = game.players[0]
            conn.sendall(pickle.dumps(reply)) #отправляем новые позиции
        except:
            conn.close()
            print("Disconnect")
            break  
    data = pickle.loads(conn.recv(2048))
    if player == 1:
        reply = game.players[0]
    else:
        reply = game.players[1]
    conn.sendall(pickle.dumps(reply))
    reply = [game.win]
    data = pickle.loads(conn.recv(2048))
    try:
        conn.sendall(pickle.dumps(reply))
    except:
        print(22222)
    conn.close()
    print("Disconnect")

game = Game()
while True:
    if game.current_players == 2:
        g = Maze()
        xyi = []
        cells = g.labirint()
        for cell in cells:
            x = [cell.x, cell.y, cell.walls['top'], cell.walls['right'], cell.walls['bottom'], cell.walls['left']]
            xyi.append(x)
        game = Game()
    conn, addr = sckt.accept()
    print("Connected to: ", addr)
    game.current_players += 1
    _thread.start_new_thread(threadedClient, (conn, game.current_players, game, xyi))