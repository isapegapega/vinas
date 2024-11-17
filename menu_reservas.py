from datetime import datetime 
import sqlite3
from menu_ventas import insertar_cliente, buscar_cliente

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
    print("1. Generar Reserva")
    print("2. Volver al menú de Reservas")

    try:
        opcion_de_reserva = int(input("Seleccione una opción: "))
    except ValueError:
        print("Por favor ingrese un número válido.")
        return  # Sale de la función si la entrada no es válida

    if opcion_de_reserva == 1:
        print("Usted ha seleccionado generar reserva.")
        cliente = None

        while not cliente:
            print("\nPor favor seleccione el tipo de cliente:")
            print("1. Cliente Nuevo")
            print("2. Cliente Existente")
            print("3. Cancelar")

            try:
                opcion_cliente = int(input("Seleccione una opción: "))
                if opcion_cliente == 1:
                    cliente = insertar_cliente()  # Supone que devuelve un cliente
                elif opcion_cliente == 2:
                    cliente = buscar_cliente()  # Supone que devuelve un cliente
                elif opcion_cliente == 3:
                    print("Operación cancelada.")
                    return
                else:
                    print("Opción inválida, intente de nuevo.")
            except ValueError:
                print("Por favor ingrese un número válido.")

        # Realiza la reserva solo si se encontró un cliente
        if cliente:
            realizar_reserva(cliente)
    elif opcion_de_reserva == 2:
        menu_reservas()
    else:
        print("Opción inválida, regresando al menú principal.")


#FUNCIONES PARA REALIZAR LA RESERVA
def mostrar_tours():

    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute('''SELECT id_tour, nombre_tour, fecha_tour,tipo_tour FROM tour''')#datos de tour
    tours = cursor.fetchall() #extrae los datos y los regresa en forma de tuplas

    print("-" * 30)

    for tour in tours :#tour
        print(f"ID: {tour[0]} | Tour: {tour[1]} | Fecha del tour: {tour[2]} | tipo de tour: {tour[3]} |")
    print("-" * 30)  

    conn.close()
    return tours    #return tour 


def realizar_reserva(cliente):
    print(f"Bienvenido {cliente['Nombre']} {cliente['Apellido']}!")

    print("Estos son los Tours disponibles para su compra:")
    tours = mostrar_tours()

    try:
        id_tour = int(input("Por favor seleccione el ID del tour que desea agregar a la compra: "))
        tour_seleccionado = next((p for p in tours if p[0] == id_tour), None)  # Busca coincidencias

        if not tour_seleccionado:
            print("Tour no encontrado, intente nuevamente.")
            return
        
        # Obtener el precio del tour seleccionado
        conn = sqlite3.connect('vinas_1.db')
        cursor = conn.cursor()
        
        # Consulta para obtener el precio_original asociado a un id_tour
        try:
            cursor.execute('''
                SELECT reserva.precio_original
                FROM reserva
                INNER JOIN reserva_tour ON reserva.id_reserva = reserva_tour.id_reserva
                WHERE reserva_tour.id_tour = ?
            ''', (id_tour,))

            # Obtener el resultado
            precio_unitario = cursor.fetchone()
            if precio_unitario:
                precio_unitario = precio_unitario[0]  # Extraer el valor de la tupla
                print(f"Precio Original asociado al id_tour {id_tour}: {precio_unitario}")
            else:
                print(f"No se encontró ninguna reserva para el id_tour {id_tour}.")
                return
        except sqlite3.OperationalError as e:
            print(f"Error al ejecutar la consulta: {e}")
            return
        
        # Solicitar la cantidad de acompañantes
        acompanante = int(input("Ingrese la cantidad de acompañantes que asistirán al tour: "))
        total = precio_unitario * (acompanante + 1)  # Incluye al comprador

        if acompanante != 0:
            print(f"Se registrarán {acompanante} acompañantes.")

            for i in range(acompanante):
                print(f"Registro del acompañante {i + 1}:")

                # Solicitar datos del acompañante
                nombre = input("Ingrese Nombre: ").strip()
                apellido = input("Ingrese Apellido: ").strip()
                relacion = input("Ingrese relación con el comprador: ").strip()

                # Validar si los campos están vacíos
                if not nombre or not apellido or not relacion:
                    print("Los datos del acompañante no pueden estar vacíos. Intente nuevamente.")
                    return

                # Insertar datos en la base de datos
                cursor.execute('''
                    INSERT INTO acompanante (nombre_acompanante, apellido_acompanante, relacion_con_comprador)
                    VALUES (?, ?, ?)
                ''', (nombre, apellido, relacion))
                conn.commit()
                print(f"Acompañante {nombre} {apellido} agregado exitosamente.")

            print(f"Se han registrado exitosamente {acompanante} acompañantes.")
        else:
            print("No se agregaron acompañantes.")
        
        # Aquí se asegura que siempre se muestra el resumen
        print("\nResumen de la reserva:")
        print("-" * 30)
        print(f"Tour: {tour_seleccionado[1]}")
        print(f"Acompañantes: {acompanante}")
        print(f"Precio unitario: ${precio_unitario}")
        print(f"Total a pagar: ${total:.2f}")  # Total correctamente calculado
        print(f"Fecha y hora de la reserva: {datetime.now().strftime('%d-%m-%Y %H:%M:%S')}")
        print("-" * 30)

        # Confirmar la reserva
        confirmacion = input("¿Desea confirmar la reserva? (s/n): ").strip().lower()
        if confirmacion == 's':
            try:
                # Insertar la reserva (sin id_tour)
                cursor.execute('''
                    INSERT INTO reserva (id_cliente, fecha_reserva, precio_original, estado_reserva)
                    VALUES (?, ?, ?, ?)
                ''', (cliente['id'], datetime.now().strftime('%d-%m-%Y %H:%M:%S'), precio_unitario, 'Confirmada'))
                conn.commit()

                # Obtener el id_reserva recién generado
                id_reserva = cursor.lastrowid

                # Insertar en la tabla intermedia reserva_tour para asociar la reserva con el tour
                cursor.execute('''
                    INSERT INTO reserva_tour (id_reserva, id_tour)
                    VALUES (?, ?)
                ''', (id_reserva, id_tour))
                conn.commit()

                print("¡Reserva confirmada! Muchas gracias por su compra.")
            except sqlite3.Error as e:
                print(f"Hubo un error al confirmar la reserva: {e}")
            finally:
                conn.close()
        else:
            print("La reserva ha sido cancelada.")
    
    except ValueError:
        print("Por favor, ingrese los datos correctamente.")
    finally:
        if conn:
            conn.close()