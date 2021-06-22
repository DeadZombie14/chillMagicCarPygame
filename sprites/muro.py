import pygame

from utilidades.treed import core3d

class Muro(pygame.sprite.Sprite):

    # Constructor. Pass in the color of the block,
    # and its x and y position
    def __init__(self, screen,screenSize, coord, color, width, height):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self)

        # Create an image of the block, and fill it with a color.
        # This could also be an image loaded from the disk.
        self.image = pygame.Surface([width, height])
        self.image.fill(color)

        # Fetch the rectangle object that has the dimensions of the image
        # Update the position of this object by setting the values of rect.x and rect.y

        self.rect = pygame.Surface([28, 28]).get_rect()
        self.rect = self.image.get_rect()
        self.rect.x,self.rect.y = coord[0],coord[1]

        # self.cubo = core3d.ObtenerFigura(screen,screenSize)
        # self.cubo.cube((self.rect.x,self.rect.y,self.rect.y),size=(32,32,32)) 
        # self.cubo.viewer.rotate('x',0.5)
        # self.cubo.viewer.rotate('y',0.5)
    
    def update(self):
        # self.cubo.viewer.display()
        pass
    
    def draw(self):
        # self.cubo.viewer.display()
        pass
