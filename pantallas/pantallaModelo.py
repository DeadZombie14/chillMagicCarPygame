import pygame, thorpy
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

from app import App

"""
Pantalla 1
"""
class Pantalla1(App):
    def __init__(self, Aplicacion):
        self.running = True
        self.app = Aplicacion
        pass
    
    def iniciar(self):
        super().__init__()
        
        self.thorpy()
        self.screen = super().getScreen()

        self.ejecucion()
        return
    
    def thorpy(self):
        ################## THORPY #########################
        # Declarar elementos de Thorpy
        thorpy.set_theme('human') # Tema

        slider = thorpy.SliderX.make(100, (12, 35), "My Slider")
        button = thorpy.make_button("Generar nueva pantalla", func= lambda: self.app.cambioDePantalla(3,self))
        
        # Encerrar elementos en una caja
        box = thorpy.Box.make(elements=[slider,button])
        # Encerrar elementos en un Menu
        self.menu = thorpy.Menu(box)
        # Declarar la pantalla como un elemento tipo surface
        for element in self.menu.get_population():
            element.surface = self.screen

        # Usar elementos de torpy
        box.set_topleft((100,100))
        button.set_main_color((255,0,0))
        box.blit()
        box.update()

    def ejecucion(self):
        while( self.running ):
            super().general_events(self) # Eventos generales
            for event in pygame.event.get(): 
                self.eventos(event)
            self.menu.react(event) # Thorpy
            self.update()
    
    def eventos(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        return
    
    def update(self):
        # Refrescar pantalla constantemente
        print('holamundo')
        pygame.display.update()
        return

