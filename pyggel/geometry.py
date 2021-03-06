"""
pyggel.geometry
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.

The geometry module contains classes used to render 3d geometric primitives.
"""

import math

from pyggel.include import *
from pyggel import view, data, misc, math3d
from pyggel.data import Texture, BlankTexture
from pyggel.scene import BaseSceneObject

class Cube(BaseSceneObject):
    """A geometric cube that can be colored and textured"""
    def __init__(self, size, pos=(0,0,0), rotation=(0,0,0),
                 colorize=(1,1,1,1), texture=None, mirror=True,
                 hide_faces=[]):
        """Create a cube
           size is the absolute size of the cube
           pos is the position of the cube
           rotation is the rotation of the cube
           colorize is the color of the cube (0-1 RGBA)
           texture can be None, a data.Texture object or a string representing the filename of a texture to load
           mirror indicates whether each face of the cube has the full texture on it (so each is identicle) or
               if True, each face will have the entire texture mapped to it
               if False, the Texture is considered a cube map, like this:
                   blank, blank, top, blank,
                   back, left, front, right,
                   blank, blank, bottom, blank
           hide_faces must be a list of the sides of the cube not to add:
               acceptable values are left, right, top, bottom, back, front"""
        BaseSceneObject.__init__(self)

        self.hide_faces = hide_faces

        self.size = size
        self.pos = pos
        self.rotation = rotation
        if type(texture) is type(""):
            texture = Texture(texture)
        if texture:
            self.texture = texture
        self.colorize = colorize

        self.mirror = mirror

        self.corners = ((-1, -1, 1),#topleftfront
                      (1, -1, 1),#toprightfront
                      (1, 1, 1),#bottomrightfront
                      (-1, 1, 1),#bottomleftfront
                      (-1, -1, -1),#topleftback
                      (1, -1, -1),#toprightback
                      (1, 1, -1),#bottomrightback
                      (-1, 1, -1))#bottomleftback

        sides = ((7,4,0,3, 2, 2, 5),#left
                      (2,1,5,6, 3, 4, 4),#right
                      (7,3,2,6, 5, 0, 3),#top
                      (0,4,5,1, 4, 5, 2),#bottom
                      (3,0,1,2, 0, 1, 0),#front
                      (6,5,4,7, 1, 3, 1))#back
        self.sides = []
        if not "left" in hide_faces:
            self.sides.append(sides[0])
        if not "right" in hide_faces:
            self.sides.append(sides[1])
        if not "top" in hide_faces:
            self.sides.append(sides[2])
        if not "bottom" in hide_faces:
            self.sides.append(sides[3])
        if not "front" in hide_faces:
            self.sides.append(sides[4])
        if not "back" in hide_faces:
            self.sides.append(sides[5])

        self.normals = ((0, 0, 1), #front
                        (0, 0, -1), #back
                        (0, -1, 0), #top
                        (0, 1, 0), #bottom
                        (1, 0, 0), #right
                        (-1, 0, 0)) #left

        self.split_coords = ((2,2),#top
                             (0,1),#back
                             (1,1),#left
                             (2,1),#front
                             (3,1),#right
                             (2,0))#bottom

        self.scale = 1

        self.display_list = data.DisplayList()

        self._compile()

    def get_dimensions(self):
        """Return a tuple of the size of the cube - to be used by the quad tree and collision testing"""
        return self.size, self.size, self.size

    def get_pos(self):
        """Return the position of the quad"""
        return self.pos

    def _compile(self):
        """Compile the cube's rendering into a data.DisplayList"""
        self.display_list.begin()

        ox = .25
        oy = .33
        last_tex = None
        for i in self.sides:
            ix = 0
            x, y = self.split_coords[i[5]]
            x *= ox
            y *= oy
            if self.mirror:
                coords = ((1,1), (1,0), (0,0), (0,1))
            else:
                coords = ((x+ox, y+oy), (x+ox, y), (x, y), (x, y+oy))

            glBegin(GL_QUADS)

            glNormal3f(*self.normals[i[6]])

            for x in i[:4]:
                glTexCoord2fv(coords[ix])
                a, b, c = self.corners[x]
                glVertex3f(a,b,c)
                ix += 1
            glEnd()
        self.display_list.end()

    def render(self, camera=None):
        """Render the cube
           camera is None or the camera object the scene is using to render this object"""
        glPushMatrix()
        x, y, z = self.pos
        glTranslatef(x, y, -z)
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)
        glScalef(.5*self.size,.5*self.size,.5*self.size)
        try:
            if not self.scale==(1,1,1):
                glScalef(*self.scale)
        except:
            if not self.scale==1:
                glScalef(self.scale, self.scale, self.scale)
        glColor(*self.colorize)
        self.texture.bind()
        if self.outline:
            misc.outline(self.display_list, self.outline_color, self.outline_size)
        self.display_list.render()
        glPopMatrix()

    def copy(self):
        """Return a copy of the quad - uses the same display list"""
        n = Cube(self.size, self.pos, self.rotation, self.colorize, self.texture, self.mirror, self.hide_faces)
        n.display_list = self.display_list
        n.scale = self.scale
        return n

    def get_scale(self):
        """Return the scale of the object."""
        try: return self.scale[0], self.scale[1], self.scale[2]
        except: return self.scale, self.scale, self.scale

class Quad(Cube, BaseSceneObject):
    """A simple 3d square object."""
    def __init__(self, size, pos=(0,0,0), rotation=(0,0,0),
                 colorize=(1,1,1,1), texture=None, hide_faces=[]):
        """Create the Quad
           size is the quad
           pos is the position of the quad
           rotation is the rotation of the quad
           colorize is the color of the quad
           texture can be None, a string filename of an image to load or a data.Texture object - entire texture is mapped to the face
           hide_faces are the same as for Cube, except only front and back are allowed"""

        BaseSceneObject.__init__(self)
        self.size = size
        self.pos = pos
        self.rotation = rotation
        if type(texture) is type(""):
            texture = Texture(texture)
        if texture:
            self.texture = texture
        self.colorize = colorize

        self.scale = 1

        self.display_list = data.DisplayList()

        self.hide_faces = hide_faces

        self._compile()

    def _compile(self):
        """Compile the Quad into a data.DisplayList"""
        self.display_list.begin()

        glBegin(GL_QUADS)
        glNormal3f(0,1,0)
        if not "back" in self.hide_faces:
            glTexCoord2f(1,1)
            glVertex3f(-1,1,0)
            glTexCoord2f(0,1)
            glVertex3f(1, 1, 0)
            glTexCoord2f(0,0)
            glVertex3f(1, -1, 0)
            glTexCoord2f(1,0)
            glVertex3f(-1, -1, 0)
        if not "front" in self.hide_faces:
            glTexCoord2f(1,0)
            glVertex3f(-1, -1, 0)
            glTexCoord2f(0,0)
            glVertex3f(1, -1, 0)
            glTexCoord2f(0,1)
            glVertex3f(1, 1, 0)
            glTexCoord2f(1,1)
            glVertex3f(-1, 1, 0)
        glEnd()
        self.display_list.end()

    def copy(self):
        """Return a copy of the Quad, sharing the same display list"""
        n = Quad(self.size, self.pos, self.rotation, self.colorize, self.texture, self.hide_faces)
        n.scale = self.scale
        n.display_list = self.display_list
        return n

    def render(self, camera=None):
        """Render the Quad
           camera is None or the camera object the scene is using to render this object"""
        Cube.render(self, camera)

class Plane(Quad):
    """Like a Quad, except the texture is tiled on the face, which increases performance over a lot of quads tiled"""
    def __init__(self, size, pos=(0,0,0), rotation=(0,0,0),
                 colorize=(1,1,1,1), texture=None, tile=1, hide_faces=[]):
        """Create the Plane
           size of the plane
           pos is the position of the quad
           rotation is the rotation of the quad
           colorize is the color of the quad
           texture can be None, a string filename of an image to load or a data.Texture object - entire texture is mapped to the face
           tile is the number of times to tile the texture across the Plane
           hide_faces are the same as for a Quad"""

        self.tile = tile

        Quad.__init__(self, size, pos, rotation, colorize, texture, hide_faces)

    def _compile(self):
        """Compile Plane into a data.DisplayList"""
        self.display_list.begin()

        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_S, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_T, GL_REPEAT)
        glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_WRAP_R, GL_REPEAT)

        glBegin(GL_QUADS)
        glNormal3f(0,1,0)
        if not "back" in self.hide_faces:
            glTexCoord2f(self.tile,self.tile)
            glVertex3f(-1,1,0)
            glTexCoord2f(0,self.tile)
            glVertex3f(1, 1, 0)
            glTexCoord2f(0,0)
            glVertex3f(1, -1, 0)
            glTexCoord2f(self.tile,0)
            glVertex3f(-1, -1, 0)
        if not "front" in self.hide_faces:
            glTexCoord2f(self.tile,0)
            glVertex3f(-1, -1, 0)
            glTexCoord2f(0,0)
            glVertex3f(1, -1, 0)
            glTexCoord2f(0,self.tile)
            glVertex3f(1, 1, 0)
            glTexCoord2f(self.tile,self.tile)
            glVertex3f(-1, 1, 0)
        glEnd()
        self.display_list.end()

    def render(self, camera=None):
        """Render the Plane
           camera is None or the camera object the scene is using to render this object"""
        glPushMatrix()
        x, y, z = self.pos
        glTranslatef(x, y, -z)
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)
        s = self.size / self.tile if (self.size and self.tile) else self.size
        glScalef(.5*self.size,.5*self.size,.5*self.size)
        try:
            if not self.scale == (1,1,1):
                glScalef(*self.scale)
        except:
            if not self.scale == 1:
                glScalef(self.scale, self.scale, self.scale)
        glColor(*self.colorize)
        self.texture.bind()
        self.display_list.render()
        glPopMatrix()

    def copy(self):
        """Return a copy of the Plane - sharing the same display list..."""
        n = Plane(self.size, self.pos, self.rotation, self.colorize, self.texture, self.tile, self.hide_faces)
        n.scale = self.scale
        n.display_list = self.display_list
        return n

class Skybox(Cube):
    """A skybox object, which basically creates an infinitly far-away box, where all rendering is inside.
       Used to simulate a sky, or other things where you want to fill the view with something other than a blank color"""
    def __init__(self, texture, colorize=(1,1,1,1)):
        """Create the Skybox
           texture can be the same as a Cube, None, data.Texture, string filename or  list of 6 data.Texture objects
           colorize - the color of the Skybox"""
        Cube.__init__(self, 1, colorize=colorize, texture=texture, mirror=False)
        self._compile()

    def render(self, camera):
        """Render the Skybox
           camera is the camera object the scene is using to render the Skybox"""
        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE)
        gb_cull = glGetBooleanv(GL_CULL_FACE)
        glDisable(GL_CULL_FACE)

        glPushMatrix()
        camera.set_skybox_data()
        Cube.render(self)
        glPopMatrix()
        glDepthMask(GL_TRUE)
        if view.screen.lighting:
            glEnable(GL_LIGHTING)
        if gb_cull:
            glEnable(GL_CULL_FACE)

    def copy(self):
        """Return a copy of the Skybox - sharing the same data.DisplayList"""
        n = Skybox(self.texture, self.colorize)
        n.scale = self.scale
        n.display_list = self.display_list
        return n

class Sphere(BaseSceneObject):
    """A geometric Sphere object that can be colored and textured"""
    def __init__(self, size, pos=(0,0,0), rotation=(0,0,0),
                 colorize=(1,1,1,1), texture=None, detail=30, show_inside=False):
        """Create the Sphere
           size is the radius of the Sphere
           pos ithe position of the sphere
           rotation is the rotation of the sphere
           colorize is the color of the sphere
           texture can be None, a string filename of an image to load or a data.Texture object that will be mapped to the sphere
           detail is the level of detail for the Sphere, higher = a more smooth sphere
           show_inside indicates whether the inside of the sphere is rendered or not"""
        BaseSceneObject.__init__(self)

        self.size = size
        self.pos = pos
        self.rotation = rotation
        self.colorize = colorize
        if type(texture) is type(""):
            texture = Texture(texture)
        if texture:
            self.texture = texture
        self.detail = detail
        self.scale = 1
        self.show_inside = show_inside

        self.display_list = data.DisplayList()

        self._compile()

    def get_dimensions(self):
        """Return a three part tuple of the radius of the sphere - used in teh quadtree and collision testing"""
        return self.size, self.size, self.size

    def get_pos(self):
        """Return the position of the sphere"""
        return self.pos

    def _compile(self):
        """Compile the Sphere into a data.DisplayList"""
        self.display_list.begin()
        verts = []
        texcs = []
        norms = []

        space=self.detail

        for b in range(0, 180, space):
            b *= 1.0
            for a in range(0, 360, space):
                a *= 1.0
                _v = []
                _t = []
                for i in range(2):
                    for j in range(2):
                        s1 = space*i
                        s2 = space*j
                        x=math.sin(math3d.safe_div(a+s1, 180)*math.pi) * math.sin(math3d.safe_div(b+s2, 180)*math.pi)
                        z=math.cos(math3d.safe_div(a+s1, 180)*math.pi) * math.sin(math3d.safe_div(b+s2, 180)*math.pi)
                        y=math.cos(math3d.safe_div(b+s2, 180)*math.pi)
                        u=math3d.safe_div(a+s1,360)
                        v=math3d.safe_div(b+s2,360)
                        _v.append((x,y,z))
                        _t.append((u,1-v*2))
                verts.extend([_v[0], _v[1], _v[3], _v[0], _v[3], _v[2]])
                texcs.extend([_t[0], _t[1], _t[3], _t[0], _t[3], _t[2]])
                norms.extend([math3d.calcTriNormal(*verts[-6:-3])]*3)
                norms.extend([math3d.calcTriNormal(*verts[-3::])]*3)
                if self.show_inside:
                    verts.extend(reversed(verts[-6::]))
                    texcs.extend(reversed(texcs[-6::]))
                    norms.extend([math3d.calcTriNormal(*verts[-6:-3])]*3)
                    norms.extend([math3d.calcTriNormal(*verts[-3::])]*3)
        glBegin(GL_TRIANGLES)
        for i in range(len(verts)):
            u,v = texcs[i]
            glTexCoord2f(u,v)
            glNormal3f(*norms[i])
            x,y,z = verts[i]
            glVertex3f(x,y,z)
        glEnd()
        self.display_list.end()

    def render(self, camera=None):
        """Render the Sphere
           camera can be None or the camera object the scene is using"""
        glPushMatrix()
        x, y, z = self.pos
        glTranslatef(x, y, -z)
        a, b, c = self.rotation
        glRotatef(a, 1, 0, 0)
        glRotatef(b, 0, 1, 0)
        glRotatef(c, 0, 0, 1)
        glScalef(self.size, self.size, self.size)
        try:
            if not self.scale == (1,1,1):
                glScalef(*self.scale)
        except:
            if not self.scale == 1:
                glScalef(self.scale, self.scale, self.scale)
        glColor(*self.colorize)
        self.texture.bind()
        if self.outline:
            misc.outline(self.display_list, self.outline_color, self.outline_size)
        self.display_list.render()
        glPopMatrix()

    def copy(self):
        """Return a copy of the Sphere - sharing the same display list"""
        n = Sphere(self.size, self.pos, self.colorize, self.texture, self.detail)
        n.scale = self.scale
        n.display_list = self.display_list
        return n

    def get_scale(self):
        """Return the scale of the object."""
        try: return self.scale[0], self.scale[1], self.scale[2]
        except: return self.scale, self.scale, self.scale

class Skyball(Sphere):
    """A Skyball is like a Skybox - except it is a sphere intead of a cube"""
    def __init__(self, texture=None, colorize=(1,1,1,1), detail=30):
        """Create the Skyball
           texture can be None, a string filename or the data.Texture object to map to the Sphere"""
        Sphere.__init__(self, 1, colorize=colorize,
                        texture=texture, detail=detail)

    def render(self, camera):
        """Render the Skyball
           camera is the camera the scene is using"""
        glDisable(GL_LIGHTING)
        glDepthMask(GL_FALSE)
        gb_cull = glGetBooleanv(GL_CULL_FACE)
        glDisable(GL_CULL_FACE)

        glPushMatrix()
        camera.set_skybox_data()
        glRotatef(-90, 1, 0, 0)
        Sphere.render(self)
        glPopMatrix()
        glDepthMask(GL_TRUE)
        if view.screen.lighting:
            glEnable(GL_LIGHTING)
        if gb_cull:
            glEnable(GL_CULL_FACE)

    def copy(self):
        """Return a copy of teh Skyball - sharing the same dadta.DisplayList"""
        n = Skyball(self.texture, self.colorize, self.detail)
        n.scale = self.scale
        n.display_list = self.display_list
        return n
