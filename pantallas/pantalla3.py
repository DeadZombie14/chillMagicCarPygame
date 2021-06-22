import pygame
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

from app import App

from pygame.locals import *

"""
Pantalla 3
"""
class Pantalla3(App):
    def __init__(self, Aplicacion):
        self.running = True
        self.app = Aplicacion
        pass
    
    def iniciar(self):
        super().__init__()
        
        self.screen = super().getScreen()
        self.screenSize = super().getScreenSize()
        self.weight = self.screenSize[0]
        self.height = self.screenSize[1]

        # load image (it is in same directory)
        self.image = pygame.image.load("assets/img/man01.png").convert()
        self.image.set_colorkey((255,0,255))

        # instead of blitting the background image you could fill it 
        # (uncomment the next line to do so)
        #screen.fill((255,0,0))
        
        self.samus = self.screen.blit(self.image, (56,56))
        
        # define the position of the smily
        self.xpos = 50
        self.ypos = 50
        # how many pixels we move our smily each frame
        self.step_x = 10
        self.step_y = 10

        self.keypress = False
        # update the screen to make the changes visible (fullscreen update)
        self.speedx = 1
        self.speedy = 1
        pygame.display.flip()





        self.ejecucion()
        return

    def ejecucion(self):
        while( self.running ):
            super().general_events(self) # Eventos generales
            for event in pygame.event.get(): 
                self.eventos(event)
            self.update()
    
    def eventos(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        if event.type == pygame.QUIT:
            self._running = False
        if pygame.key.get_pressed()[K_w]:
           pass
        if pygame.key.get_pressed()[K_LALT] and pygame.key.get_pressed()[K_RETURN]:
            pygame.display.toggle_fullscreen()
        return
    
    def update(self):
        if KEYDOWN and not self.keypress:
            if pygame.key.get_pressed()[K_w] or pygame.key.get_pressed()[K_UP]:
                # update the position of the smily
                self.ypos += -self.speedy	 # move it up
            elif pygame.key.get_pressed()[K_s] or pygame.key.get_pressed()[K_DOWN]:
                # update the position of the smily
                self.ypos += self.speedy	 # move it down
            elif pygame.key.get_pressed()[K_a] or pygame.key.get_pressed()[K_LEFT]:
                # update the position of the smily
                self.xpos  += -self.speedx # move it left
            elif pygame.key.get_pressed()[K_d] or pygame.key.get_pressed()[K_RIGHT]:
                # update the position of the smily
                self.xpos  += self.speedx # move it right
            self.keypress = True
        else:
            self.keypress = False
        # Refrescar pantalla constantemente
        # check if the smily is still on screen, if not change direction
        if self.xpos > self.weight-64 or self.xpos<0:
            self.speedx = 0
            self.xpos += -self.speedy
        else:
            self.speedx = 1
        if self.ypos > self.height-64 or self.ypos<0:
            self.speedy = 0
            self.ypos += -self.speedy
        else:
            self.speedy = 1
        # update the position of the smily



        # now blit the smily on screen
        self.screen.blit(self.image, (self.xpos, self.ypos))
        # and update the screen (dont forget that!)
        pygame.display.flip()
        
        # first erase the screen 
        #(just blit the background over anything on screen)
        #self.screen.blit(bgd_image, (0,0))
        self.screen.fill((156,48,64))
        # now blit the smily on screen
        self.screen.blit(self.image, (self.xpos, self.ypos))
        # and update the screen (dont forget that!)
        pygame.display.update()
        return

