import pygame

class Ball(pygame.sprite.Sprite):
    def __init__(self, x, y, filename, speed, number):
        pygame.sprite.Sprite.__init__(self)
        self.number = number #индекс игрока
        self.image = pygame.image.load(filename).convert_alpha()
        self.rect = self.image.get_rect()
        self.rect.centerx = x 
        self.rect.centery = y
        self.speed = speed

    def update(self, flag, walls):
        if flag == 2:
            self.rect.x += self.speed
            if self.check(walls):
                self.rect.x += self.speed
            else:
                self.rect.x -= self.speed
            if self.rect.x > 779:
                self.rect.x = 782
        if flag == 1:
            self.rect.x -= self.speed
            if self.check(walls):
                self.rect.x -= self.speed
            else:
                self.rect.x += self.speed
            if self.rect.x < 0:
                self.rect.x = 7
        if flag==3:
            self.rect.y -= self.speed
            if self.check(walls):
                self.rect.y -= self.speed
            else:
                self.rect.y += self.speed
            if self.rect.y < 0:
                self.rect.y = 7
        if flag==4:
            self.rect.y += self.speed
            if self.check(walls):
                self.rect.y += self.speed
            else:
                self.rect.y -= self.speed
            if self.rect.y > 775:
                self.rect.y = 782
        
    def check(self, wall):
        k = True
        for el in wall:
            if self.rect.colliderect(el):
                k = False
        return k
            
        