import pygame
from pygame import Vector2
from sprites.meta import Meta
from sprites.bala import Bala
from sprites.obstaculo import Obstaculo

# Librerías when ganas
import random
from threading import Timer
from mapas import mapas as mapas

"""
SPRITE: Jugador
"""
class Player(pygame.sprite.Sprite):
    def __init__(self, pantalla, teclas, coord, color=(200,200,200), estilo=1):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)
        
        self.nombre = "Jugador "+str(estilo)
        self.player_img = pygame.image.load(f'assets/img/player{str(estilo)}.png')



        self.player_img = pygame.transform.scale(self.player_img,[32, 32])
        # self.player_img.fill((255,0,0))

        # Animaciones
        self.animaciones = self.a_arriba, self.a_izq, self.a_der, self.a_abajo = pygame.transform.rotate(self.player_img,0),pygame.transform.rotate(self.player_img,90),pygame.transform.rotate(self.player_img,270),pygame.transform.rotate(self.player_img,180)
        self.direccion = 0

        self.image = pygame.transform.rotate(self.a_izq,0)
        # self.image.set_colorkey((0,0,0))
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = coord[0], coord[1]
        self.objetos = []
        self.teclas = teclas
        self.pantalla = pantalla

    # Método: Update
    def update(self):
        self.teclado()
        pass
    
    # Método: Definir objetos de colisión
    def colision(self, objetos):
        self.objetos = objetos
    
    # Teclado
    def teclado(self):
        # for event in pygame.event.get():
        #     if event.type == pygame.KEYDOWN:
        #         if event.key == pygame.K_w:
        #             self.image = self.a_arriba
        #             self.mover(0,-2)
        #         elif event.key == pygame.K_a:
        #             self.image = self.a_izq
        #             self.mover(-2,0)
        #         elif event.key == pygame.K_d:
        #             self.image = self.a_der
        #             self.mover(2,0)
        #         elif event.key == pygame.K_s:
        #             self.image = self.a_abajo
        #             self.mover(0,2)
        keys = pygame.key.get_pressed()
        if keys[self.teclas[0]]:
            self.direccion = 270
            self.image = self.a_arriba
            self.mover(0,-10)
        elif keys[self.teclas[1]]:
            self.direccion = 180
            self.image = self.a_izq
            self.mover(-10,0)
        elif keys[self.teclas[2]]:
            self.direccion = 0
            self.image = self.a_der
            self.mover(10,0)
        elif keys[self.teclas[3]]:
            self.direccion = 90
            self.image = self.a_abajo
            self.mover(0,10)
        # if keys[pygame.K_SPACE]:
        #     self.disparar()
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
                    print(f'{self.nombre} ha ganado')
                    self.cambiarMapa()
                    pass
                elif type(objeto) == Bala:
                    print('has muerto')
                elif type(objeto) == Obstaculo:
                    print('has muerto')
                    self.kill()
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
        self.pantalla.balas_sprites.add(Bala(self.pantalla,self.rect.center, self.direccion))
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