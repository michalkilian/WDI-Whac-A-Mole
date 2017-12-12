import pygame

class Background(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = pygame.image.load(image).convert()
        self.rect = self.image.get_rect()
        self.rect.left = 0
        self.rect.top = 0

#our cursor
class Cursor(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
    def hit(self, target):
        return self.rect.colliderect(target)
    def update(self, position):
        self.rect.center = position
    def draw(self,screen):
        screen.blit(self.image, self.rect)

#bad moles
class Mole(pygame.sprite.Sprite):
    def __init__(self,image):
        super().__init__()
        self.image = pygame.image.load(image)
        self.rect = self.image.get_rect()
    def update(self,position):
        self.rect.center = position
    def draw(self,screen):
        screen.blit(self.image,self.rect)

class Buttons(pygame.sprite.Sprite):
    def __init__(self,width,height,left,top):
        super().__init__()
        self.image = pygame.Surface((width,height))
        self.rect = self.image.get_rect()
        self.rect.left = left
        self.rect.top = top
    def draw(self,screen):
        screen.blit(self.image,self.rect)