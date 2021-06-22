import pygame, thorpy
from utilidades.texto import Texto, TextArea
from utilidades.button import Button
from utilidades.colores import *

from app import App

"""
Menú Principal
"""
class MenuPrincipal(App):
    def __init__(self, Aplicacion):
        self.running = True
        self.app = Aplicacion
        pass
    
    def iniciar(self):
        super(MenuPrincipal, self).__init__() 
        self.screen = super(MenuPrincipal, self).getScreen()
        self.s_W, self.s_H = super(MenuPrincipal, self).getScreenSize() # Tamaño de la pantalla
        self.volumen = 100
        self.thorpy()

        pygame.mixer.music.load('assets/sound/menu.ogg')
        pygame.mixer.music.play()

        self.ejecucion()
        return
    
    def thorpy(self):
        ################## THORPY #########################
        # Declarar elementos de Thorpy
        thorpy.set_theme('human') # Tema

        buttonsMenu = [
            thorpy.make_button("Un jugador", func= lambda: self.jugar(1)),
            thorpy.make_button("Multijugador", func= lambda: self.jugar(2)),
            thorpy.make_button("Sonido"),
            thorpy.make_button("Pantalla Completa", func= lambda: super(MenuPrincipal, self).togglePantallaCompleta(self) ),
            thorpy.make_button("Seleccionar coches"),
            thorpy.make_button("Personalizar atributos"),
            # thorpy.make_button("Puntuaciones"),
            thorpy.make_button("Pantalla Prueba 3D", func= lambda: self.app.cambioDePantalla(6,self)),
            thorpy.make_button("Salir", func= thorpy.functions.quit_func),
        ]


        # Personalizar botones menú
        for boton in buttonsMenu:
            boton.set_size((250, 50))
            boton.set_font_size(20)
            boton.set_main_color((255,0,0))
            boton.set_font_color_hover((255,255,255))
            boton.set_main_color((255,1,0), state=thorpy.constants.STATE_PRESSED)
        
        contenedor1 = thorpy.Box.make(elements=buttonsMenu, size=(250, 500))
        contenedor1.center(y_shift=105)
        contenedor1.set_main_color((255,255,255,0))

        def cambiarV(event, sliderV):
            if event.el == sliderV:
                pygame.mixer.music.set_volume(sliderV.get_value()/100)

        # Sonido
        sliderV = thorpy.SliderX.make(length=100, limvals=(0, 100), text="Volumen:", type_=int, initial_value=100)
        sonido = thorpy.make_ok_box([sliderV],ok_text='Aceptar')
        launcher = thorpy.set_launcher(buttonsMenu[2], sonido)
        # launcher.func_after = lambda: cambiarV(sliderV)

        reaction1 = thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                                reac_func=cambiarV,
                                event_args={"id":thorpy.constants.EVENT_SLIDE},
                                params={"sliderV":sliderV},
                                reac_name="my reaction to slide event")
        sonido.add_reaction(reaction1)
        

        def escogerCoche(event):
            choices = [("I like blue",None), ("No! red",None), ("cancel",None)]
            thorpy.launch_nonblocking_choices("This is a non-blocking choices box!\n", choices)
            print("Proof that it is non-blocking : this sentence is printing!")
        
        # Seleccionar coches
        normal = "assets/img/player1.png"
        coche1 = thorpy.make_image_button_with_frame(normal,alpha=255, #opaque
        colorkey=(255,255,255)) #white=transparent
        coche1.add_reaction(thorpy.Reaction(reacts_to=thorpy.constants.THORPY_EVENT,
                              reac_func= escogerCoche,
                              event_args={"id":thorpy.constants.EVENT_UNPRESS}))
        imagen = thorpy.Image.make(path="assets/img/player3.png", color=(0,255,0),colorkey=(0,0,0))
        coches = thorpy.make_ok_box([coche1,imagen])
        thorpy.set_launcher(buttonsMenu[4], coches)


        # Personalizar atributos
        color_setter = thorpy.ColorSetter.make()
        color_launcher = thorpy.ColorSetterLauncher.make(color_setter,"Seleccionar color")
        atributos = thorpy.make_ok_box([color_launcher])
        thorpy.set_launcher(buttonsMenu[5], atributos)
        
        # Personalizar atributos
        color_setter = thorpy.ColorSetter.make()
        color_launcher = thorpy.ColorSetterLauncher.make(color_setter,"Seleccionar color")
        atributos = thorpy.make_ok_box([color_launcher])
        thorpy.set_launcher(buttonsMenu[3], atributos)

        
        
        #Declaration of some elements...
        title_element = thorpy.make_text("Overview example", 22, (255,255,0))
        
        
        background = thorpy.Background.make(image="assets/img/background_menu.jpg",mode="scale to screen",elements=[contenedor1,title_element])

        # Encerrar elementos en una caja
        self.box = thorpy.Box.make(elements=[background])
        self.box.center()

        # Encerrar elementos en un Menu
        self.menu = thorpy.Menu(self.box, fps=60)

        # Declarar la pantalla como un elemento tipo surface
        for element in self.menu.get_population():
            element.surface = self.screen
        thorpy.functions.set_current_menu(self.menu)
        self.box.blit()
        self.box.update()

    def ejecucion(self):
        while( self.running ):
            super().general_events(self) # Eventos generales
            for event in pygame.event.get(): 
                self.eventos(event)
            self.menu.react(event) # Thorpy
            self.update()
    
    def eventos(self, event):
        if event.type == pygame.QUIT:
            self.running = False
        return
    
    def update(self):
        
        image = pygame.image.load('assets/img/speeder.png')
        image = pygame.transform.scale(image, (60, 100)) # resize graphic
        image = image.convert_alpha() # remove whitespace from graphic
        self.screen.blit(image, (56,56))
        Texto(self.screen, 'Chill Magic Car', 213, 18, color=(255,0,0),text_size=80 , fuente='Calibri', subrayado=True, italic=True)
        TextArea(self.screen, 'Hola! Bienvenido al programa, por favor, selecciona una opción', 213, 120, color=(0,0,0))

        # Refrescar pantalla constantemente
        pygame.display.flip()
        return

    def jugar(self, cantidad):
        if cantidad == 1:
            self.app.cambioDePantalla(2,self,{'unJugador': True})
        else:
            self.app.cambioDePantalla(2,self,{'unJugador': False})

        pass