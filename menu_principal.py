from menu_ventas import menu_ventas
# from menu_tours import menu_tours
# from menu_reservas import menu_reservas
from menu_productos import menu_productos


def menu_principal():
    
    print("\nBienvenido al bla bla bla bla bla")
    print("1. Ventas")
    print("2. Tours")
    print("3. Reservas")
    print("4. Productos")
    print("5. Salir")

    Flag = True
    while Flag == True:
            try:
                opcion = int(input("\nSeleccione una opcion: \n"))

                if opcion == 1:
                    menu_ventas()
                # elif opcion == 2:
                #     menu_tours()
                # elif opcion == 3:
                #     menu_reservas()
                # elif opcion == 4:
                    menu_productos()
                elif opcion == 5:
                    print("Saliendo del menú...")
                    Flag = False
                else:
                    print("Opción no válida, intentelo de nuevo.")

            except ValueError:
                print ("Por favor ingrese un número entero valido.")
menu_principal()