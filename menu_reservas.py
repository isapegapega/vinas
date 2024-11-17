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
            elif opcion == 2:
                print("Eliminar Reserva")
                eliminar_reserva()
            elif opcion == 3:
               print("Modificar Reserva")
               modificar_reserva()
            elif opcion == 4:
                print("Buscar Reserva")
                buscar_reserva()
            elif opcion == 5:
                print("Mostrar Reserva")
                mostrar_reservas()
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


    print("¿Cómo desea buscar la reserva?")
    print("1. Buscar por ID de reserva")
    print("2. Buscar por correo electrónico del cliente")
    print("3. Volver al menú de Reservas")

    try:
        opcion_busqueda = int(input("Seleccione una opción: "))
    except ValueError:
        print("Por favor ingrese un número válido.")
        return  # Sale de la función si la entrada no es válida

    if opcion_busqueda == 1:
        # Buscar por ID de reserva
        id_reserva = input("Ingrese el ID de la reserva: ").strip()
        conn = sqlite3.connect('vinas_1.db')
        cursor = conn.cursor()

        query = '''
        SELECT 
            r.id_reserva,
            r.fecha_reserva,
            c.nombre_cliente || ' ' || c.apellido_cliente AS cliente,
            GROUP_CONCAT(t.nombre_tour) AS tours,
            r.total_reserva
        FROM reserva r
        JOIN cliente_reserva cr ON r.id_reserva = cr.id_reserva
        JOIN cliente c ON cr.id_cliente = c.id_cliente
        JOIN reserva_tour rt ON r.id_reserva = rt.id_reserva
        JOIN tour t ON rt.id_tour = t.id_tour
        WHERE r.id_reserva = ?
        GROUP BY r.id_reserva, r.fecha_reserva, cliente, r.total_reserva
        '''
        cursor.execute(query, (id_reserva,))

        reserva = cursor.fetchone()
        conn.close()

        if reserva:
            # Mostrar detalles de la reserva encontrada
            print("\nReserva encontrada:")
            print("-" * 60)
            print(f"ID Reserva: {reserva[0]}")
            print(f"Fecha de reserva: {reserva[1]}")
            print(f"Cliente: {reserva[2]}")
            print(f"Tours: {reserva[3]}")
            print(f"Total: ${reserva[4]:.2f}")
            print("-" * 60)
        else:
            print("No se encontró ninguna reserva con ese ID.")

    elif opcion_busqueda == 2:
        # Buscar por email de cliente
        email_cliente = input("Ingrese el correo electrónico del cliente: ").strip()
        conn = sqlite3.connect('vinas_1.db')
        cursor = conn.cursor()

        query = '''
        SELECT 
            r.id_reserva,
            r.fecha_reserva,
            c.nombre_cliente || ' ' || c.apellido_cliente AS cliente,
            GROUP_CONCAT(t.nombre_tour) AS tours,
            r.total_reserva
        FROM reserva r
        JOIN cliente_reserva cr ON r.id_reserva = cr.id_reserva
        JOIN cliente c ON cr.id_cliente = c.id_cliente
        JOIN reserva_tour rt ON r.id_reserva = rt.id_reserva
        JOIN tour t ON rt.id_tour = t.id_tour
        WHERE c.email_cliente = ?
        GROUP BY r.id_reserva, r.fecha_reserva, cliente, r.total_reserva
        '''
        cursor.execute(query, (email_cliente,))

        reservas = cursor.fetchall()
        conn.close()

        if reservas:
            # Mostrar todas las reservas encontradas
            print("\nReservas encontradas:")
            print("-" * 60)
            for idx, reserva in enumerate(reservas, start=1):
                print(f"Reserva #{idx}")
                print(f"ID Reserva: {reserva[0]}")
                print(f"Fecha de reserva: {reserva[1]}")
                print(f"Cliente: {reserva[2]}")
                print(f"Tours: {reserva[3]}")
                print(f"Total: ${reserva[4]:.2f}")
                print("-" * 60)
        else:
            print("No se encontraron reservas para ese correo electrónico.")

    elif opcion_busqueda == 3:
        # Volver al menú de reservas
        menu_reservas()

    else:
        print("Opción inválida, regresando al menú de reservas.")


#BUSCAR RESERVA
def buscar_reserva():
    print("¿Cómo desea buscar la reserva?")
    print("1. Buscar por ID de reserva")
    print("2. Buscar por correo electrónico del cliente")
    print("3. Volver al menú de Reservas")

    while True:
        opcion_busqueda = int(input("Seleccione una opción: "))
                      
        if opcion_busqueda == 1:
            # Buscar por ID de reserva
            id_reserva = input("Ingrese el ID de la reserva: ").strip()
            conn = sqlite3.connect('vinas_1.db')
            cursor = conn.cursor()

            query = '''
            SELECT 
                r.id_reserva,
                r.fecha_reserva,
                c.nombre_cliente || ' ' || c.apellido_cliente AS cliente,
                GROUP_CONCAT(t.nombre_tour) AS tours,
                r.precio_original
            FROM reserva r
            JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
            JOIN cliente c ON dr.id_cliente = c.id_cliente  -- Relación entre reserva y cliente a través de detalle_reserva
            JOIN reserva_tour rt ON r.id_reserva = rt.id_reserva
            JOIN tour t ON rt.id_tour = t.id_tour
            WHERE r.id_reserva = ?
            GROUP BY r.id_reserva, r.fecha_reserva, cliente, r.precio_original
            '''
            cursor.execute(query, (id_reserva,))

            reserva = cursor.fetchone()
            conn.close()

            if reserva:
                # Mostrar detalles de la reserva encontrada
                print("\nReserva encontrada:")
                print("-" * 60)
                print(f"ID Reserva: {reserva[0]}")
                print(f"Fecha de reserva: {reserva[1]}")
                print(f"Cliente: {reserva[2]}")
                print(f"Tours: {reserva[3]}")
                print(f"Total: ${reserva[4]:.2f}")
                print("-" * 60)
            else:
                print("No se encontró ninguna reserva con ese ID.")

        elif opcion_busqueda == 2:
            # Buscar por email de cliente
            email_cliente = input("Ingrese el correo electrónico del cliente: ").strip()
            conn = sqlite3.connect('vinas_1.db')
            cursor = conn.cursor()

            query = '''
            SELECT 
                r.id_reserva,
                r.fecha_reserva,
                c.nombre_cliente || ' ' || c.apellido_cliente AS cliente,
                GROUP_CONCAT(t.nombre_tour) AS tours,
                r.precio_original
            FROM reserva r
            JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
            JOIN cliente c ON dr.id_cliente = c.id_cliente  -- Relación entre reserva y cliente a través de detalle_reserva
            JOIN reserva_tour rt ON r.id_reserva = rt.id_reserva
            JOIN tour t ON rt.id_tour = t.id_tour
            WHERE c.email_cliente = ?
            GROUP BY r.id_reserva, r.fecha_reserva, cliente, r.precio_original
            '''
            cursor.execute(query, (email_cliente,))
        

            reservas = cursor.fetchall()
            conn.close()

            if reservas:
                # Mostrar todas las reservas encontradas
                print("\nReservas encontradas:")
                print("-" * 60)
                for idx, reserva in enumerate(reservas, start=1):
                    print(f"Reserva #{idx}")
                    print(f"ID Reserva: {reserva[0]}")
                    print(f"Fecha de reserva: {reserva[1]}")
                    print(f"Cliente: {reserva[2]}")
                    print(f"Tours: {reserva[3]}")
                    print(f"Total: ${reserva[4]:.2f}")
                    print("-" * 60)
            else:
                print("No se encontraron reservas para ese correo electrónico.")

        elif opcion_busqueda == 3:
            # Volver al menú de reservas
            menu_reservas()

        else:
            print("Opción inválida, regresando al menú de reservas.")


#ELIMINAR RESERVA
def eliminar_reserva():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    id_reserva = input("Ingrese el ID de la reserva que desea eliminar: ").strip()

    # Verificar si la reserva existe
    cursor.execute('''SELECT id_reserva FROM reserva WHERE id_reserva = ?''', (id_reserva,))
    reserva = cursor.fetchone()

    if reserva:
        confirmar_eliminacion = input(f"¿Seguro(a) que desea eliminar la reserva con ID {id_reserva} (s/n): ").strip().lower()
        if confirmar_eliminacion == "s":
            try:
                # Eliminar relaciones con otras tablas
                cursor.execute('''DELETE FROM reserva_tour WHERE id_reserva = ?''', (id_reserva,))
                cursor.execute('''DELETE FROM detalle_reserva WHERE id_reserva = ?''', (id_reserva,))
                # Eliminar la reserva
                cursor.execute('''DELETE FROM reserva WHERE id_reserva = ?''', (id_reserva,))
                conn.commit()
                print(f"La reserva con ID {id_reserva} ha sido exitosamente eliminada.")
            except Exception as e:
                print(f"Error al eliminar la reserva: {e}")
        else:
            print("Operación cancelada.")
    else:
        print(f"No se ha podido encontrar ninguna reserva con el ID {id_reserva}.")

    conn.close()


#MODIFICAR RESERVA
def modificar_reserva():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    id_reserva = input("Ingrese el ID de la reserva que desea modificar: ").strip()

    # Verificar si la reserva existe
    cursor.execute('''SELECT id_reserva FROM reserva WHERE id_reserva = ?''', (id_reserva,))
    reserva = cursor.fetchone()

    if reserva:
        print(f"\nReserva encontrada con ID {id_reserva}.")
        print("Seleccione qué desea modificar:")
        print("1. Modificar tours asociados")
        print("2. Modificar cliente asociado")
        print("3. Modificar fecha de la reserva")
        opcion = input("Ingrese su opción (1, 2 o 3): ").strip()

        if opcion == "1":
            # Mostrar tours actuales
            cursor.execute('''
                SELECT t.id_tour, t.nombre_tour
                FROM reserva_tour rt
                JOIN tour t ON rt.id_tour = t.id_tour
                WHERE rt.id_reserva = ?
            ''', (id_reserva,))
            tours = cursor.fetchall()

            print("\nTours actuales en la reserva:")
            for tour in tours:
                print(f"ID Tour: {tour[0]}, Nombre: {tour[1]}")

            # Solicitar nuevo tour o actualizar tours
            print("1. Agregar un nuevo tour")
            print("2. Eliminar un tour existente")
            print("3. Volver al menú")
            sub_opcion = input("Seleccione una opción: ").strip()

            if sub_opcion == "1":
                id_tour = input("Ingrese el ID del nuevo tour: ").strip()
                cursor.execute('SELECT id_tour FROM tour WHERE id_tour = ?', (id_tour,))
                tour = cursor.fetchone()
                if tour:
                    cursor.execute('''
                        INSERT INTO reserva_tour (id_reserva, id_tour)
                        VALUES (?, ?)
                    ''', (id_reserva, id_tour))
                    conn.commit()
                    print("El nuevo tour ha sido agregado a la reserva.")
                else:
                    print("El tour ingresado no existe.")
            elif sub_opcion == "2":
                id_tour = input("Ingrese el ID del tour que desea eliminar: ").strip()
                cursor.execute('''
                    DELETE FROM reserva_tour
                    WHERE id_reserva = ? AND id_tour = ?
                ''', (id_reserva, id_tour))
                conn.commit()
                print("El tour ha sido eliminado de la reserva.")
            elif sub_opcion == "3":
                print("Volviendo al menú...")
            else:
                print("Opción no válida.")

        elif opcion == "2":
            # Modificar cliente asociado
            nuevo_email = input("Ingrese el correo electrónico del nuevo cliente: ").strip()
            cursor.execute('SELECT id_cliente FROM cliente WHERE email_cliente = ?', (nuevo_email,))
            cliente = cursor.fetchone()
            if cliente:
                cursor.execute('''
                    UPDATE detalle_reserva
                    SET id_cliente = ?
                    WHERE id_reserva = ?
                ''', (cliente[0], id_reserva))
                conn.commit()
                print("El cliente asociado a la reserva ha sido actualizado.")
            else:
                print("No se encontró ningún cliente con el correo proporcionado.")

        elif opcion == "3":
            # Modificar fecha de la reserva
            nueva_fecha = input("Ingrese la nueva fecha de la reserva (YYYY-MM-DD): ").strip()
            cursor.execute('''
                UPDATE reserva
                SET fecha_reserva = ?
                WHERE id_reserva = ?
            ''', (nueva_fecha, id_reserva))
            conn.commit()
            print("La fecha de la reserva ha sido actualizada.")

        else:
            print("Opción no válida.")
    else:
        print(f"No se encontró ninguna reserva con el ID {id_reserva}.")

    conn.close()


def mostrar_reservas():
    import sqlite3  # Asegúrate de que sqlite3 esté importado
    
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            r.id_reserva,
            r.fecha_reserva,
            c.nombre_cliente || ' ' || c.apellido_cliente AS cliente,
            GROUP_CONCAT(t.nombre_tour) AS tours,
            r.precio_original
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        JOIN cliente c ON dr.id_cliente = c.id_cliente
        JOIN reserva_tour rt ON r.id_reserva = rt.id_reserva
        JOIN tour t ON rt.id_tour = t.id_tour
        GROUP BY r.id_reserva, r.fecha_reserva, cliente, r.precio_original
        ORDER BY r.fecha_reserva DESC
    ''')

    reservas = cursor.fetchall()

    print("\nHistorial de Reservas:")
    print("-" * 60)
    if reservas:
        for reserva in reservas:
            print(f"ID Reserva: {reserva[0]}")
            print(f"Fecha: {reserva[1]}")
            print(f"Cliente: {reserva[2]}")
            print(f"Tours: {reserva[3]}")
            print(f"Total: ${reserva[4]:.2f}")
            print("-" * 60)
    else:
        print("No hay reservas registradas.")
        print("-" * 60)
    conn.close()