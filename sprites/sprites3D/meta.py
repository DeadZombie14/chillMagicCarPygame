import pygame

class Meta(pygame.sprite.Sprite):

    def __init__(self, screen,screenSize, coord):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/img/r_flag.png')
        self.image = pygame.transform.scale(self.image,[32,32])
        # self.image.fill((0,0,255))

        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = coord[0],coord[1]