import sqlite3
from menu_principal import menu_principal
def menu_ventas():

    print("1. Agregar Venta")
    print("2. Eliminar Venta")
    print("3. Modificar Venta")
    print("4. Buscar Venta")
    print("5. Mostrar Ventas")
    print("6. Volver al menú principal")
    
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
                menu_principal()
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
                    insertar_cliente()
                elif opcion_cliente == 2:
                    buscar_cliente()
                else:
                    print("Opción Invalida")
            except ValueError:
                print ("Por favor ingrese un número entero valido.")
        realizar_compra(cliente)
    if opcion_de_venta == 2:
        menu_ventas()

#FUNCIONES PARA LA BUSQUEDA DE CLIENTE
def insertar_cliente():
        print("Ingrese los datos del cliente: ")
        nombre = input("Nombre: ")
        apellido = input("Apellido: ")
        email = input("Correo Electronico: ")
        telefono = input("Teléfono (sin +56 9): ")
        conn = sqlite3.connect('')
        cursor = conn.cursor()
        try:
            cursor.execute('''
                        INSERT INTO clientes (Nombre, Apellido, Email, Telefono)
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
    conn = sqlite3.connect('')
    cursor = conn.cursor()
    
    #BUSCAR CLIENTE
    cursor.execute('''SELECT * FROM clientes WHERE Email = ?
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

    conn = sqlite3.connect('')
    cursor = conn.cursor()

    cursor.execute('SELECT id_producto, nombre, precio, FROM producto')
    productos = cursor.fetchall()

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
        
        cantidad = int(input(f"Ingrese la cantidad de '{producto_seleccionado[1]}' que desea llevar: "))
        total = producto_seleccionado[2] * cantidad

        print("\nResumen de la compra:")
        print("-" * 30)
        print(f"Producto: {producto_seleccionado[1]}")
        print(f"Cantidad: {cantidad}")
        print(f"Precio unitario: ${producto_seleccionado[2]:.2f}")
        print(f"Total a pagar: ${total:.2f}")
        print("-" * 30)

        confirmacion = input("¿Desea confirmar la compra? (s/n): ").strip().lower()
        if confirmacion == 's':
            conn = sqlite3.connect('ventas.db')
            cursor = conn.cursor()

            cursor.execute('''
            INSERT INTO ventas (cliente_id, producto_nombre, cantidad, total)
            VALUES (?, ?, ?, ?)
            ''', (cliente['id'], producto_seleccionado[1], cantidad, total))

            conn.commit()
            conn.close()
            print("La compra fue realizada con exito, ¡Muchas gracias!")
        else:
            print("La compra ha sido cancelada")
    except ValueError:
        print("Error: Por favor ingrese un número válido.")
        

