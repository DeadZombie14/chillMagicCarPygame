


##################### Funcion principal ##################### 
def miprograma():
    empresas = []
    productos = []
    usuarios = [
            { 
                'ID': "1",
                'Nombre': "Pablo"
            }
        ]

    # Llamar a mi menu
    empresas.append(registrarEmpresa()) # Esto registra una empresa

    # for i in range(5, 8):
    while continuar != 0
        productos.append(registreProducto())
        continuar = input("Continuar? (0 = no)")


#################### /Funcion principal ##################### 


def registrarEmpresa():
    print("Hola")
    print("Dame el nombre de tu empresa:") 
    empresa = {
        'Nombre': str(input())
    } 
    return empresa

def registreProducto():
    print("Hola")
    print("Dame el nombre de tu producto:") 
    nombre = str(input())
    print("Dame el id de tu producto:") 
    id = str(input())
    producto = {
        'Nombre': nombre
        'id': id
    } 
    return producto




miprograma()





# print("Hola! Aqui estan los usuarios: \n")
# for usuario in usuarios:
#     print ("ID: " + usuario.get('ID'))
#     print ("Nombre: " + usuario.get('Nombre'))
        
# archivo = open("usuarios.txt","w+")
# for usuario in usuarios:
#     archivo.write("ID: " + usuario.get('ID') + "\n")
#     archivo.write("Nombre: " + usuario.get('Nombre') + "\n")

# print("Dame un nuevo nombre para el usuario: ")
# # usuarios[0].update({'Nombre':str(input())})
# usuarios[0]['Nombre'] = str(input())

# print("Hola! Aqui estan los usuarios: \n")
# for usuario in usuarios:
#     print ("ID: " + usuario.get('ID'))
#     print ("Nombre: " + usuario.get('Nombre'))