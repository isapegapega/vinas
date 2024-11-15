import sqlite3
from menu_principal import menu_principal
from menu_ventas import insertar_cliente,buscar_cliente
def menu_reservas():
    print("1. Agregar Reserva")
    print("2. Eliminar Reserva")
    print("3. Modificar Reserva")
    print("4. Buscar Reserva")
    print("5. Mostrar Reserva")
    print("6. Volver al menú principal")

    Flag = True
    while Flag == True:

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                print("Ha sido seleccionado agregar Reserva")
                agregar_reserva()
            # elif opcion == 2:
            #     print("Eliminar Reserva")
            #     eliminar_venta()
            # elif opcion == 3:
            #     print("Modificar Reserva")
            #     modificar_venta()
            # elif opcion == 4:
            #     print("Buscar Reserva")
            #     buscar_venta()
            # elif opcion == 5:
            #     print("Mostrar Reserva")
            #     mostrar_reserva()
            elif opcion == 6:
                menu_principal()
            else:
                print("Opción no válida, intentelo de nuevo.")

        except ValueError:
            print ("Por favor ingrese un número entero valido.")

#AGREGAR RESERVA
def agregar_reserva():
    print("\n1. Generar Reserva")
    print("2. Volver al menu de Reserva")
    opcion_de_reserva = int(input("Seleccione una opción: "))

    if opcion_de_reserva == 1:
        
        print("\nUsted ha seleccionado generar reserva.")
        cliente = None
        while not cliente:
            print("Por favor seleccione el tipo de cliente: ")
            print("1. Cliente Nuevo")
            print("2. Cliente Existente\n")

            try:
                opcion_cliente = int(input("Seleccione una opción"))
                if opcion_cliente == 1:
                    insertar_cliente()
                elif opcion_cliente == 2:
                    buscar_cliente()
                else:
                    print("Opción Invalida")
            except ValueError:
                print ("Por favor ingrese un número entero valido.")
        #realizar_reserva(cliente)
    if opcion_de_reserva == 2:
        menu_reservas()



