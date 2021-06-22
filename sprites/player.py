import pygame
from pygame import Vector2
from sprites.meta import Meta
from sprites.bala import Bala
from sprites.obstaculo import Obstaculo

# Librerías when ganas
import random
from threading import Timer
from mapas import mapas as mapas

from utilidades.colores import *

"""
SPRITE: Jugador
"""
class Player(pygame.sprite.Sprite):
    def __init__(self, pantalla, teclas, coord, color=(200,200,200), estilo=1):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.nombre = "Jugador "+str(estilo)
        self.player_img = pygame.image.load(f'assets/img/player1.png')
        self.player_img = pygame.transform.scale(self.player_img,[32, 32])

        self.estilo = estilo



        def color_surface(surface, color):
            arr = pygame.surfarray.pixels3d(surface)
            arr[:,:,0] = color[0]
            arr[:,:,1] = color[1]
            arr[:,:,2] = color[2]

        coloredSurface = self.player_img.copy()
        if estilo == 1:
            color_surface(coloredSurface, red)
        elif estilo == 2:
            color_surface(coloredSurface, green)
        elif estilo == 3:
            color_surface(coloredSurface, blue)
        elif estilo == 4:
            color_surface(coloredSurface, black)
        self.player_img = coloredSurface

        # self.player_img = pygame.image.load(f'assets/img/player{str(estilo)}.png')



        # self.player_img.fill((255,0,0))

        # Animaciones
        self.animaciones = self.a_arriba, self.a_izq, self.a_der, self.a_abajo = pygame.transform.rotate(self.player_img,0),pygame.transform.rotate(self.player_img,90),pygame.transform.rotate(self.player_img,270),pygame.transform.rotate(self.player_img,180)
        self.direccion = 0

        self.image = pygame.transform.rotate(self.a_izq,0)
        # self.image.set_colorkey((0,0,0))

        self.rect = pygame.transform.scale(self.player_img,[32, 32]).get_rect()
        self.rect.x, self.rect.y = coord[0], coord[1]
        self.objetos = []
        self.teclas = teclas
        self.pantalla = pantalla
        self.speed = 32

    # Método: Update
    def update(self):
        # if self.rect.center % (32,32) != (0,0):
        #     self.rect.center = self.rect.center + self.rect.center % (32,32)
        self.teclado()
        pass
    
    # Método: Definir objetos de colisión
    def colision(self, objetos):
        self.objetos = objetos
    
    # Teclado
    def teclado(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == self.teclas[0]:
        #             self.direccion = 270
        #             self.image = self.a_arriba
        #             self.mover(0,-self.speed)
        #         elif event.key == self.teclas[1]:
        #             self.direccion = 180
        #             self.image = self.a_izq
        #             self.mover(-self.speed,0)
        #         elif event.key == self.teclas[2]:
        #             self.direccion = 0
        #             self.image = self.a_der
        #             self.mover(self.speed,0)
        #         elif event.key == self.teclas[3]:
        #             self.direccion = 90
        #             self.image = self.a_abajo
        #             self.mover(0,self.speed)



        keys = pygame.key.get_pressed()
        if keys[self.teclas[0]]:
            self.direccion = 270
            self.image = self.a_arriba
            self.mover(0,-self.speed)
            # self.rect.move_ip(0,-self.speed)
        elif keys[self.teclas[1]]:
            self.direccion = 180
            self.image = self.a_izq
            self.mover(-self.speed,0)
            # self.rect.move_ip(-self.speed,0)elf.rect.x%32
        elif keys[self.teclas[2]]:
            self.direccion = 0
            self.image = self.a_der
            self.mover(self.speed,0)
            # self.rect.move_ip(self.speed,0)elf.rect.x%32
        elif keys[self.teclas[3]]:
            self.direccion = 90
            self.image = self.a_abajo
            self.mover(0,self.speed)
            # self.rect.move_ip(0,self.speed)
        pass
    
    # Mover
    def mover(self, speedx, speedy):
        if speedx != 0:
            self.movimiento(speedx, 0)
        if speedy != 0:
            self.movimiento(0, speedy)
    def movimiento(self, speedx,speedy):
        self.rect.x += speedx
        self.rect.y += speedy

        for objeto in self.objetos:
            if self.rect.colliderect(objeto.rect):
                # if type(objeto) == Player:
                #     # self.kill()
                #     # self.rect.center = (-1,-1)
                #     pass
                if type(objeto) == Meta:
                    if objeto.estilo == self.estilo:
                        print(f'{self.nombre} ha ganado')
                        if objeto.estilo == 1:
                            self.pantalla.p1score += 1
                        elif objeto.estilo == 2:
                            self.pantalla.p2score += 1
                        self.cambiarMapa()
                    pass
                elif type(objeto) == Bala:
                    if objeto.estilo == self.estilo:
                        pass
                    else:
                        print('has muerto')
                        self.kill()
                # elif type(objeto) == Obstaculo:
                #     # if objeto.estilo == self.estilo:
                #     #     pass
                #     # else:
                #     # print('has muerto')
                #     # self.rect.center = (-50,-50)
                #     # self.kill()
                #     pass
                else:
                    if speedx > 0: # Moving right; Hit the left side of the wall
                        self.rect.right = objeto.rect.left
                    if speedx < 0: # Moving left; Hit the right side of the wall
                        self.rect.left = objeto.rect.right
                    if speedy > 0: # Moving down; Hit the top side of the wall
                        self.rect.bottom = objeto.rect.top
                    if speedy < 0: # Moving up; Hit the bottom side of the wall
                        self.rect.top = objeto.rect.bottom
    
    # Disparar
    def disparar(self):
        self.pantalla.balas_sprites.add(Bala(self.pantalla,self.rect.center, self.direccion, estilo=self.estilo))
        # print('disparaste')
        pass
    
    # Eventos
    def eventos(self, event):
        if event.key == self.teclas[4]:
            self.disparar()
        pass
    
    # Cambiar de mapa
    def cambiarMapa(self):
        # random.seed(9001)
        mapa = random.randrange(0,len(mapas.levels)) # Escojer mapa al azar
        self.pantalla.dibujarMapa(mapa)
        pass
