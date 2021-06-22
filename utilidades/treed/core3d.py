import pygame, math
import numpy as np

"""
LIBRERIA DE OBJETOS 3D BÁSICOS
==========================================
Esta librería proviene de un tutorial para renderizar formas simples usando matemática  y pygame.

Este archivo esta designado para dibujar en pantalla la forma especificada.
"""



# Radian rotated by a key event
ROTATION_AMOUNT = np.pi/16
MOVEMENT_AMOUNT = 10

key_to_function = {
    pygame.K_LEFT:   (lambda x: x.transform(translationMatrix(dx=-MOVEMENT_AMOUNT))),
    pygame.K_RIGHT:  (lambda x: x.transform(translationMatrix(dx= MOVEMENT_AMOUNT))),
    pygame.K_UP:     (lambda x: x.transform(translationMatrix(dy=-MOVEMENT_AMOUNT))),
    pygame.K_DOWN:   (lambda x: x.transform(translationMatrix(dy= MOVEMENT_AMOUNT))),
    pygame.K_EQUALS: (lambda x: x.scale(1.25)),
    pygame.K_MINUS:  (lambda x: x.scale(0.8)),
    pygame.K_q:      (lambda x: x.rotate('x', ROTATION_AMOUNT)),
    pygame.K_w:      (lambda x: x.rotate('x',-ROTATION_AMOUNT)),
    pygame.K_a:      (lambda x: x.rotate('y', ROTATION_AMOUNT)),
    pygame.K_s:      (lambda x: x.rotate('y',-ROTATION_AMOUNT)),
    pygame.K_z:      (lambda x: x.rotate('z', ROTATION_AMOUNT)),
    pygame.K_x:      (lambda x: x.rotate('z',-ROTATION_AMOUNT))
}

light_movement = {
    pygame.K_q:      (lambda x: x.transform(rotateXMatrix(-ROTATION_AMOUNT))),
    pygame.K_w:      (lambda x: x.transform(rotateXMatrix( ROTATION_AMOUNT))),
    pygame.K_a:      (lambda x: x.transform(rotateYMatrix(-ROTATION_AMOUNT))),
    pygame.K_s:      (lambda x: x.transform(rotateYMatrix( ROTATION_AMOUNT))),
    pygame.K_z:      (lambda x: x.transform(rotateZMatrix(-ROTATION_AMOUNT))),
    pygame.K_x:      (lambda x: x.transform(rotateZMatrix( ROTATION_AMOUNT)))
}

def translationMatrix(dx=0, dy=0, dz=0):
    """ Return matrix for translation along vector (dx, dy, dz). """
    
    return np.array([[1,0,0,0],
                     [0,1,0,0],
                     [0,0,1,0],
                     [dx,dy,dz,1]])

def translateAlongVectorMatrix(vector, distance):
    """ Return matrix for translation along a vector for a given distance. """
    
    unit_vector = np.hstack([unitVector(vector) * distance, 1])
    return np.array([[1,0,0,0],[0,1,0,0],[0,0,1,0], unit_vector])

def scaleMatrix(s, cx=0, cy=0, cz=0):
    """ Return matrix for scaling equally along all axes centred on the point (cx,cy,cz). """
    
    return np.array([[s,0,0,0],
                     [0,s,0,0],
                     [0,0,s,0],
                     [cx*(1-s), cy*(1-s), cz*(1-s), 1]])

def rotateXMatrix(radians):
    """ Return matrix for rotating about the x-axis by 'radians' radians """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[1,0, 0,0],
                     [0,c,-s,0],
                     [0,s, c,0],
                     [0,0, 0,1]])

def rotateYMatrix(radians):
    """ Return matrix for rotating about the y-axis by 'radians' radians """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[ c,0,s,0],
                     [ 0,1,0,0],
                     [-s,0,c,0],
                     [ 0,0,0,1]])

def rotateZMatrix(radians):
    """ Return matrix for rotating about the z-axis by 'radians' radians """
    
    c = np.cos(radians)
    s = np.sin(radians)
    return np.array([[c,-s,0,0],
                     [s, c,0,0],
                     [0, 0,1,0],
                     [0, 0,0,1]])

def rotateAboutVector(cvalues, coord, radians):
    cx,cy,cz = cvalues
    x,y,z = coord
    """ Rotate wireframe about given vector by 'radians' radians. """        
    
    # Find angle and matrix needed to rotate vector about the z-axis such that its y-component is 0
    rotZ = np.arctan2(y, x)
    rotZ_matrix = rotateZMatrix(rotZ)

    # Find angle and matrix needed to rotate vector about the y-axis such that its x-component is 0
    (x, y, z, _) = np.dot(np.array([x,y,z,1]), rotZ_matrix)
    rotY = np.arctan2(x, z)
    
    matrix = translationMatrix(dx=-cx, dy=-cy, dz=-cz)
    matrix = np.dot(matrix, rotZ_matrix)
    matrix = np.dot(matrix, rotateYMatrix(rotY))
    matrix = np.dot(matrix, rotateZMatrix(radians))
    matrix = np.dot(matrix, rotateYMatrix(-rotY))
    matrix = np.dot(matrix, rotateZMatrix(-rotZ))
    matrix = np.dot(matrix, translationMatrix(dx=cx, dy=cy, dz=cz))
    
    return matrix

class Wireframe:
    """ An array of vectors in R3 and list of edges connecting them. """
    
    def __init__(self, nodes=None):
        self.nodes = np.zeros((0,4))
        self.edges = []
        self.faces = []
        
        if nodes:
            self.addNodes(nodes)

    def addNodes(self, node_array):
        """ Append 1s to a list of 3-tuples and add to self.nodes. """
        
        ones_added = np.hstack((node_array, np.ones((len(node_array),1))))
        self.nodes = np.vstack((self.nodes, ones_added))
    
    def addEdges(self, edge_list):
        """ Add edges as a list of 2-tuples. """
        
        # Is it better to use a for loop or generate a long list then add it?
        # Should raise exception if edge value > len(self.nodes)
        self.edges += [edge for edge in edge_list if edge not in self.edges]

    def addFaces(self, face_list, face_colour=(255,255,255)):
        for node_list in face_list:
            num_nodes = len(node_list)
            if all((node < len(self.nodes) for node in node_list)):
                #self.faces.append([self.nodes[node] for node in node_list])
                self.faces.append((node_list, np.array(face_colour, np.uint8)))
                self.addEdges([(node_list[n-1], node_list[n]) for n in range(num_nodes)])
    
    def output(self):
        if len(self.nodes) > 1:
            self.outputNodes()
        if self.edges:
            self.outputEdges()
        if self.faces:
            self.outputFaces()  
    
    def outputNodes(self):
        print ("\n --- Nodes --- ")
        for i, (x, y, z, _) in enumerate(self.nodes):
            print ("   %d: (%d, %d, %d)" % (i, x, y, z))

    def outputEdges(self):
        print ("\n --- Edges --- ")
        for i, (node1, node2) in enumerate(self.edges):
            print ("   %d: %d -> %d" % (i, node1, node2))
            
    def outputFaces(self):
        print ("\n --- Faces --- ")
        for i, nodes in enumerate(self.faces):
            # print ("   %d: (%s)" % (i, ", ".join(['%d' % n for n in nodes])))
            pass
    
    def transform(self, transformation_matrix):
        """ Apply a transformation defined by a transformation matrix. """
        
        self.nodes = np.dot(self.nodes, transformation_matrix)
    
    def findCentre(self):
        """ Find the spatial centre by finding the range of the x, y and z coordinates. """

        min_values = self.nodes[:,:-1].min(axis=0)
        max_values = self.nodes[:,:-1].max(axis=0)
        return 0.5*(min_values + max_values)
    
    def sortedFaces(self):
        return sorted(self.faces, key=lambda face: min(self.nodes[f][2] for f in face[0]))
    
    def update(self):
        """ Override this function to control wireframe behaviour. """
        pass
    
    def rotar_por_centro(self, eje, valor=math.pi/2):
        # Find rotation matrix
        (x,y,z) = self.findCentre()    
        translation_matrix = translationMatrix(-x, -y, -z)
        if eje == 'x':
            rotation_matrix = np.dot(translation_matrix, rotateXMatrix(valor))
        elif eje == 'y':
            rotation_matrix = np.dot(translation_matrix, rotateYMatrix(valor))
        elif eje == 'z':
            rotation_matrix = np.dot(translation_matrix, rotateZMatrix(valor))
        
        rotation_matrix = np.dot(rotation_matrix, -translation_matrix)
        self.transform(rotation_matrix)


class WireframeGroup:
    """ A dictionary of wireframes and methods to manipulate them all together. """
    
    def __init__(self):
        self.wireframes = {}
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
    
    def output(self):
        for name, wireframe in self.wireframes.items():
            print (name)
            wireframe.output()    
    
    def outputNodes(self):
        for name, wireframe in self.wireframes.items():
            print (name)
            wireframe.outputNodes()
    
    def outputEdges(self):
        for name, wireframe in self.wireframes.items():
            print (name)
            wireframe.outputEdges()
    
    def findCentre(self):
        """ Find the central point of all the wireframes. """
        
        # There may be a more efficient way to find the minimums for a group of wireframes
        min_values = np.array([wireframe.nodes[:,:-1].min(axis=0) for wireframe in self.wireframes.values()]).min(axis=0)
        max_values = np.array([wireframe.nodes[:,:-1].max(axis=0) for wireframe in self.wireframes.values()]).max(axis=0)
        return 0.5*(min_values + max_values)
    
    def transform(self, matrix):
        for wireframe in self.wireframes.values():
            wireframe.transform(matrix)

    def update(self):
        for wireframe in self.wireframes.values():
            wireframe.update()



"""
LIBRERIA DE OBJETOS 3D BÁSICOS
==========================================
Esta librería proviene de un tutorial para renderizar formas simples usando matemática  y pygame.
"""


def Cuboid(coord, sizes):
    x,y,z = coord
    w,h,d = sizes
    """ Return a wireframe cuboid starting at (x,y,z)
        with width, w, height, h, and depth, d. """

    cuboid = Wireframe()
    cuboid.addNodes(np.array([[nx,ny,nz] for nx in (x,x+w) for ny in (y,y+h) for nz in (z,z+d)]))
    cuboid.addFaces([(0,1,3,2), (7,5,4,6), (4,5,1,0), (2,3,7,6), (0,2,6,4), (5,7,3,1)])
    
    return cuboid
    
def Spheroid(coord, coord_r, resolution=10):
    x,y,z = coord
    rx,ry,rz = coord_r
    """ Returns a wireframe spheroid centred on (x,y,z)
        with a radii of (rx,ry,rz) in the respective axes. """
    
    spheroid   = Wireframe()
    latitudes  = [n*np.pi/resolution for n in range(1,resolution)]
    longitudes = [n*2*np.pi/resolution for n in range(resolution)]

    # Add nodes except for poles
    spheroid.addNodes([(x + rx*np.sin(n)*np.sin(m), y - ry*np.cos(m), z - rz*np.cos(n)*np.sin(m)) for m in latitudes for n in longitudes])

    # Add square faces to whole spheroid but poles
    num_nodes = resolution*(resolution-1)
    spheroid.addFaces([(m+n, (m+resolution)%num_nodes+n, (m+resolution)%resolution**2+(n+1)%resolution, m+(n+1)%resolution) for n in range(resolution) for m in range(0,num_nodes-resolution,resolution)])

    # Add poles and triangular faces around poles
    spheroid.addNodes([(x, y+ry, z),(x, y-ry, z)])
    spheroid.addFaces([(n, (n+1)%resolution, num_nodes+1) for n in range(resolution)])
    start_node = num_nodes-resolution
    spheroid.addFaces([(num_nodes, start_node+(n+1)%resolution, start_node+n) for n in range(resolution)])

    return spheroid
    
def HorizontalGrid(coord, dcoords, ncoords):
    x,y,z = coord
    dx,dz = dcoords
    nx,nz = ncoords
    """ Returns a nx by nz wireframe grid that starts at (x,y,z) with width dx.nx and depth dz.nz. """
    
    grid = Wireframe()
    grid.addNodes([[x+n1*dx, y, z+n2*dz] for n1 in range(nx+1) for n2 in range(nz+1)])
    grid.addEdges([(n1*(nz+1)+n2,n1*(nz+1)+n2+1) for n1 in range(nx+1) for n2 in range(nz)])
    grid.addEdges([(n1*(nz+1)+n2,(n1+1)*(nz+1)+n2) for n1 in range(nx) for n2 in range(nz+1)])
    
    return grid
    
def FractalLandscape(origin=(0,0,0), dimensions=(400,400), iterations=4, height=40):
    import random
    
    def midpoint(nodes):
        m = 1.0/ len(nodes)
        x = m * sum(n[0] for n in nodes) 
        y = m * sum(n[1] for n in nodes) 
        z = m * sum(n[2] for n in nodes) 
        return [x,y,z]
    
    (x,y,z) = origin
    (dx,dz) = dimensions
    nodes = [[x, y, z], [x+dx, y, z], [x+dx, y, z+dz], [x, y, z+dz]]
    edges = [(0,1), (1,2), (2,3), (3,0)]
    size = 2

    for i in range(iterations):
        # Add nodes midway between each edge
        for (n1, n2) in edges:
            nodes.append(midpoint([nodes[n1], nodes[n2]]))

        # Add nodes to the centre of each square
        squares = [(x+y*size, x+y*size+1, x+(y+1)*size+1, x+(y+1)*size) for y in range(size-1) for x in range(size-1)]
        for (n1,n2,n3,n4) in squares:
            nodes.append(midpoint([nodes[n1], nodes[n2], nodes[n3], nodes[n4]]))
        
        # Sort in order of grid
        nodes.sort(key=lambda node: (node[2],node[0]))
        
        size = size*2-1
        # Horizontal edge
        edges = [(x+y*size, x+y*size+1) for y in range(size) for x in range(size-1)]
        # Vertical edges
        edges.extend([(x+y*size, x+(y+1)*size) for x in range(size) for y in range(size-1)])
        
        # Shift node heights
        scale = height/2**(i*0.8)
        for node in nodes:
            node[1] += (random.random()-0.5)*scale
    
    grid = Wireframe(nodes)
    grid.addEdges(edges)
    
    return grid
    
if __name__ == '__main__':
    grid = FractalLandscape(origin = (0,400,0), iterations=1)
    grid.output()





##############################



class WireframeViewer(WireframeGroup):
    """ A group of wireframes which can be displayed on a Pygame screen """
    #DIBUJA el elemento en la pantalla especificada
    
    def __init__(self, screen, width, height):
        self.width = width
        self.height = height
        self.screen = screen
        
        self.wireframes = {}
        self.wireframe_colours = {}
        self.object_to_update = []
        
        self.displayNodes = False
        self.displayEdges = True
        self.displayFaces = True
        
        self.perspective = False #300.
        self.eyeX = self.width/2
        self.eyeY = 100
        self.view_vector = np.array([0, 0, -1])
        
        self.light = Wireframe()
        self.light.addNodes([[0, -1, 0]])
        
        self.min_light = 0.02
        self.max_light = 1.0
        self.light_range = self.max_light - self.min_light 
        
        self.background = (10,10,50)
        self.nodeColour = (250,250,250)
        self.nodeRadius = 4
        
        self.control = 0
    
    def addWireframe(self, name, wireframe):
        self.wireframes[name] = wireframe
        #   If colour is set to None, then wireframe is not displayed
        self.wireframe_colours[name] = (250,250,250)
    
    def addWireframeGroup(self, wireframe_group):
        # Potential danger of overwriting names
        for name, wireframe in wireframe_group.wireframes.items():
            self.addWireframe(name, wireframe)
    
    def scale(self, scale):
        """ Scale wireframes in all directions from the centre of the group. """
        
        scale_matrix = scaleMatrix(scale, self.width/2, self.height/2, 0)
        self.transform(scale_matrix)

    def rotate(self, axis, amount):
        (x, y, z) = self.findCentre()
        translation_matrix1 = translationMatrix(-x, -y, -z)
        translation_matrix2 = translationMatrix(x, y, z)
        
        if axis == 'x':
            rotation_matrix = rotateXMatrix(amount)
        elif axis == 'y':
            rotation_matrix = rotateYMatrix(amount)
        elif axis == 'z':
            rotation_matrix = rotateZMatrix(amount)
            
        rotation_matrix = np.dot(np.dot(translation_matrix1, rotation_matrix), translation_matrix2)
        self.transform(rotation_matrix)

    def display(self):
        # self.screen.fill(self.background)
        light = self.light.nodes[0][:3]
        spectral_highlight = self.light.nodes[0][:3] + self.view_vector
        spectral_highlight /= np.linalg.norm(spectral_highlight)
        
        for name, wireframe in self.wireframes.items():
            nodes = wireframe.nodes
            
            if self.displayFaces:
                for (face, colour) in wireframe.sortedFaces():
                    v1 = (nodes[face[1]] - nodes[face[0]])[:3]
                    v2 = (nodes[face[2]] - nodes[face[0]])[:3]
                    
                    normal = np.cross(v1, v2)
                    towards_us = np.dot(normal, self.view_vector)
                    
                    # Only draw faces that face us
                    if towards_us > 0:
                        normal /= np.linalg.norm(normal)
                        theta = np.dot(normal, light)
                        #catchlight_face = np.dot(normal, spectral_highlight) ** 25

                        c = 0
                        if theta < 0:
                            shade = self.min_light * colour
                        else:
                            shade = (theta * self.light_range + self.min_light) * colour
                        pygame.draw.polygon(self.screen, shade, [(nodes[node][0], nodes[node][1]) for node in face], 0)
                        
                        #mean_x = sum(nodes[node][0] for node in face) / len(face)
                        #mean_y = sum(nodes[node][1] for node in face) / len(face)
                        #pygame.draw.aaline(self.screen, (255,255,255), (mean_x, mean_y), (mean_x+25*normal[0], mean_y+25*normal[1]), 1)
            
                if self.displayEdges:
                    for (n1, n2) in wireframe.edges:
                        if self.perspective:
                            if wireframe.nodes[n1][2] > -self.perspective and nodes[n2][2] > -self.perspective:
                                z1 = self.perspective/ (self.perspective + nodes[n1][2])
                                x1 = self.width/2  + z1*(nodes[n1][0] - self.width/2)
                                y1 = self.height/2 + z1*(nodes[n1][1] - self.height/2)
                    
                                z2 = self.perspective/ (self.perspective + nodes[n2][2])
                                x2 = self.width/2  + z2*(nodes[n2][0] - self.width/2)
                                y2 = self.height/2 + z2*(nodes[n2][1] - self.height/2)
                                
                                pygame.draw.aaline(self.screen, colour, (x1, y1), (x2, y2), 1)
                        else:
                            pygame.draw.aaline(self.screen, colour, (nodes[n1][0], nodes[n1][1]), (nodes[n2][0], nodes[n2][1]), 1)

            if self.displayNodes:
                for node in nodes:
                    pygame.draw.circle(self.screen, colour, (int(node[0]), int(node[1])), self.nodeRadius, 0)
        
        # pygame.display.flip()

    def keyEvent(self, key):
        if key in key_to_function:
            key_to_function[key](self)
            #light_movement[key](self.light)

    # def run(self):
    #     """ Display wireframe on screen and respond to keydown events """
        
    #     running = True
    #     key_down = False
    #     while running:
    #         for event in pygame.event.get():
    #             if event.type == pygame.QUIT:
    #                 running = False
    #             elif event.type == pygame.KEYDOWN:
    #                 key_down = event.key
    #             elif event.type == pygame.KEYUP:
    #                 key_down = None
            
    #         if key_down:
    #             self.keyEvent(key_down)
            
    #         self.display()
            
    #     pygame.quit()


class ObtenerFigura:
    def __init__(self, screen, screenSize):
        self.screen = screen
        self.screenW, self.screenH = screenSize
        self.viewer = WireframeViewer(self.screen, self.screenW, self.screenH)

    
    def esfera(self, coord, size=(100,100,100), resolution=15, color=(255,0,0)):
        """ Create and display a sphere with surfaces. """
        x, y = coord
        figura = Spheroid((x, y, 20), size, resolution=resolution)
        self.viewer.addWireframe('sphere', figura)

        # Colour ball
        faces = self.viewer.wireframes['sphere'].faces
        for i in range( round(resolution/4) ):
            for j in range( round(resolution*2-4) ):
                f = i*(resolution*4-8) +j
                faces[f][1][1] = color[0]
                faces[f][1][2] = color[1]
            
        # Colour with lattitude
        #for (face, colour) in faces[::2]:
        #    colour[1] = 0
        #    colour[2] = 0
        
        print ("Created a sphere with %d faces." % len(self.viewer.wireframes['sphere'].faces))
        self.viewer.displayEdges = False
        return figura
    
    def cube(self, coord, size=(100,100,100)):
        """ Create and display a cube with surfaces. """
        x, y, z = coord
        figura = Cuboid((x,y,z), size)
        self.viewer.addWireframe('cube', figura)
        # Colour ball
        faces = self.viewer.wireframes['cube'].faces
        # for i in range( round(resolution/4) ):
        #     for j in range( round(resolution*2-4) ):
        #         f = i*(resolution*4-8) +j
        #         faces[f][1][1] = 255
        #         faces[f][1][2] = 255
            
        #Colour with lattitude
        for (face, colour) in faces[::2]:
           colour[1] = 255
           colour[2] = 176
        
        print ("Created a cube with %d faces." % len(self.viewer.wireframes['cube'].faces))
        self.viewer.displayEdges = False
        return figura
    
    def renderizar(self):
        self.viewer.display()


################################################################################
# EJEMPLO DE USO

"""
#Pantalla 1
class Pantalla1(App):
    def __init__(self, Aplicacion):
        self.running = True
        self.app = Aplicacion
        pass
    
    def iniciar(self):
        super(Pantalla1, self).__init__()
        self.thorpy()

        texto1 = Texto(self.screen,'HolaMundo',500,50)
        self.screen = super(Pantalla1, self).getScreen()
        self.screenSize = super(Pantalla1, self).getScreenSize()
        
        self.esfera = core3d.ObtenerFigura(self.screen,self.screenSize)
        self.cubo = core3d.ObtenerFigura(self.screen,self.screenSize)
        self.esfera.esfera((900,500))
        self.cubo.cube((300,300,300)) 
        
        

        self.ejecucion()
        return
    
    def thorpy(self):
        ################## THORPY #########################
        # Declarar elementos de Thorpy
        #Declaration of the application in which the menu is going to live.
        thorpy.set_theme('human') # Tema

        slider = thorpy.SliderX.make(100, (12, 35), "My Slider")
        button = thorpy.make_button("Generar nueva pantalla", func= lambda: self.app.cambioDePantalla(3,self))
        button2 = thorpy.make_button("Ir a sonido", func= lambda: self.app.cambioDePantalla(4,self))

        #Declaration of some elements...
        # useless1 = thorpy.Element.make("This button is useless.\nAnd you can't click it.")

        text = "This button also is useless.\nBut you can click it anyway."
        useless2 = thorpy.Clickable.make(text)

        draggable2 = thorpy.Draggable.make("Drag me!")

        quit_button = thorpy.make_button("Quit")
        quit_button.set_as_exiter()
        
        # Encerrar elementos en una caja
        box = thorpy.Box.make(elements=[slider,button,button2, useless2, draggable2, quit_button], size=(500,500))
        box.set_main_color((0, 0, 0, 255))
        box.center()
        self.menu = thorpy.Menu(box)
        # Declarar la pantalla como un elemento tipo surface
        for element in self.menu.get_population():
            element.surface = self.screen

        # Usar elementos de torpy
        box.set_topleft((100,100))
        button.set_main_color((255,0,0))
        self.box = box
        

    def ejecucion(self):
        while( self.running ):
            for event in pygame.event.get(): 
                self.eventos(event)
            # self.menu.react(event) # Thorpy
            self.update()
    
    def eventos(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        return
    
    def update(self):
        self.esfera.viewer.rotate('x',0.1)
        self.esfera.viewer.rotate('y',0.1)
        #Find rotation matrix
        # Refrescar pantalla constantemente
        pygame.display.update()
        # self.screen.fill((0,0,0))
        # self.box.blit() # Thorpy
        # self.box.update() # Thorpy
        self.esfera.viewer.display()
        self.cubo.viewer.display()
        return
"""