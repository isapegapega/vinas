import sqlite3
def menu_ventas():

    print("\nMenú Venta")
    print("-"*30)
    print("1. Agregar Venta")
    print("2. Eliminar Venta")
    print("3. Modificar Venta")
    print("4. Buscar Venta")
    print("5. Mostrar Ventas")
    print("6. Salir")
    print("-"*30)

    Flag = True
    while Flag == True:

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                print("Ha sido seleccionado agregar venta")
                agregar_venta()
            elif opcion == 2:
                print("Eliminar Venta")
                eliminar_venta()
            elif opcion == 3:
                print("Modificar Venta")
                modificar_venta()
            elif opcion == 4:
                print("Buscar Venta")
                buscar_venta()
            elif opcion == 5:
                print("Mostrar Ventas")
                mostrar_ventas()
            elif opcion == 6:
                Flag = False
            else:
                print("Opción no válida, intentelo de nuevo.")

        except ValueError:
            print ("Por favor ingrese un número entero valido.")
#AGREGAR VENTA
def agregar_venta():
    print("\n1. Generar Venta")
    print("2. Volver al menu de ventas")
    opcion_de_venta = int(input("Seleccione una opción: "))

    if opcion_de_venta == 1:
        
        print("\nUsted ha seleccionado generar venta.")
        cliente = None
        while not cliente:
            print("Por favor seleccione el tipo de cliente: ")
            print("1. Cliente Nuevo")
            print("2. Cliente Existente\n")

            try:
                opcion_cliente = int(input("Seleccione una opción"))
                if opcion_cliente == 1:
                    cliente = insertar_cliente()
                    if cliente:  
                        realizar_compra(cliente)

                elif opcion_cliente == 2:
                    buscar_cliente()
                    if cliente:  
                        realizar_compra(cliente)
                else:
                    print("Opción Invalida")
            except ValueError:
                print ("Por favor ingrese un número entero valido.")
        
    if opcion_de_venta == 2:
        menu_ventas()
#FUNCIONES PARA LA BUSQUEDA DE CLIENTE
def insertar_cliente():
        print("Ingrese los datos del cliente: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Correo Electronico: ")
        telefono = input("Teléfono (sin +56 9): ")
        conn = sqlite3.connect('vinas_1.db')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                        INSERT INTO cliente (nombre_cliente, apellido_cliente, email_cliente, telefono_cliente
                        )
                        VALUES (?, ?, ?, ?)
                        ''', (nombre, apellido, email, telefono))
            conn.commit()
            print(f"Cliente {nombre} {apellido} fue agregado exitosamente")

            cliente = {'id':cursor.lastrowid, 'Nombre': nombre, 'Apellido': apellido, 'Email': email, 'Telefono': telefono}
            conn.close()
            return cliente
        except sqlite3.IntegrityError:
            print("Ya existe un cliente con ese correo electrónico.")
            conn.close()
            return None
def buscar_cliente():
    email = input("Ingrese el correo electronico del cliente a buscar: ").strip()

    #CONECTAR BASE DE DATOS
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()
    
    #BUSCAR CLIENTE
    cursor.execute('''SELECT * FROM cliente WHERE email_cliente = ?
                   ''', (email,))
    cliente = cursor.fetchone()

    if cliente:
        print(f"Cliente encontrado: {cliente[1]} {cliente[2]} - Email: {cliente[3]} - Teléfono: {cliente[4]}")
        cliente_dict = {'id': cliente[0], 'Nombre': cliente[1], 'Apellido': cliente[2], 'Email': cliente[3], 'Telefono': cliente[4]}
        conn.close()
        return cliente_dict
    else:
        print("Cliente no encontrado. Asegurese de que el correo utilizado sea el correcto")
        conn.close()
        return None
#FUNCIONES PARA REALIZAR LA COMPRA
def mostrar_productos():

    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute('SELECT id_producto, nombre_producto, precio_original, FROM producto')
    productos = cursor.fetchall()

    print("\nProductos disponibles:")
    print("-" * 30)
    for producto in productos:
        print(f"ID: {producto[0]} | Producto: {producto[1]} | Precio: ${producto[2]:.2f}")
    print("-" * 30)  

    conn.close()
    return productos     
def realizar_compra(cliente):
    print(f"\nBienvenido {cliente['nombre']} {cliente['apellido']}!")

    print("\nEstos son los productos disponibles para su compra:")
    productos = mostrar_productos()

    try:
        producto_id = int(input("Por favor seleccione el ID del producto que desea agregar a la compra: "))
        producto_seleccionado = next((p for p in productos if p[0] == producto_id), None)

        if not producto_seleccionado:
            print("Producto no encontrado, intente nuevamente.")
            return
        
        total = producto_seleccionado[2]

        print(f"Producto seleccionado: {producto_seleccionado[1]}, Precio: ${producto_seleccionado[2]}")

        confirmacion = input("¿Desea confirmar la compra? (s/n): ").strip().lower()
        if confirmacion == 's':
            conn = sqlite3.connect('vinas_1.db')
            cursor = conn.cursor()

            from datetime import datetime
            fecha_venta = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            cursor.execute('''
                INSERT INTO venta (fecha_venta, total_venta, id_descuento)
                VALUES (?, ?, ?)
            ''', (fecha_venta, total, 0))
            id_venta = cursor.lastrowid

            cursor.execute('''
                INSERT INTO cliente_venta (id_cliente, id_venta)
                VALUES (?, ?)
            ''', (cliente['id'], id_venta))

            cursor.execute('''
                INSERT INTO producto_venta (id_producto, id_venta)
                VALUES (?, ?)
            ''', (producto_seleccionado[0], id_venta))

            conn.commit()
            conn.close()
            print("La compra fue realizada con exito, ¡Muchas gracias!")
        else:
            print("La compra ha sido cancelada")
    except ValueError:
        print("Error: Por favor ingrese un número válido.")
#FUNCION PARA ELIMINAR UNA VENTA
def eliminar_venta():
    conn = sqlite3.connect('vina_1.db')
    cursor = conn.cursor()

    id_venta = int(input("Ingrese el ID de la venta que desea eliminar: ")).strip()
    cursor.execute('''SELECT id_venta FROM venta WHERE id_venta = ?''', (id_venta,))
    venta = cursor.fetchone()

    if venta:
        confirmar_eliminacion = input(f"¿Seguro(a) que desea eliminar la venta con ID {id_venta} (s/n): ").strip().lower()
        if confirmar_eliminacion == "s":
            try:
                cursor.execute('''DELETE FROM producto_venta WHERE id_venta = ?''', (id_venta,))
                cursor.execute('''DELETE FROM cliente_venta WHERE id_venta = ?''', (id_venta,))
                cursor.execute('''DELETE FROM venta WHERE id_venta = ?''', (id_venta,))
                conn.commit()
                print(f"La venta con ID {id_venta} ha sido exitosamente eliminada.")
            except Exception as e:
                print(f"Error al eliminar la venta: {e}")
        else:
            print("Operacion cancelada.")
    else:
        print(f"No se ha podido encontrar ninguna venta con el ID {id_venta}.")

    conn.close() 
#FUNCIÓN PARA MOSTRAR LA VENTA
def mostrar_ventas():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            v.id_venta,
            v.fecha_venta,
            c.nombre_cliente || ' ' || c.apellido_cliente AS cliente,
            GROUP_CONCAT(p.nombre_producto || ' (x' || pv.cantidad || ')') AS productos,
            v.total_venta
        FROM venta v
        JOIN venta_cliente cv ON v.id_venta = cv.id_venta
        JOIN cliente c ON cv.id_cliente = c.id_cliente
        JOIN producto_venta pv ON v.id_venta = pv.id_venta
        JOIN producto p ON pv.id_producto = p.id_producto
        GROUP BY v.id_venta, v.fecha_venta, cliente, v.total_venta
        ORDER BY v.fecha_venta DESC
    ''')

    ventas = cursor.fetchall()

    print("\nHistorial de Ventas:")
    print("-" * 60)
    if ventas:
        for venta in ventas:
            print(f"ID Venta: {venta[0]}")
            print(f"Fecha: {venta[1]}")
            print(f"Cliente: {venta[2]}")
            print(f"Productos: {venta[3]}")
            print(f"Total: ${venta[4]:.2f}")
            print("-" * 60)
    else:
        print("No hay ventas registradas.")
        print("-" * 60)
    conn.close()
#FUNCIÓN PARA BUSCAR VENTA
def buscar_venta():  
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    print("\n¿Cómo desea buscar la venta?")
    print("1. Buscar por ID de venta")
    print("2. Buscar por correo electrónico del cliente")

    opcion = int(input("Ingrese su opción (1 o 2): ")).strip()

    if opcion == 1:
        id_venta = input("Ingrese el ID de la venta: ").strip()

        query = '''
        SELECT 
            v.id_venta,
            v.fecha_venta,
            GROUP_CONCAT(p.nombre_producto) AS productos,
            v.total_venta
        FROM venta v
        JOIN venta_cliente vc ON v.id_venta = vc.id_venta
        JOIN cliente c ON vc.id_cliente = c.id_cliente
        JOIN producto_venta pv ON v.id_venta = pv.id_venta
        JOIN producto p ON pv.id_producto = p.id_producto
        WHERE v.id_venta = ?
        GROUP BY v.id_venta, v.fecha_venta, v.total_venta
        '''
        cursor.execute(query, (id_venta,))

    elif opcion == 2:
        email_cliente = input("Ingrese el correo electrónico del cliente: ").strip()

        query = '''
        SELECT 
            v.id_venta,
            v.fecha_venta,
            GROUP_CONCAT(p.nombre_producto) AS productos,
            v.total_venta
        FROM venta v
        JOIN venta_cliente vc ON v.id_venta = vc.id_venta
        JOIN cliente c ON vc.id_cliente = c.id_cliente
        JOIN producto_venta pv ON v.id_venta = pv.id_venta
        JOIN producto p ON pv.id_producto = p.id_producto
        WHERE c.email_cliente = ?
        GROUP BY v.id_venta, v.fecha_venta, v.total_venta
        '''
        cursor.execute(query, (email_cliente,))
    else:
        print("Opción no válida.")
        conn.close()
        return

    ventas = cursor.fetchall()
    conn.close()

    if ventas:
        print("\nVentas encontradas:")
        print("-" * 60)
        for idx, venta in enumerate(ventas, start=1):
            print(f"Venta #{idx}")
            print(f"ID Venta: {venta[0]}")
            print(f"Fecha: {venta[1]}")
            print(f"Productos: {venta[2]}")
            print(f"Total: ${venta[3]:.2f}")
            print("-" * 60)
    else:
        print("No se encontraron ventas con el criterio seleccionado.")
def modificar_venta():
    import sqlite3  # Importación de sqlite3 dentro de la función

    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    id_venta = input("Ingrese el ID de la venta que desea modificar: ").strip()
    cursor.execute('''SELECT id_venta FROM venta WHERE id_venta = ?''', (id_venta,))
    venta = cursor.fetchone()

    if venta:
        print(f"\nVenta encontrada con ID {id_venta}.")
        print("Seleccione qué desea modificar:")
        print("1. Modificar productos")
        print("2. Modificar cliente asociado")
        print("3. Modificar fecha de la venta")
        opcion = input("Ingrese su opción (1, 2 o 3): ").strip()

        if opcion == "1":
            # Mostrar productos actuales
            cursor.execute('''
                SELECT p.id_producto, p.nombre_producto
                FROM producto_venta pv
                JOIN producto p ON pv.id_producto = p.id_producto
                WHERE pv.id_venta = ?
            ''', (id_venta,))
            productos = cursor.fetchall()

            print("\nProductos actuales en la venta:")
            for producto in productos:
                print(f"ID Producto: {producto[0]}, Nombre: {producto[1]}")

            # Solicitar nuevo producto o actualizar cantidades
            id_producto = input("Ingrese el ID del producto que desea modificar o agregar: ").strip()

            cursor.execute('''
                SELECT id_producto FROM producto WHERE id_producto = ?
            ''', (id_producto,))
            producto = cursor.fetchone()

            if producto:
                # Actualizar producto en la venta
                cursor.execute('''
                    SELECT * FROM producto_venta
                    WHERE id_venta = ? AND id_producto = ?
                ''', (id_venta, id_producto))
                producto_venta = cursor.fetchone()

                if producto_venta:
                    print("Este producto ya está asociado a la venta. No es necesario agregarlo nuevamente.")
                else:
                    cursor.execute('''
                        INSERT INTO producto_venta (id_venta, id_producto)
                        VALUES (?, ?)
                    ''', (id_venta, id_producto))
                    conn.commit()
                    print("El producto ha sido agregado a la venta.")
            else:
                print("El producto ingresado no existe.")

        elif opcion == "2":
            # Modificar cliente asociado
            nuevo_email = input("Ingrese el correo electrónico del nuevo cliente: ").strip()

            cursor.execute("SELECT id_cliente FROM cliente WHERE email_cliente = ?", (nuevo_email,))
            cliente = cursor.fetchone()

            if cliente:
                cursor.execute('''
                    UPDATE venta_cliente
                    SET id_cliente = ?
                    WHERE id_venta = ?
                ''', (cliente[0], id_venta))
                conn.commit()
                print("El cliente asociado a la venta ha sido actualizado.")
            else:
                print("No se encontró ningún cliente con el correo proporcionado.")

        elif opcion == "3":
            # Modificar fecha de la venta
            nueva_fecha = input("Ingrese la nueva fecha de la venta (YYYY-MM-DD): ").strip()
            cursor.execute('''
                UPDATE venta
                SET fecha_venta = ?
                WHERE id_venta = ?
            ''', (nueva_fecha, id_venta))
            conn.commit()
            print("La fecha de la venta ha sido actualizada.")
        else:
            print("Opción no válida.")
    else:
        print(f"No se encontró ninguna venta con el ID {id_venta}.")

    conn.close()
        
        

