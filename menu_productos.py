import sqlite3

#MENU PRINCIPAL PRODUCTO
def menu_productos():

    Flag = True
    while Flag == True:

        print("\nMenú Producto")
        print("-"*30)
        print("1. Agregar Producto")
        print("2. Eliminar Producto")
        print("3. Modificar producto")
        print("4. Busqueda de producto")
        print("5. Mostrar Stock")
        print("6. Salir")
        print("-"*30)

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                print("Ha sido seleccionado agregar producto")
                agregar_producto()
            elif opcion == 2:
                print("Ha sido seleccionado eliminar producto")
                eliminar_producto()
            elif opcion == 3:
                print("Ha sido seleccionado modificar producto")
                modificar_producto_general()
            elif opcion == 4:
                print("Ha sido seleccionado buscar producto")
                buscar_producto()
            elif opcion == 5:
                print("Ha sido seleccionado mostrar stock")
                mostrar_stock()
            elif opcion == 6:
                Flag = False
            else:
                print("Opción no válida, intentelo de nuevo.")

        except ValueError:
            print ("Por favor ingrese un número entero valido.")

#AGREAGR PRODUCTO
def agregar_producto():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    nombre_producto = input("Ingrese el nombre del producto: ").strip()
    precio_original = int(input("Ingrese el precio original del producto: "))
    tipo_producto = input("Ingrese el tipo de producto: ").strip()

    try:
        cursor.execute('''
            INSERT INTO producto (nombre_producto, precio_original, tipo_producto)
            VALUES (?, ?, ?)
        ''', (nombre_producto, precio_original, tipo_producto))
        conn.commit()
        print("Producto agregado exitosamente.")
        
    except Exception as e:
        print(f"Error al agregar producto: {e}")
    finally:
        conn.close()

#ELIMINAR PRODUCTOS
def eliminar_producto():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    id_producto = int(input("Ingrese el ID del producto que desea eliminar: ").strip())
    cursor.execute('''SELECT id_producto FROM producto WHERE id_producto = ?''', (id_producto,))
    producto = cursor.fetchone()
    if producto:
        confirmar_eliminacion = input(f"¿Seguro(a) que desea eliminar el producto con ID {id_producto}? (s/n): ").strip().lower()
        if confirmar_eliminacion == "s":
            try:
                cursor.execute('''DELETE FROM producto WHERE id_producto = ?''', (id_producto,))
                cursor.execute('''DELETE FROM producto_stock WHERE id_producto = '? ''',(id_producto))
                cursor.execute('''DELETE FORM vina_producto WHERE id_producto = ? ''', (id_producto))
                cursor.execute('''DELETE FROM descuento_producto WHERE id_producto = ? ''',(id_producto))
                conn.commit()
                print(f"El producto con ID {id_producto} ha sido eliminado exitosamente.")
            except Exception as e:
                print(f"Se produjo un error al eliminar el producto: {e}")
        else:
            print("La operación fue cancelada.")
    else:
        print(f"No se logró encontrar ningún producto con el ID {id_producto}.")
    conn.close()

#MOSTAR STOCK
def mostrar_stock():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT 
            p.id_producto,
            p.nombre_producto,
            p.precio_original,
            p.tipo_producto,
            s.n_disponible
        FROM producto p
        JOIN producto_stock ps ON p.id_producto = ps.id_producto
        JOIN stock s ON ps.id_stock = s.id_stock
    ''')

    productos = cursor.fetchall()
    conn.close()

    print("\nStock de productos:")
    if productos:
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: ${producto[2]}, Tipo: {producto[3]}, Stock Disponible: {producto[4]}")
    else:
        print("No hay productos en stock.")

#FUNCIÓN PARA BUSCAR VENTA
def buscar_producto():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()
    print("\n¿Cómo quiere buscar el producto?")
    print("1. Buscar por ID de producto")
    print("2. Buscar por nombre del producto")

    opcion = int(input("Ingrese la opción que desee (1 o 2): ").strip())

    if opcion == 1:
        id_producto = int(input("Ingrese el ID del producto: ").strip())
        cursor.execute('''SELECT * FROM producto WHERE id_producto = ?''', (id_producto,))
    elif opcion == 2:
        nombre_producto = input("Ingrese el nombre del producto: ").strip()
        cursor.execute('''SELECT * FROM producto WHERE nombre_producto LIKE ?''', (f"%{nombre_producto}%",))
    else:
        print("La opción no es valida.")
        conn.close()
        return
    productos = cursor.fetchall()
    conn.close()

    if productos:
        print("\nProductos encontrados:")
        for producto in productos:
            print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: {producto[2]}, Tipo: {producto[3]}")
        
    else:
        print("No se encontraron productos con el criterio seleccionado.")

#MODIFICAR PRODUCTO    
def modificar_producto_general():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    id_producto = int(input("Ingrese el ID del producto que desea modificar: ").strip())
    cursor.execute('''SELECT * FROM producto WHERE id_producto = ?''', (id_producto,))
    producto = cursor.fetchone()

    if producto:
        print("\nProducto actual:")
        print(f"ID: {producto[0]}, Nombre: {producto[1]}, Precio: ${producto[2]}, Tipo: {producto[3]}")
        print("\n¿Qué desea modificar?")
        print("1. Datos del producto (nombre, precio, tipo)")
        print("2. Stock del producto")
        print("3. Viña asociada al producto")
        print("4. Cancelar")
        opcion = int(input("Seleccione una opción (1-4): ").strip())

        if opcion == 1:  # Modificar datos del producto
            nuevo_nombre = input("Ingrese el nuevo nombre (dejar vacío para no modificar): ").strip()
            nuevo_precio = input("Ingrese el nuevo precio (dejar vacío para no modificar): ").strip()
            nuevo_tipo = input("Ingrese el nuevo tipo de producto (dejar vacío para no modificar): ").strip()

            try:
                if nuevo_nombre:
                    cursor.execute('UPDATE producto SET nombre_producto = ? WHERE id_producto = ?', (nuevo_nombre, id_producto))
                if nuevo_precio:
                    cursor.execute('UPDATE producto SET precio_original = ? WHERE id_producto = ?', (int(nuevo_precio), id_producto))
                if nuevo_tipo:
                    cursor.execute('UPDATE producto SET tipo_producto = ? WHERE id_producto = ?', (nuevo_tipo, id_producto))
                conn.commit()
                print("Datos del producto modificados exitosamente.")
            except Exception as e:
                print(f"Error al modificar los datos del producto: {e}")

        elif opcion == 2:  # Modificar stock del producto
            cursor.execute('''
                SELECT s.id_stock, s.n_disponible
                FROM stock s
                JOIN producto_stock ps ON s.id_stock = ps.id_stock
                WHERE ps.id_producto = ?
            ''', (id_producto,))
            stock_actual = cursor.fetchone()

            if stock_actual:
                print(f"Stock actual: {stock_actual[1]}")
                nuevo_stock = int(input("Ingrese la nueva cantidad de stock: ").strip())
                try:
                    cursor.execute('UPDATE stock SET n_disponible = ? WHERE id_stock = ?', (nuevo_stock, stock_actual[0]))
                    conn.commit()
                    print("Stock modificado exitosamente.")
                except Exception as e:
                    print(f"Error al modificar el stock: {e}")
            else:
                print("El producto no tiene stock registrado.")

        elif opcion == 3:  # Modificar viña asociada al producto
            cursor.execute('''
                SELECT v.id_vina, v.nombre_vina
                FROM vina v
                JOIN vina_producto vp ON v.id_vina = vp.id_vina
                WHERE vp.id_producto = ?
            ''', (id_producto,))
            vina_actual = cursor.fetchone()

            if vina_actual:
                print(f"Viña actual: {vina_actual[1]} (ID: {vina_actual[0]})")
                nueva_vina = int(input("Ingrese el ID de la nueva viña: ").strip())
                try:
                    cursor.execute('UPDATE vina_producto SET id_vina = ? WHERE id_producto = ?', (nueva_vina, id_producto))
                    conn.commit()
                    print("Viña asociada modificada exitosamente.")
                except Exception as e:
                    print(f"Error al modificar la viña asociada: {e}")
            else:
                print("El producto no está asociado a ninguna viña actualmente.")

        elif opcion == 4:  # Cancelar
            print("Modificación cancelada.")

        else:
            print("Opción no válida.")
    else:
        print(f"No se encontró ningún producto con el ID {id_producto}.")

    conn.close()
    