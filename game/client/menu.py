import socket
import pickle, time
from chel import Ball
import pygame, cv2
import pygame_menu
from pygame_menu.examples import create_example_window
from typing import Tuple, Any
from random import randint

__all__ = ['main']
RAS = WIDTH, HEIGHT = 800, 700
TILE=50
rows=WIDTH//TILE
cols=HEIGHT//TILE
pygame.init()
dis = pygame.display.set_mode(RAS)
pygame.display.set_caption("Client")
group_walls = pygame.sprite.Group()
cells = []
animals = ['animals\_rabbit.png', 'animals\cat.png', 'animals\owl.png',
           'animals\panda.png', 'animals\lemur.png', 'animals\hed.png',
           'animals\_bear.png', 'animals\dog.png', 'animals\squ.png',
           'animals\_fox.png', 'animals\_xz.png', 'animals\lion.png'
           ]
image_1 = pygame.image.load('1.jpg').convert_alpha()
image_2 = pygame.image.load('2.jpg').convert_alpha()
image_3 = pygame.image.load('3.jpg').convert_alpha()
image_4 = pygame.image.load('4.jpg').convert_alpha()
k = randint(0, 10)
   
class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        self.x, self.y, self.dx, self.dy=x,y,dx,dy
        pygame.sprite.Sprite.__init__(self)
        self.image = self.image(dy)
        self.rect = self.image.get_rect(left=self.x*TILE, top=self.y*TILE)
    
    def image(self, flag):
        if flag == 1:
            image = pygame.image.load('gorizont_fon.png').convert_alpha()
        else:
            image = pygame.image.load('vertical_fon.png').convert_alpha()
        return image
        
class Cell:
    def __init__(self, x, y, wall, a):
        self.x=x
        self.y=y
        self.wall= {'top': bool(wall[0]), 'right': bool(wall[1]), 'bottom': bool(wall[2]), 'left': bool(wall[3])}
        self.visited=False
        self.top=Wall(x, y, TILE, 1)
        self.left=Wall(x, y, 1, TILE)
        self.bottom=Wall(x, y+1, TILE, 1)
        self.right=Wall(x+1,y, 1, TILE)
        a.add(self.top, self.left, self.bottom, self.right)
        
    def draw(self):
        x=self.x*TILE
        y=self.y*TILE
        if self.visited:
            pygame.draw.rect(dis, (0,100,100), (x, y, TILE, TILE))
        if self.wall['top']==False:
            self.top.kill()
        if self.wall['left']==False:
            self.left.kill()
        if self.wall['right']==False:
            self.right.kill()
        if self.wall['bottom']==False:
            self.bottom.kill()
            
class network:
    def __init__(self):
        self.client = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server = "localhost"
        self.port = 8888
        self.addr = (self.server, self.port)
        self.p = self.connect()
    
    def getP(self):
        return self.p
    
    def connect(self):
        self.client.connect(self.addr)
        return pickle.loads(self.client.recv(1024))
    
    def send(self, d):
        try:
            data = [d.rect.centerx, d.rect.centery]
            self.client.send(pickle.dumps(data)) #отправляем наши координаты
            data2 = pickle.loads(self.client.recv(1024)) #получаем координаты другого игрока
            return data2
        except socket.error as e:
            print(e)

def create_maze(data): #создаем лабиринт
    global group_walls, cells
    for i in range(224):
        cl = Cell(data[i][0], data[i][1], data[i][2:], group_walls)
        cl.draw()
        cells.append(cl)
def window(dis, my_player, opponent, number2, image):
    global k 
    fon = pygame.image.load(image)
    fon_rect = fon.get_rect()
    dis.blit(fon, fon_rect)
    group_walls.draw(dis)
    ch = Ball(opponent[0], opponent[1], animals[k], 25, number2)
    dis.blit(ch.image, ch.rect)
    dis.blit(my_player.image, my_player.rect)
    pygame.display.update()
    pygame.display.flip()

def res(dis, p, win):
    global n
    time.sleep(3)
    run = True
    if win[0] == p.number:
        name_file = 'win.mp4'
    else:
        name_file = 'lose.mp4'
    cap = cv2.VideoCapture(name_file)
    success, img = cap.read()
    shape = img.shape[1::-1]
    while run:
        success, img = cap.read()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        if not success:
            cap = cv2.VideoCapture(name_file)
            success, img = cap.read()
            shape = img.shape[1::-1]
        dis.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
        pygame.display.update()
        pygame.display.flip()
        clock.tick(60)

ABOUT = [f'To start play: ',
         f'press Play and choose person',
         f'Author: Alyona',
         f'Email: alena.chadina2016@yandex.ru']
DIFFICULTY = ['animals\_rabbit.png']
FPS = 60

def change_person(value: Tuple[Any, int], difficulty: str) -> None:
    """
    Change person of the game.
    :param value: Tuple containing the data of the selected object
    :param difficulty: Optional parameter passed as argument to add_selector
    """
    selected, index = value
    print(difficulty)
    print(f'Selected animal: "{selected}" ({difficulty}) at index {index}')
    DIFFICULTY[0] = animals[selected[1]]

def play_function() -> None:
    global main_menu
    
    main_menu.disable()
    main_menu.full_reset()
    n = network() #подключаемся
    my_position = n.getP() #получаем свои начальные позиции
    if my_position[0] == 25:
        my_number = 1
        number2 = 2
    else:
        my_number = 2
        number2 = 1
    my_player = Ball(my_position[0], my_position[1], DIFFICULTY[0], 25, my_number) #играем этим игроком
    try:
        data_maze = pickle.loads(n.client.recv(8000)) #получаем лабиринт
        create_maze(data_maze)
    except:
        print("Error")
    run = True
    cap = cv2.VideoCapture('wait.MP4')
    success, img = cap.read()
    shape = img.shape[1::-1]
    wn = pygame.display.set_mode(shape)
    clock = pygame.time.Clock()
    while run:
        clock.tick(60)
        success, img = cap.read()
        try:
            data = n.client.recv(1024).decode('utf-8')
            if data and data != "Wait":
                run = False
                dis.blit(image_1, image_1.get_rect())
                pygame.display.update()
                time.sleep(1)
                dis.blit(image_2, image_2.get_rect())
                pygame.display.update()
                time.sleep(1)
                dis.blit(image_3, image_3.get_rect())
                pygame.display.update()
                time.sleep(1)
                dis.blit(image_4, image_4.get_rect())
                pygame.display.update()
                time.sleep(0.5)
        except Exception:
            print("Error")
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
        dis.fill((23, 5, 48))
        dis.blit(pygame.image.frombuffer(img.tobytes(), shape, "BGR"), (0, 0))
        pygame.display.update()
        pygame.display.flip()
    run = True
    
    while run:
        flag = -1
        opponent = n.send(my_player)
        if len(opponent) == 1:
            window(dis, my_player, r, number2, 'zatemn.JPEG')
            res(dis, my_player, opponent)
            run = False
        r = opponent
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    flag = 3
                if event.key == pygame.K_DOWN:
                    flag = 4
                if event.key == pygame.K_LEFT:
                    flag = 1
                if event.key == pygame.K_RIGHT:
                    flag = 2
            my_player.update(flag, group_walls)
        window(dis, my_player, r, number2, 'clouds.jpg')
    n.client.close()

def main_background():

    global surface
    fon = pygame.image.load('fon.jpg').convert_alpha()
    fon_rect = fon.get_rect()
    surface.blit(fon, fon_rect)

def main(test: bool = False) -> None:
    global clock
    global main_menu
    global surface
    surface = create_example_window('Maze Game', RAS)
    clock = pygame.time.Clock()
    # -------------------------------------------------------------------------
    # Create menus: Play Menu
    # -------------------------------------------------------------------------
    
    play_menu_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    play_menu_theme.title_font_color = (230, 115, 214)
    play_menu = pygame_menu.Menu(
        height=HEIGHT * 0.5,
        theme=play_menu_theme,
        title='Play Menu',
        width=WIDTH * 0.5
    )

    play_menu.add.button('Start',
                         play_function)
    play_menu.add.selector('Select person ',
                           [('Rabbit', 0),
                            ('Cat', 1),
                            ('Owl', 2),
                            ('Panda', 3),
                            ('Lemur', 4),
                            ('Cheetah', 5),
                            ('Bear', 6),
                            ('Dog', 7),
                            ('Squirrel', 8),
                            ('Fox', 9)],
                            onchange=change_person,
                            selector_id='select_animal')
    play_menu.add.button('Return to main menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus:About
    # -------------------------------------------------------------------------
    about_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    about_theme.title_font_color = (230, 115, 214)
    about_theme.widget_margin = (0, 0)

    about_menu = pygame_menu.Menu(
        height=HEIGHT * 0.5,
        theme=about_theme,
        title='About',
        width=WIDTH * 0.5
    )

    for m in ABOUT:
        about_menu.add.label(m, align=pygame_menu.locals.ALIGN_LEFT, font_size=20)
    about_menu.add.vertical_margin(30)
    about_menu.add.button('Return to menu', pygame_menu.events.BACK)

    # -------------------------------------------------------------------------
    # Create menus: Main
    # -------------------------------------------------------------------------
    main_theme = pygame_menu.themes.THEME_SOLARIZED.copy()
    main_theme.title_font_color = (230, 115, 214)
    main_menu = pygame_menu.Menu(
        height=HEIGHT * 0.5,
        theme=main_theme,
        title='Main Menu',
        width=WIDTH * 0.5
    )

    main_menu.add.button('Play', play_menu)
    main_menu.add.button('About', about_menu)
    main_menu.add.button('Quit', pygame_menu.events.EXIT)

    # -------------------------------------------------------------------------
    # Main loop
    # -------------------------------------------------------------------------
    while True:
        clock.tick(FPS)
        main_background()
        events = pygame.event.get()
        for event in events:
            if event.type == pygame.QUIT:
                exit()
        if main_menu.is_enabled():
            main_menu.mainloop(surface, main_background, disable_loop=test, fps_limit=FPS)
        pygame.display.flip()

if __name__ == '__main__':
    main()