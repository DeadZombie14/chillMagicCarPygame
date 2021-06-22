"""
pyggel.__init__
This library (PYGGEL) is licensed under the LGPL by Matthew Roe and PYGGEL contributors.
"""

PYGGEL_VERSION = "0.08-alpha4c"
from pyggel.include import *

from pyggel import mesh, view, image, camera, math3d, light
from pyggel import scene, font, geometry, misc, data
from pyggel import particle, event, gui

def quit():
    """Deinitialize PYGGEL..."""
    view.clear_screen()
    glFlush()
    pygame.quit()

init = view.init

def get_version():
    """Return the version string for PYGGEL."""
    return PYGGEL_VERSION
