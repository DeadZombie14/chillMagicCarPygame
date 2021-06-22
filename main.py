import pantallas.menu as screen1
import pantallas.pantalla1 as screen2
import pantallas.pantalla2 as screen3
import pantallas.pantalla3 as screen4
import pantallas.pantallaSonido as screen5
import pantallas.pantalla3D as screen6
import pygame
############################### Llamado a las funciones ########################################
class Main:
    def __init__(self):
        self.cambioDePantalla(1, None)
        pass
    # Función: Cambio entre pantallas - Permite cambiar entre pantallas...
    def cambioDePantalla(self, pantalla, old_pantalla, config = {}):
        if old_pantalla:
            # pygame.mixer.music.stop()
            old_pantalla.running = False
            del(old_pantalla)
        if pantalla == 1:
            menu = screen1.MenuPrincipal(self)
            menu.iniciar()
        elif pantalla == 2:
            pantalla1 = screen2.Pantalla1(self, config)
            pantalla1.iniciar()
            pass
        elif pantalla == 3:
            pantalla2 = screen3.Pantalla2(self)
            pantalla2.iniciar()
            pass
        elif pantalla == 4:
            pantalla2 = screen4.Pantalla3(self)
            pantalla2.iniciar()
            pass
        elif pantalla == 5:
            pantalla4 = screen5.PantallaSonido(self)
            pantalla4.iniciar()
            pass
        elif pantalla == 6:
            pantalla6 = screen6.Pantalla1(self)
            pantalla6.iniciar()
            pass
        else:
            pass

# Primera función que se ejecuta
# Aqui se hacen todas las llamadas a las clases
Aplicacion = Main()
