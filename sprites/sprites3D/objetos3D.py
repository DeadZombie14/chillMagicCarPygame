import pygame
from pygame.locals import *

import math, random

import pyggel
from pyggel.misc import ObjectGroup as Group
from pyggel.misc import ObjectInstance

def colliderect(a, b):
    return a[0] + a[2] > b[0] and b[0] + b[2] > a[0] and a[1] + a[3] > b[1] and b[1] + b[3] > a[1]

def collidepoint(p, r):
    if r[0] < p[0] and p[0] < r[0]+r[2]:
        if r[1] < p[1] and p[1] < r[1]+r[3]:
            return True
    return False

class Object(ObjectInstance):
    
    def __init__(self, groups):
        self.grid_color = [0, 0, 0]
        ObjectInstance.__init__(self, groups)
        
    def draw(self, surface):
        surface.blit(self.image, self.rect)

class GameObject(Object):
    
    def __init__(self, game, obj=None, pos=[0, 0], rotation=0, height=0, color=[1, 1, 1, 1]):
        Object.__init__(self, self.groups)
        self.game = game
        self.scene = self.game.scene
        self.pos = [pos[0], pos[1]]
        self.rotation = rotation
        self.obj = obj
        self.height = height
        self.update_obj()
    
    def update_obj(self):
        if self.obj:
            self.obj.pos = (self.pos[0], self.height, self.pos[1])
            self.obj.rotation = (self.obj.rotation[0], self.rotation, self.obj.rotation[2])
    
    def move(self, amount, rotation):
        po=0.0174532925
        self.pos[0] -= math.sin(rotation[1]*po)*amount
        self.height += math.sin(rotation[0]*po)*amount
        self.pos[1] += math.cos(rotation[1]*po)*amount
        self.update_obj()
    
    def position(self, x, y, h=None):
        self.pos[0] = x
        self.pos[1] = y
        if h:
            self.height = h
    
    def rotate(self, dx, dy, dz):
        self.obj.rotation = (self.obj.rotation[0]+dx, self.obj.rotation[1]+dy, self.obj.rotation[2]+dz)
        self.rotation = self.obj.rotation[1]
    
    def rotate_to(self, x, y, z):
        self.obj.rotation = (x, y, z)
        self.rotation = self.obj.rotation[1]
    
    def update(self):
        self.update_obj()

class Player(GameObject):
    
    def __init__(self, game):
        GameObject.__init__(self, game, obj=None, pos=[10, 15], rotation=0, height=0)
        self.old_pos = list(self.pos)
        
    def update(self):
        self.old_pos = list(self.pos)
    
    def collide(self, rect):
        #Collide n' slide.
        if collidepoint(self.pos, rect):
            #print [self.pos[0] - self.old_pos[0], self.pos[1] - self.old_pos[1]]
            if self.old_pos[0] >= rect[0]+rect[2] or self.old_pos[0] <= rect[0]:
                self.pos[0] = self.old_pos[0]
            if self.old_pos[1] >= rect[1]+rect[3] or self.old_pos[1] <= rect[1]:
                self.pos[1] = self.old_pos[1]

class Wall(Object):
    
    def __init__(self, pos):
        Object.__init__(self, self.groups)
        self.pos = pos
    
    def get_sides(self):
        centro = self.image.get_pos()
        width = self.image.get_dimensions()[0]
        height = self.image.get_dimensions()[1]
        long = self.image.get_dimensions()[2]

        # Calcular lados
        self.center = centro 

        left = centro[0] - (width / 2) 
        self.left = ( left, centro[1], centro[2])

        right = centro[0] + (width / 2) 
        self.right = ( right, centro[1], centro[2])

        top = centro[1] - (height / 2) 
        self.top = ( centro[0], top, centro[2])

        bottom = centro[1] + (height / 2)
        self.bottom = ( centro[0], bottom, centro[2])

        front = centro[2] - (long / 2)
        self.front = ( centro[0], centro[1], front)

        behind = centro[2] + (long / 2)
        self.behind = ( centro[0], centro[1], behind)

        # print('LEFT: ',self.left)
        # print('RIGHT: ',self.right)
        # print('TOP: ',self.top)
        # print('BOTTOM: ',self.bottom)
        return
