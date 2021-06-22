import pygame, thorpy
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

from app import App

from mapas import mapas

from sprites.sprites3D.player3D import Player3D
from sprites.sprites3D.muro3D import Muro3D

from sprites.sprites3D.objetos3D import *

class Muro2D:

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

        self.screen = pygame.display.set_mode((1024,640), pygame.OPENGL| pygame.DOUBLEBUF)

        self.pyggel()

        self.clock = pygame.time.Clock()

        self.ejecucion()
        return
    
    def pyggel(self):
        pyggel.init(screen_size=self.ScreenSize) #initialize everything
        #for now, pyggel.init just calls pyggel.view init...

        event_handler = pyggel.event.Handler()

        self.scene = pyggel.scene.Scene()

        self.camera = pyggel.camera.LookAtCamera((0,0,0), distance=25)

        light = pyggel.light.Light((0,100,0), (0.5,0.5,0.5,1), (1,1,1,1),
                                (50,50,50,10), (0,0,0), True)

        self.scene.add_light(light)
        skybox = pyggel.geometry.Skybox("assets/img/background_menu.jpg",colorize=(1,1,1,1))
        self.scene.add_skybox(skybox)

        #OK, let's make some stuff!

        # Declarar elementos
        # self.muros = [
        #     Muro3D(self.scene,(0,0,0)),
        # ]

        #Create starting objects
        self.objects = Group()
        self.walls = Group()
        Player.groups = [self.objects]
        Wall.groups = [self.objects, self.walls]


        static = []
        walls = []

        box = pyggel.geometry.Cube(1, colorize=(1,0,0,1))
        box.pos=(0,0,0)

        static.append(box)
        walls.append( Wall(box.pos) )
        # walls.append( Wall( [box.pos[0], box.pos[2] ]) )

        self.walls._objects = walls
        
        self.scene.add_3d(pyggel.misc.StaticObjectGroup(static))

        self.player = Player3D(self.scene, (1,1,0) )

        self.objects.add(self.player)

        pass

    def ejecucion(self):
        while( self.running ):
            for event in pygame.event.get(): 
                self.eventos(event)
            # self.menu.react(event) # Thorpy
            self.update()

    def dibujarMapa(self, numero):
        # Holds the level layout in a list of strings.
        level = mapas.levels[numero]
        # Parse the level string above. W = wall, E = exit, P = P1, J = P2
        x = y = 0
        # for row in level:
        #     for col in row:
        #         if col == "W":
        #             Muro(self.scene,(x,y),(255,0,0),100,100)
        #         if col == "O":
        #             self.walls.append( Obstaculo((x,y),(255,0,0),32,32))
        #         if col == "E":
        #             self.walls.append( Meta(self.screen,self.screenSize,(x,y)) )
        #             pass
        #         if col == "P":
        #             self.player_sprites.add( Player(self,[pygame.K_w,pygame.K_a,pygame.K_d,pygame.K_s,pygame.K_SPACE], (x,y)) )
        #         if col == "J":
        #             self.player_sprites.add( Player(self,[pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_RCTRL], (x,y), estilo=2) )
        #         x += 32
        #     y += 32
        #     x = 0   
        
        # players = [
        #     Player(self,[pygame.K_w,pygame.K_a,pygame.K_d,pygame.K_s,pygame.K_SPACE], (32,32)),
        #     Player(self,[pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_RCTRL], (96,32), estilo=2)
        # ]


        # for wall in self.walls:
        #     self.all_sprites.add(wall)
        
        # # for player in players:
        # #     self.player_sprites.add(player)

        # # Añadir colisión a todos los jugadores
        # for player in self.player_sprites:
        #     objetos = self.walls # Arreglo de sprites que tienen colision
        #     jugadores = []
        #     for y in self.player_sprites:
        #         if player != y: # No enviar a si mismo como objeto de colisión
        #             jugadores.append( y )
        #     player.colision(objetos + jugadores)
        pass




    def eventos(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        return
    
    def update(self):
        self.clock.tick(60) #limit FPS
        pyggel.view.set_title("FPS: %s"%int(self.clock.get_fps()))
        
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP]:
            self.camera.rotx -= .5
            pass
        if keys[pygame.K_RIGHT]:
            self.camera.roty += .5
            pass
        if keys[pygame.K_DOWN]:
            self.camera.rotx += .5
            pass
        if keys[pygame.K_LEFT]:
            self.camera.roty -= .5
            pass


        # Sprites
        # walls = []
        for w in self.walls:
            # print (f'Posición: {w.pos}')
            r = [w.pos[0], w.pos[1], 1.0, 1.0]
            # r = [w.pos[0]-1.0, w.pos[1]-1.0, 6.0, 6.0]
            self.player.collide(r) 
        
        self.player.update()


        # Refrescar pantalla constantemente
        pyggel.view.clear_screen()
        self.scene.render(self.camera)
        pyggel.view.refresh_screen()
        return

