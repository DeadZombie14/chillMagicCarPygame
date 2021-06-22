import pygame, pyggel

class Muro3D:

    """
    Muro3D

    Un simple cubo que representa un sprite en 3D
    """
    def __init__(self, scene, coord, size=1, color=(255,0,0)):
        color = color[0]/255,color[1]/255,color[2]/255 # RGB a OpenGLColor
        # Crear la figura 3D
        self.image = pyggel.geometry.Cube(size, pos=coord, colorize=color)

        # Obtener ubicación
        self.pos = self.image.get_pos()
        
        # Dibujar la figura 3D
        scene.add_3d(self.image)
        
    
    def update(self):
        # self.pos = self.image.get_pos()
        pass