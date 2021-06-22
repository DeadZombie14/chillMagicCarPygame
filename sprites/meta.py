import pygame
from utilidades.colores import *

class Meta(pygame.sprite.Sprite):

    def __init__(self, screen,screenSize, coord, estilo=1):
        pygame.sprite.Sprite.__init__(self)

        self.image = pygame.image.load('assets/img/r_flag.png')
        self.image = pygame.transform.scale(self.image,[32,32])
        # self.image.fill((0,0,255))

        self.estilo = estilo

        def color_surface(surface, color):
            arr = pygame.surfarray.pixels3d(surface)
            arr[:,:,0] = color[0]
            arr[:,:,1] = color[1]
            arr[:,:,2] = color[2]

        coloredSurface = self.image.copy()
        
        if estilo == 1:
            color_surface(coloredSurface, red)
        elif estilo == 2:
            color_surface(coloredSurface, green)
        elif estilo == 3:
            color_surface(coloredSurface, blue)
        elif estilo == 4:
            color_surface(coloredSurface, black)


        self.image = coloredSurface
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = coord[0],coord[1]
    
    def getEstilo(self):
        return self.estilo