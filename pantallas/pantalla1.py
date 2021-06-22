import pygame, thorpy
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

from app import App

# Sprites
from sprites.player import Player
from sprites.muro import Muro
from sprites.meta import Meta
from sprites.obstaculo import Obstaculo

from mapas import mapas # Mapas
from mapas import generarMapa as mapaRandom

"""
Pantalla 1
"""
class Pantalla1(App):
    def __init__(self, Aplicacion, config):
        self.running = True
        self.app = Aplicacion
        self.unJugador = config['unJugador']
        pass
    
    def iniciar(self):
        super().__init__()
        
        self.thorpy()

        self.p1score = 0
        self.p2score = 0

        
        self.screen = super().getScreen()
        self.screenSize = super().getScreenSize()
        
        self.sprites()
        self.mensajes = ''
        
        self.ejecucion()
        return
    
    def thorpy(self):
        ################## THORPY #########################
        # Declarar elementos de Thorpy
        
        # Encerrar elementos en una caja

        # Declarar la pantalla como un elemento tipo surface

        # Usar elementos de torpy

        # Elementos adicionales
        pass
    
    def ejecucion(self):
        while( self.running ):
            super().general_events(self) # Eventos generales
            for event in pygame.event.get(): 
                self.eventos(event)
            # self.menu.react(event) # Thorpy
            self.update()

    # Sprites del juego
    def sprites(self):
        self.all_sprites = pygame.sprite.Group()
        self.balas_sprites = pygame.sprite.Group()
        self.player_sprites = pygame.sprite.Group()
        self.walls = []


        self.dibujarMapa(0)                  

        pass
    
    def eventos(self, event):
        if event.type == pygame.QUIT:
            
            self.running = False
        if event.type == pygame.KEYDOWN:
            for sprite in self.player_sprites:
                sprite.eventos(event)
            pass
        elif event.type == pygame.KEYUP:
            pass
        return
    
    def update(self):
        # Render
        self.render()

        self.all_sprites.draw(self.screen)
        self.player_sprites.draw(self.screen)
        self.balas_sprites.draw(self.screen)
        self.all_sprites.update()
        self.player_sprites.update()
        self.balas_sprites.update()

        Texto(self.screen,self.mensajes, self.screenSize[0]/2, 0,30, color=(255,0,0))

        for puntuacion in self.puntuaciones:
            puntuacion.redraw()

        pygame.display.update()
        return
    
    def render(self):
        pygame.time.Clock().tick(60)
        self.screen.fill((192,192,192))
        return
    
    def dibujarMapa(self, numero):
        self.all_sprites.empty()
        self.player_sprites.empty()
        self.balas_sprites.empty()
        self.mensajes = ""
        self.puntuaciones = []
        self.walls = []
        # Crea el mapa
        if not self.unJugador:
            level = mapaRandom.generar_mapa(jugadores=2)
        else:
            level = mapaRandom.generar_mapa(jugadores=1)

        
        # level = mapas.levels[numero]


        # Parse the level string above. W = wall, E = exit, P = P1, J = P2
        x = y = 0
        for row in level:
            for col in row:
                if col == "W":
                    self.walls.append( Muro(self.screen,self.screenSize,(x,y),(0,0,0),32,32) )
                if col == "O":
                    self.walls.append( Obstaculo((x,y),(200,255,200),32,32))
                if col == "1":
                    self.walls.append( Meta(self.screen,self.screenSize,(x,y)) )
                    pass
                if col == "P":
                    self.player_sprites.add( Player(self,[pygame.K_w,pygame.K_a,pygame.K_d,pygame.K_s,pygame.K_SPACE], (x,y)) )
                    self.puntuaciones.append( Texto(self.screen, f"Puntuacion P1: {self.p1score}", 0, 0,30, color=(255,255,255)) )
                if not self.unJugador:
                    if col == "Q":
                        self.player_sprites.add( Player(self,[pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_RCTRL], (x,y), estilo=2) )
                        self.puntuaciones.append( Texto(self.screen, f"Puntuacion P2: {self.p2score}", 300, 0,30, color=(255,255,255)) )
                    if col == "2":
                        self.walls.append( Meta(self.screen,self.screenSize,(x,y), estilo=2) )
                x += 32
            y += 32
            x = 0   
        
        # players = [
        #     Player(self,[pygame.K_w,pygame.K_a,pygame.K_d,pygame.K_s,pygame.K_SPACE], (32,32)),
        #     Player(self,[pygame.K_UP,pygame.K_LEFT,pygame.K_RIGHT,pygame.K_DOWN,pygame.K_RCTRL], (96,32), estilo=2)
        # ]


        for wall in self.walls:
            self.all_sprites.add(wall)
        
        # for player in players:
        #     self.player_sprites.add(player)

        # Añadir colisión a todos los jugadores
        for player in self.player_sprites:
            objetos = self.walls # Arreglo de sprites que tienen colision
            jugadores = []
            for y in self.player_sprites:
                if player != y: # No enviar a si mismo como objeto de colisión
                    jugadores.append( y )
            player.colision(objetos + jugadores)
        pass


