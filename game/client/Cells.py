import pygame
from random import choice

TILE=50
RAS = WIDTH, HEIGHT = 800, 800
rows=WIDTH//TILE
cols=HEIGHT//TILE

class Wall(pygame.sprite.Sprite):
    def __init__(self, x, y, dx, dy):
        self.x, self.y, self.dx, self.dy=x,y,dx,dy
        pygame.sprite.Sprite.__init__(self)
        self.image=pygame.Surface((dx,dy))
        self.image.fill((100,0,50))
        self.rect = self.image.get_rect(left=self.x*TILE, top=self.y*TILE)
        
class Cell:
    def __init__(self, x, y, a):
        self.x=x
        self.y=y
        self.wall={'right': True, 'left': True, 'bottom': True, 'top': True}
        self.visited=False
        self.top=Wall(x, y, TILE, 1)
        self.left=Wall(x, y, 1, TILE)
        self.bottom=Wall(x, y+1, TILE, 1)
        self.right=Wall(x+1,y, 1, TILE)
        a.add(self.top, self.left, self.bottom, self.right)
        
    def draw_current_cell(self, dis):
        x=self.x*TILE
        y=self.y*TILE
        pygame.draw.rect(dis, (255,255,255), (x+2,y+2,TILE-2,TILE-2))
        
    def draw(self):
        x=self.x*TILE
        y=self.y*TILE
        #if self.visited:
            #pygame.draw.rect(dis, (0,100,100), (x, y, TILE, TILE))
        if self.wall['top']==False:
            self.top.kill()
        if self.wall['left']==False:
            self.left.kill()
        if self.wall['right']==False:
            self.right.kill()
        if self.wall['bottom']==False:
            self.bottom.kill()
            
    def check_cell(self, x, y, cells):
        find_index=lambda x, y: x+y*cols
        if x<0 or x>cols-1 or y<0 or y>rows-1:
            return False
        return cells[find_index(x,y)]
    
    def check_neighbors(self, cells):
        neighbors=[]
        top=self.check_cell(self.x, self.y-1, cells)
        right=self.check_cell(self.x+1,self.y, cells)
        left=self.check_cell(self.x-1,self.y, cells)
        bottom=self.check_cell(self.x, self.y+1, cells)
        if top and top.visited==False:
            neighbors.append(top)
        if right and right.visited==False:
            neighbors.append(right)
        if left and left.visited==False:
            neighbors.append(left)
        if bottom and bottom.visited==False:
            neighbors.append(bottom)
            
        if neighbors:
            return choice(neighbors)
        else:
            return False
        
    def remove_walls(self, next):
        dx=self.x-next.x
        dy=self.y-next.y
        if dx==1:
            self.wall['left']=False
            next.wall['right']=False
        elif dx==-1:
            self.wall['right']=False
            next.wall['left']=False
        if dy==1:
            self.wall['top']=False
            next.wall['bottom']=False
        elif dy==-1:
            self.wall['bottom']=False
            next.wall['top']=False
            