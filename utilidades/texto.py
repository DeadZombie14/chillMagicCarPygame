import pygame

class Texto:
    def __init__(self, screen, text, x, y, text_size = 20, fuente = 'Calibri', italic = False, bold= False, subrayado= False, color = (250, 240, 230), bg = [] ):
        
        self.screen = screen

        fg = color

        self.coord = x, y

        #load font, prepare values
        font = pygame.font.Font(None, 80)
        size = font.size(text)

        # Font
        a_sys_font = pygame.font.SysFont(fuente, text_size)

        # Cursiva
        if italic:
            a_sys_font.set_bold(1)
        # Negritas
        if bold:
            a_sys_font.set_bold(1)
        # Subrayado
        if subrayado:
            a_sys_font.set_underline(1)

        # Construccion del texto
        if len(bg) > 1: # Si hay fondo de texto        
            ren = a_sys_font.render(text, 1, fg, bg)
        else: # Si no, transparente
            ren = a_sys_font.render(text, 1, fg)
        # self.size = x+size[0], y
        self.text_rect = ren.get_rect()
        self.text_rect.center = (x,y)

        self.image = ren, (x,y)
        
        screen.blit(ren, (x, y))

        # Cursiva
        if italic:
            a_sys_font.set_bold(0)
        # Negritas
        if bold:
            a_sys_font.set_bold(0)
        # Subrayado
        if subrayado:
            a_sys_font.set_underline(0)
        
        
        # self.image.blit(ren, self.text_rect)
        # self.text_rect = (x, y),ren.get_size()
        # text = str(self.counter)
        # label = self.myfont.render(text, 1, (255,0,0))
        # text_rect = label.get_rect()
        # text_rect.center = (50,50)

        # self.image.blit(label, text_rect)
        
        pass

    def getProperties(self):
        return self.text_rect
    
    def redraw(self):
        self.screen.blit(self.image[0], self.image[1])
        pass
    

##################### EJEMPLO DE USO ##############################
# texto1 = Texto(screen, 'Hola', 10, 10)

class TextArea():
    def __init__(self, screen, text, x, y, fuente='Calibri', text_size = 20, color=pygame.Color('black')):
        self.coord = x, y
        font = pygame.font.SysFont(fuente, text_size)
        words = [word.split(' ') for word in text.splitlines()]  # 2D array where each row is a list of words.
        space = font.size(' ')[0]  # The width of a space.
        max_width, max_height = screen.get_size()
        pos = x,y
        for line in words:
            for word in line:
                word_surface = font.render(word, 0, color)
                word_width, word_height = word_surface.get_size()
                if x + word_width >= max_width:
                    x = pos[0]  # Reset the x.
                    y += word_height  # Start on new row.
                screen.blit(word_surface, (x, y))
                x += word_width + space
            x = pos[0]  # Reset the x.
            y += word_height  # Start on new row.
            self.size = word_width, word_height
        pass 
    
    def getProperties(self):
        return self.size, self.coord

##################### EJEMPLO DE USO ##############################
# textarea1 = Textarea(screen, 'Hola mundo que tal estas hoy')