import pygame
import time

pygame.init()

# Colores por defecto de los botones.
IMAGE_NORMAL = pygame.Surface((100, 32))
IMAGE_NORMAL.fill(pygame.Color('dodgerblue1'))
IMAGE_HOVER = pygame.Surface((100, 32))
IMAGE_HOVER.fill(pygame.Color('lightskyblue'))
IMAGE_DOWN = pygame.Surface((100, 32))
IMAGE_DOWN.fill(pygame.Color('aquamarine1'))

"""
LIBRERIA DE BOTONES
Permite crear botones de distintos colores y tamaños, también permite añadir una imagen en lugar de 
colores al boton.
"""
class Button(pygame.sprite.Sprite):

    def __init__(self, text, x, y, width, height, callback,
                 fuente='Calibri', text_color=(255, 255, 255), text_size=20,
                 color_normal=pygame.Color('dodgerblue1'), color_hover=pygame.Color('lightskyblue'),
                 color_down=pygame.Color('aquamarine1')):
        super().__init__()

        # x = x - (width/2)
        # y = y - (height/2)

        # Color
        image_normal = pygame.Surface((100, 32))
        image_normal.fill(color_normal)
        image_hover = pygame.Surface((100, 32))
        image_hover.fill(color_hover)
        image_down = pygame.Surface((100, 32))
        image_down.fill(color_down)


        # Fuente por defecto
        font = pygame.font.SysFont(fuente, text_size)

        # Escalar las imagenes al tamaño designado (no modifica las originales).
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
        self.image_down = pygame.transform.scale(image_down, (width, height))

        self.image = self.image_normal  # La imagen activa.
        self.rect = self.image.get_rect(topleft=(x, y))
        # Centrar la imagen y el texto.
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # Hacer blit del texto en las imagenes o cuadros de colores.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # Esta función es la que se llama cuando haces click.
        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Si el objeto colisiona con el mouse.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()  # Llamar la función.
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal

##################### EJEMPLO DE USO ##############################
# self.quit_button = Button(320, 240, 170, 65, salir(), 'Arial', 'Quit', (255, 255, 255))

class ImageButton(pygame.sprite.Sprite):

    def __init__(self, x, y, width, height, callback,image_normal: pygame.Surface, image_hover: pygame.Surface,
                 image_down: pygame.Surface,
                 fuente='Calibri', text='', text_color=(0, 0, 0), text_size=20,):
        super().__init__()

        # x = x - (width/2)
        # y = y - (height/2)

        # Fuente por defecto
        font = pygame.font.SysFont(fuente, text_size)

        # Escalar las imagenes al tamaño designado (no modifica las originales).
        self.image_normal = pygame.transform.scale(image_normal, (width, height))
        self.image_hover = pygame.transform.scale(image_hover, (width, height))
        self.image_down = pygame.transform.scale(image_down, (width, height))

        self.image = self.image_normal  # La imagen activa.
        self.rect = self.image.get_rect(topleft=(x, y))
        # Centrar la imagen y el texto.
        image_center = self.image.get_rect().center
        text_surf = font.render(text, True, text_color)
        text_rect = text_surf.get_rect(center=image_center)
        # Hacer blit del texto en las imagenes o cuadros de colores.
        for image in (self.image_normal, self.image_hover, self.image_down):
            image.blit(text_surf, text_rect)

        # Esta función es la que se llama cuando haces click.
        self.callback = callback
        self.button_down = False

    def handle_event(self, event):
        if event.type == pygame.MOUSEBUTTONDOWN:
            if self.rect.collidepoint(event.pos):
                self.image = self.image_down
                self.button_down = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # Si el objeto colisiona con el mouse.
            if self.rect.collidepoint(event.pos) and self.button_down:
                self.callback()  # Llamar la función.
                self.image = self.image_hover
            self.button_down = False
        elif event.type == pygame.MOUSEMOTION:
            collided = self.rect.collidepoint(event.pos)
            if collided and not self.button_down:
                self.image = self.image_hover
            elif not collided:
                self.image = self.image_normal

##################### EJEMPLO DE USO ##############################
# self.quit_button = Button(320, 240, 170, 65, salir(), 'Arial', 'Quit', (255, 255, 255))


class DynamicButton:
    def __init__(self, screen, msg, x, y, button_width, button_height, ic = 'green', ac= 'bright_green', action=None, fuente = 'comicsansms', it='black', at="black"):

        # x = x - (button_width/2)
        # y = y - (button_height/2)

        self.bloqueo = False
        # Colores
        self.black = (0, 0, 0)
        self.white = (255, 255, 255)
        self.red = (200, 0, 0)
        self.green = (0, 200, 0)
        self.bright_red = (255, 0, 0)
        self.bright_green = (0, 255, 0)
        self.block_color = (53, 115, 255)

        if ic == 'green':
            ic = self.green
        elif ic == 'black':
            ic = self.black
        elif ic == 'white':
            ic = self.white
        elif ic == 'red':
            ic = self.red
        elif ic == 'bright_red':
            ic = self.bright_red
        elif ic == 'bright_green':
            ic = self.bright_green
        elif ic == 'block_color':
            ic = self.block_color
        else:
            ic == 'black'
        
        if ac == 'green':
            ac = self.green
        elif ac == 'black':
            ac = self.black
        elif ac == 'white':
            ac = self.white
        elif ac == 'red':
            ac = self.red
        elif ac == 'bright_red':
            ac = self.bright_red
        elif ac == 'bright_green':
            ac = self.bright_green
        elif ac == 'block_color':
            ac = self.block_color
        else:
            ac == 'black'
        
        if it == 'green':
            it = self.green
        elif it == 'black':
            it = self.black
        elif it == 'white':
            it = self.white
        elif it == 'red':
            it = self.red
        elif it == 'bright_red':
            it = self.bright_red
        elif it == 'bright_green':
            it = self.bright_green
        elif it == 'block_color':
            it = self.block_color
        else:
            it == 'black'
        
        if at == 'green':
            at = self.green
        elif at == 'black':
            at = self.black
        elif at == 'white':
            at = self.white
        elif at == 'red':
            at = self.red
        elif at == 'bright_red':
            at = self.bright_red
        elif at == 'bright_green':
            at = self.bright_green
        elif at == 'block_color':
            at = self.block_color
        else:
            at == 'black'

        mouse = pygame.mouse.get_pos()
        click = pygame.mouse.get_pressed()

        if x + button_width > mouse[0] > x and y + button_height > mouse[1] > y:
            pygame.draw.rect(screen, ac, (x, y, button_width, button_height))
            # Constructor del texto: Hover
            smallText = pygame.font.SysFont(fuente, 20)
            textSurf, textRect = self.text_objects(msg, smallText, at)
            textRect.center = ((x + (button_width / 2)), (y + (button_height / 2)))
            screen.blit(textSurf, textRect)
            # Evento: click
            if click[0] == 1 and action != None and not self.bloqueo:
                action()
                self.bloqueo = True
                time.sleep(1)
            else:
                self.bloqueo = False
        else:
            pygame.draw.rect(screen, ic, (x, y, button_width, button_height))
            # Constructor del texto
            smallText = pygame.font.SysFont(fuente, 20)
            textSurf, textRect = self.text_objects(msg, smallText, it)
            textRect.center = ((x + (button_width / 2)), (y + (button_height / 2)))
            screen.blit(textSurf, textRect)
        pass

    def text_objects(self, text, font, color):
        textSurface = font.render(text, True, color)
        return textSurface, textSurface.get_rect()


##################### EJEMPLO DE USO ##############################
# ATENCIÓN: EL LLAMADO DEBE EJECUTARSE EN EL LOOP (UPDATE 60 FPS)
# boton1 = Button(screen, "Exit", 10, 10, 100, 50, ic="red", ac="black", fuente="Calibri", at="white")