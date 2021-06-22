import pygame
from pygame import Vector2

BULLET_IMAGE = pygame.Surface((20, 11), pygame.SRCALPHA)
pygame.draw.polygon(BULLET_IMAGE, pygame.Color('red'),
                [(0, 0), (20, 5), (0, 11)])

class Bala(pygame.sprite.Sprite):

    def __init__(self, screen, pos, angle):
        super().__init__()
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
                print(f'{jugador.nombre} ha muerto')
                self.pantalla.mensajes = f'{jugador.nombre} ha muerto'
                jugador.kill()
        
        for muro in self.pantalla.walls:
            if self.rect.colliderect(muro.rect):
                self.kill()

