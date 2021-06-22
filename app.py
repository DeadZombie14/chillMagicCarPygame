import pygame, thorpy
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

import config as config

"""
CLASE PRINCIPAL: Aplicación
"""
ScreenSize = width, height = 1056, 672
Caption = "CMC v0.11"

if not config.pantalla_completa:
    thorpy.Application(size=ScreenSize, caption=Caption, flags= pygame.DOUBLEBUF) # Declarar propiedades ventana
else:
    thorpy.Application(size=ScreenSize, caption=Caption,flags= pygame.DOUBLEBUF | pygame.FULLSCREEN) # Declarar propiedades ventana

class App:
    # Constructor
    def __init__(self, resolucion = ScreenSize):
        # self.screen = None
        self.pantalla_completa = config.pantalla_completa
        # Tamaño de la ventana
        self.ScreenSize = resolucion
        # Crear pantalla
        self.screen = thorpy.get_screen()
        pygame.init()
        # self.screen.fill((0,0,0))
        # pygame.display.set_caption('Proyecto v3', 'icontitle=None')
    
    def getScreen(self):
        return self.screen

    def getScreenSize(self):
        return self.ScreenSize
    
    def getPantallaCompleta(self):
        return self.pantalla_completa
    
    def general_events(self, pantalla):
        # Eventos generales - No usar eventos de tipo KEYDOWN

        keys = pygame.key.get_pressed()
        # Quitar con Alt + F4
        if keys[pygame.K_LALT] and keys[pygame.K_F4]:
            thorpy.functions.quit_func()
        
        # Alternar entre pantalla completa/ventana con ALT + ENTER
        if keys[pygame.K_LALT] and keys[pygame.K_RETURN]:
            self.togglePantallaCompleta(pantalla)
    
    # Alternar entre pantalla completa/ventana
    def togglePantallaCompleta(self, pantalla):
        if not self.pantalla_completa:
            self.pantalla_completa = True
            pygame.display.quit()
            thorpy.Application(size=self.ScreenSize, caption=Caption,flags= pygame.FULLSCREEN | pygame.HWSURFACE) # Declarar propiedades ventana
            # Crear pantalla
            self.screen = thorpy.get_screen()
            pygame.display.init()
            pantalla.thorpy()
        else:
            self.pantalla_completa = False
            pygame.display.quit()
            thorpy.Application(size=self.ScreenSize, caption=Caption) # Declarar propiedades ventana
            # Crear pantalla
            self.screen = thorpy.get_screen()
            pygame.display.init()
            pantalla.thorpy()
        # Escribir en el archivo config.py la configuración de pantalla completa
        f = open("config.py","r+")
        d = f.readline(0)
        f.seek(0)
        for i in d:
            if i != "pantalla_completa=False" or i != "pantalla_completa=True":
                f.write(f'pantalla_completa={self.pantalla_completa}')
        # f.truncate()
        f.close()
        pass


