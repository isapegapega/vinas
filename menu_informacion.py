import sqlite3
import matplotlib.pyplot as plt

def menu_informacion():

    Flag = True
    while Flag == True:
         
        print("\n--- Menú de Información ---")
        print("1. Ver ganancias entre dos años")
        print("2. Ver ganancias del último año superiores al promedio")
        print("3. Ventas de productos en las distintas viñas")
        print("4. Clientes por viña (gráfico de sectores)")
        print("5. Ganancias por categoría (gráfico de barras)")
        print("6. Reservas de tours por mes (gráfico de líneas)")
        print("7. Salir")
        print("-"*30)
        try:
            opcion = int(input("Seleccione una opción: "))
            if opcion == 1:
                año_inicio, año_fin = ingresar_años_validos()
                resultados = obtener_ganancias_entre_años(año_inicio, año_fin)
                if resultados:
                    print(f"Ganancias entre {año_inicio} y {año_fin}:")
                    for año, total_ventas in resultados:
                        print(f"Año: {año}, Ganancias: ${total_ventas}")
            elif opcion == 2:
                año = ingresar_año_valido()
                resultados = obtener_ganancias_ultimo_año(año)
                if resultados:
                    print(f"\nVentas con ganancias superiores al promedio en el año {año}:")
                    for id_venta, total_venta in resultados:
                        print(f"ID de Venta: {id_venta}, Ganancia Total: ${total_venta:.2f}")
                else:
                    print(f"No se encontraron ventas con ganancias superiores al promedio en el año {año}.")
            elif opcion == 3:
                resultados = ventas_productos_por_vina()
                if resultados:
                    print("\nVentas de productos en las distintas viñas:")
                    for nombre_vina, nombre_producto, total_ventas in resultados:
                        print(f"Viña: {nombre_vina}, Producto: {nombre_producto}, Total Ventas: ${total_ventas:.2f}")
                else:
                    print("No se encontraron ventas de productos en las distintas viñas.")
            elif opcion == 4:
                año = input("Ingrese el año (YYYY): ")
                grafico_clientes_por_vina(año)
            elif opcion == 5:
                grafico_ganancias_por_categoria()
            elif opcion == 6:
                año = input("Ingrese el año (YYYY): ")
                grafico_reservas_por_mes(año)
            elif opcion == 7:
                print("Saliendo del menú...")
                break
            else:
                print("Opción inválida. Intente nuevamente.")
        except ValueError:
            print("Por favor, ingrese un número válido.")
        
def ingresar_años_validos():
    while True:
        try:
            año_inicio = int(input("Año de inicio: ").strip())
            año_fin = int(input("Año de fin: ").strip())
            if año_inicio > año_fin:
                print("El año de inicio no puede ser mayor que el año de fin. Intente de nuevo.")
                continue
            return str(año_inicio), str(año_fin)
        except ValueError:
            print("Por favor, ingrese un número válido para el año.")
def obtener_ganancias_entre_años(año_inicio, año_fin):
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute('''
        SELECT substr(v.fecha_venta, 7, 4) AS año,
               SUM(dv.precio_final) AS total_ventas
        FROM venta v
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        WHERE substr(v.fecha_venta, 7, 4) BETWEEN ? AND ?
        GROUP BY año;
    ''', (año_inicio, año_fin))

    resultados = cursor.fetchall()
    conn.close()

    return resultados
def ingresar_año_valido():
    while True:
        try:
            año = input("Ingrese el año que desea consultar: ").strip()
            if not año.isdigit() or len(año) != 4:
                print("Por favor, ingrese un año válido de 4 dígitos.")
                continue
            return año
        except ValueError:
            print("Por favor, ingrese un número válido.")

def obtener_ganancias_ultimo_año(año):

    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()

    cursor.execute("""
        SELECT v.id_venta, SUM(dv.precio_final) AS total_venta
        FROM venta v
        JOIN detalle_venta dv ON v.id_venta = dv.id_venta
        WHERE substr(v.fecha_venta, 7, 4) = ?
        GROUP BY v.id_venta
    """, (año,))
    todas_las_ventas = cursor.fetchall()

    
    valores_totales = [venta[1] for venta in todas_las_ventas]
    if not valores_totales:
        cursor.close()
        return []  

    promedio = sum(valores_totales) / len(valores_totales)

    
    ventas_mayores = [(id_venta, total) for id_venta, total in todas_las_ventas if total > promedio]

    cursor.close()
    return ventas_mayores
def ventas_productos_por_vina():

    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()
    
    cursor.execute("""
        SELECT v.nombre_vina, p.nombre_producto, SUM(dv.precio_final) AS total_ventas
        FROM venta vt
        JOIN detalle_venta dv ON vt.id_venta = dv.id_venta
        JOIN producto p ON dv.id_producto = p.id_producto
        JOIN vina_producto vp ON p.id_producto = vp.id_producto
        JOIN vina v ON vp.id_vina = v.id_vina
        GROUP BY v.nombre_vina, p.nombre_producto
        ORDER BY v.nombre_vina, total_ventas DESC
    """)
    resultados = cursor.fetchall()
    cursor.close()

    return resultados

def grafico_clientes_por_vina(año):
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT v.nombre_vina, COUNT(DISTINCT r.id_reserva) AS total_reservas
        FROM reserva r
        JOIN detalle_reserva dr ON r.id_reserva = dr.id_reserva
        JOIN detalle_venta dv ON dr.id_reserva = dv.id_venta
        JOIN producto p ON dv.id_producto = p.id_producto
        JOIN vina_producto vp ON p.id_producto = vp.id_producto
        JOIN vina v ON vp.id_vina = v.id_vina
        WHERE substr(r.fecha_reserva, 7, 4) = ?
        GROUP BY v.nombre_vina
        ORDER BY total_reservas DESC;
    """, (año,))
    data = cursor.fetchall()
    cursor.close()

    if not data:
        print(f"No se encontraron reservas asociadas a viñas para el año {año}.")
        return

    nombres_vinas = [row[0] for row in data]
    total_reservas = [row[1] for row in data]

    plt.figure(figsize=(8, 6))
    plt.pie(total_reservas, labels=nombres_vinas, autopct='%1.1f%%', startangle=90)
    plt.title(f"Viñas Chile: Distribución de reservas por viña en {año}")
    plt.axis('equal')
    plt.show()

def grafico_ganancias_por_categoria():
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT p.tipo_producto, SUM(dv.precio_final) AS total_ganancias
        FROM detalle_venta dv
        JOIN producto p ON dv.id_producto = p.id_producto
        GROUP BY p.tipo_producto
        ORDER BY total_ganancias DESC;
    """)
    data = cursor.fetchall()
    cursor.close()

    if not data:
        print("No se encontraron ganancias por categorías.")
        return

    categorias = [row[0] for row in data]
    ganancias = [row[1] for row in data]

    plt.figure(figsize=(10, 6))
    plt.bar(categorias, ganancias)
    plt.title("Ganancias por Tipo de Producto")
    plt.xlabel("Tipo de Producto")
    plt.ylabel("Ganancias (CLP)")
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
def grafico_reservas_por_mes(año):
    conn = sqlite3.connect('vinas_1.db')
    cursor = conn.cursor()
    cursor.execute("""
        SELECT CASE 
                 WHEN fecha_reserva LIKE '%/%' THEN substr(fecha_reserva, 4, 2)
                 WHEN fecha_reserva LIKE '%-%' THEN substr(fecha_reserva, 6, 2)
               END AS mes, 
               COUNT(id_reserva) AS total_reservas
        FROM reserva
        WHERE fecha_reserva LIKE ?
        GROUP BY mes
        ORDER BY mes ASC;
    """, (f'%{año}',))
    data = cursor.fetchall()
    cursor.close()

    if not data:
        print(f"No se encontraron reservas para el año {año}.")
        return

    # Filtrar y convertir los datos
    meses = [int(row[0]) for row in data if row[0] is not None]
    total_reservas = [row[1] for row in data if row[0] is not None]

    # Generar el gráfico
    plt.figure(figsize=(10, 6))
    plt.plot(meses, total_reservas, marker='o', linestyle='-', linewidth=2)
    plt.title(f"Reservas de Tours por Mes en {año}")
    plt.xlabel("Meses")
    plt.ylabel("Total Reservas")
    plt.xticks(range(1, 13), ['Ene', 'Feb', 'Mar', 'Abr', 'May', 'Jun', 'Jul', 'Ago', 'Sep', 'Oct', 'Nov', 'Dic'])
    plt.grid(True)
    plt.tight_layout()
    plt.show()