from menu_ventas import menu_ventas
from menu_tours import menu_tours
from menu_reservas import menu_reservas
from menu_productos import menu_productos
from menu_reservas import menu_reservas
from menu_informacion import menu_informacion

def menu_principal():
    
    Flag = True
    while Flag == True:
            
            print("\nBienvenido al Menú Principal")
            print("1. Ventas")
            print("2. Tours")
            print("3. Reservas")
            print("4. Productos")
            print("5. Información")
            print("6. Salir")

            try:
                opcion = int(input("\nSeleccione una opcion: \n"))

                if opcion == 1:
                    menu_ventas()
                elif opcion == 2:
                    menu_tours()
                elif opcion == 3:
                    menu_reservas()
                elif opcion == 4:
                    menu_productos()
                elif opcion == 5:
                    menu_informacion()
                elif opcion == 6:
                    print("Saliendo del menú...")
                    Flag = False
                else:
                    print("Opción no válida, intentelo de nuevo.")

            except ValueError:
                print ("Por favor ingrese un número entero valido.")
menu_principal()