import pygame, pyggel

class Player3D:

    """
    Player3D

    Clase que representa al jugador, su movimiento y configuración
    """
    def __init__(self, scene, coord, size=1, color=(255,255,0)):
        color = color[0]/255,color[1]/255,color[2]/255 # RGB a OpenGLColor
        # Crear la figura 3D
        self.image = pyggel.geometry.Cube(size, pos=coord, colorize=color)

        # Obtener ubicación
        self.pos = self.image.get_pos()
        
        # Dibujar la figura 3D
        scene.add_3d(self.image)

        # Guardar la anterior ubicación para colisiones
        self.old_pos = list(self.pos)

        # Guardar los lados del objeto
        self.get_sides()

    def update(self):
        self.get_sides()
        

        self.old_pos = list(self.pos) # Actualizar la anterior ubicación para colisiones
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w]:
            self.image.move(0,1/10,0)
            self.print_coord()
        if keys[pygame.K_s]:
            self.image.move(0,-1/10,0)
            self.print_coord()
        if keys[pygame.K_a]:
            self.image.move(-1/10,0,0)
            self.print_coord()
        if keys[pygame.K_d]:
            self.image.move(1/10,0,0)
            self.print_coord()

        # for w in self.obj_colision:
        #     r = [w.pos[0]-3.0, w.pos[1]-3.0, 6.0, 6.0]
        #     self.collide(r)
        pass
    
    def print_coord(self):
        # print(f'Coordenadas: {self.image.get_dimensions()}, 3D: {self.image.get_pos()[0:2]}')
        pass
    
    def collide(self, rect):
        # print(f'Coordenadas jugador: {self.image.get_pos()[0:2]}, objeto: {rect.pos}')
        #Collide n' slide.
        if self.collidepoint(self.pos, rect):
            #print [self.pos[0] - self.old_pos[0], self.pos[1] - self.old_pos[1]]
            
            print('colision')
            # if self.old_pos[0] >= rect[0]+rect[2] or self.old_pos[0] <= rect[0]:
            #     self.pos[0] = self.old_pos[0]
            # if self.old_pos[1] >= rect[1]+rect[3] or self.old_pos[1] <= rect[1]:
            #     self.pos[1] = self.old_pos[1]
    
    def colliderect(self, a, b):
        return a[0] + a[2] > b[0] and b[0] + b[2] > a[0] and a[1] + a[3] > b[1] and b[1] + b[3] > a[1]

    def collidepoint(self, a, b):
        if b[0] < a[0] and a[0] < b[0]+b[2]:
            if b[1] < a[1] and a[1] < b[1]+b[3]:
                return True
        return False
    
    def colision2D(self, a, b):
        # if b
        return False
    
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