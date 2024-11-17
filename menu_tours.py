import sqlite3
def obtener_tour_clientes_valoraciones():
    fecha_especifica = input("Ingrese la fecha específica (DD/MM/YYYY): ").strip()
    
    query = """
    SELECT 
        t.nombre_tour,
        c.nombre_cliente || ' ' || c.apellido_cliente AS nombre_completo,
        t.fecha_tour,
        v.opinion
    FROM tour t
    LEFT JOIN reserva_tour rt ON t.id_tour = rt.id_tour
    LEFT JOIN detalle_reserva dr ON rt.id_reserva = dr.id_reserva
    LEFT JOIN cliente c ON dr.id_cliente = c.id_cliente
    LEFT JOIN valoracion_tour vt ON vt.id_tour = t.id_tour
    LEFT JOIN valoracion v ON vt.id_valoracion = v.id_valoracion
    WHERE t.fecha_tour = ?;
    """
    
    with sqlite3.connect("vinas_1.db") as conn:
        cursor = conn.cursor()
        cursor.execute(query, (fecha_especifica,))
        resultados = cursor.fetchall()
    
    if not resultados:
        print(f"No se encontraron tours para la fecha {fecha_especifica}.")
    else:
        return resultados
    
def menu_tours():

    Flag = True
    while Flag == True:
        
        print("\nMenú Tour")
        print("-"*30)
        print("1. Tours y valoraciones en un día especifico.")
        print("6. Salir")
        print("-"*30)

        try:
            opcion = int(input("Seleccione una opción: "))

            if opcion == 1:
                resultados = obtener_tour_clientes_valoraciones()
                if resultados:
                    for fila in resultados:
                        print(f"Tour: {fila[0]}, Cliente: {fila[1]}, Fecha: {fila[2]}, Valoración: {fila[3]}")
                    
            elif opcion == 6:
                Flag = False
            else:
                print("Opción no válida, intentelo de nuevo.")

        except ValueError:
            print ("Por favor ingrese un número entero valido.")
