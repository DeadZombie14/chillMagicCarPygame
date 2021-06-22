import pygame, thorpy
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

from app import App

class Muro:

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, scene, coord, color, width, height):
        # Call the parent class (Sprite) constructor

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.image = pyggel.image.Image(self.image)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.image.pos = coord[0],coord[1]
        scene.add_2d(self.image)
    
    def update(self):
        pass
    

# Librería 3D
import pyggel

"""
Pantalla 3D
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

        self.pyggel()

        self.clock = pygame.time.Clock()

        self.ejecucion()
        return
    
    def pyggel(self):
        pyggel.init(screen_size=self.ScreenSize) #initialize everything
        #for now, pyggel.init just calls pyggel.view init...

        event_handler = pyggel.event.Handler()

        self.scene = pyggel.scene.Scene()

        self.camera = pyggel.camera.LookAtCamera((0,0,0), distance=20)

        light = pyggel.light.Light((0,100,0), (0.5,0.5,0.5,1), (1,1,1,1),
                                (50,50,50,10), (0,0,0), True)

        self.scene.add_light(light)

        #OK, let's make some stuff!

        # Declarar elementos
        cubos = (
            pyggel.geometry.Cube(1, pos=(-5, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-10, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-15, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-20, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-25, 50, 0), colorize=(1,0,0,1)),
            pyggel.geometry.Cube(1, pos=(-30, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-35, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-40, 0, 0)),
            pyggel.geometry.Cube(1, pos=(-45, 0, 0)),
        )
        # a.rotation = (45, 45, 0)
        sog = pyggel.misc.StaticObjectGroup(cubos)
        self.scene.add_3d(sog)
        skybox = pyggel.geometry.Skybox("assets/img/background_menu.jpg")
        self.scene.add_skybox(skybox)


        muro = Muro(self.scene,(100,100),(255,0,0),100,100)
        pass

    def thorpy(self):
        ################## THORPY #########################
        # Declarar elementos de Thorpy
        # thorpy.set_theme('human') # Tema

        # slider = thorpy.SliderX.make(100, (12, 35), "My Slider")
        # button = thorpy.make_button("Generar nueva pantalla", func= lambda: self.app.cambioDePantalla(3,self))
        
        # # Encerrar elementos en una caja
        # box = thorpy.Box.make(elements=[slider,button])
        # # Encerrar elementos en un Menu
        # self.menu = thorpy.Menu(box)
        # # Declarar la pantalla como un elemento tipo surface
        # for element in self.menu.get_population():
        #     element.surface = self.screen

        # # Usar elementos de torpy
        # box.set_topleft((100,100))
        # button.set_main_color((255,0,0))
        # box.blit()
        # box.update()
        pass

    def ejecucion(self):
        while( self.running ):
            super().general_events(self) # Eventos generales
            for event in pygame.event.get(): 
                self.eventos(event)
            # self.menu.react(event) # Thorpy
            self.update()
    
    def eventos(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        return
    
    def update(self):
        self.clock.tick(60) #limit FPS
        pyggel.view.set_title("FPS: %s"%int(self.clock.get_fps()))
        # Refrescar pantalla constantemente
        # print('holamundo')
        # pygame.display.update()
        pyggel.view.clear_screen()
        self.scene.render(self.camera)
        pyggel.view.refresh_screen()
        return

