import pygame
from pygame import Vector2
from utilidades.colores import *
from sprites.obstaculo import Obstaculo


BULLET_IMAGE = pygame.Surface((20, 11), pygame.SRCALPHA)
pygame.draw.polygon(BULLET_IMAGE, pygame.Color('red'),
                [(0, 0), (20, 5), (0, 11)])

class Bala(pygame.sprite.Sprite):

    def __init__(self, screen, pos, angle, estilo=1):
        super().__init__()

        self.estilo = estilo

        if estilo == 1:
            pygame.draw.polygon(BULLET_IMAGE, red,[(0, 0), (20, 5), (0, 11)])
        elif estilo == 2:
            pygame.draw.polygon(BULLET_IMAGE, green,[(0, 0), (20, 5), (0, 11)])
        elif estilo == 3:
            pygame.draw.polygon(BULLET_IMAGE, blue,[(0, 0), (20, 5), (0, 11)])
        elif estilo == 4:
            pygame.draw.polygon(BULLET_IMAGE, black,[(0, 0), (20, 5), (0, 11)])
        self.image = pygame.transform.rotate(BULLET_IMAGE, -angle)
        self.rect = self.image.get_rect(center=pos)
        # To apply an offset to the start position,
        # create another vector and rotate it as well.
        offset = Vector2(40, 0).rotate(angle)
        # Then add the offset vector to the position vector.
        self.pos = Vector2(pos) + offset  # Center of the sprite.
        # Rotate the direction vector (1, 0) by the angle.
        # Multiply by desired speed.
        self.velocity = Vector2(1, 0).rotate(angle) * 9
        self.pantalla = screen
        self.screen = screen.screen
        self.jugadores = screen.player_sprites

    def update(self):
        self.pos += self.velocity  # Add velocity to pos to move the sprite.
        self.rect.center = self.pos  # Update rect coords.

        screen_rect = self.screen.get_rect()
        if not screen_rect.contains(self.rect):
            self.kill()

        for jugador in self.jugadores:
            if self.rect.colliderect(jugador.rect):
                if jugador.estilo != self.estilo:
                    print(f'{jugador.nombre} ha muerto')
                    self.pantalla.mensajes = f'{jugador.nombre} ha muerto'
                    jugador.rect.center = (-50,-50)
                    if self.estilo == 1:
                        self.pantalla.p1score += 1
                    elif self.estilo == 2:
                        self.pantalla.p2score += 1
                    jugador.kill()
                    del(jugador)
        
        for muro in self.pantalla.walls:
            if self.rect.colliderect(muro.rect):
                if type(muro) == Obstaculo:
                    muro.rect.center = (-100,-100)
                    muro.kill()
                    del(muro)
                self.kill()

