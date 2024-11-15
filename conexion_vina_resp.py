import sqlite3

conexion = sqlite3.connect('vinas_1.db')
cursor = conexion.cursor()

#A CONTINUACION TODAS LAS ENTIDADES FUERTES(no tienen llaves foranea)

def crear_tablas_fuertes():
        #region
    cursor.execute('''CREATE TABLE IF NOT EXISTS region (
        `id_region` INTEGER NOT NULL UNIQUE,
        `nombre_region` TEXT NOT NULL UNIQUE,
        PRIMARY KEY(`id_region` AUTOINCREMENT)
    )''')
        #ubicacion
    cursor.execute('''CREATE TABLE IF NOT EXISTS ubicacion (
        `id_ubicacion` INTEGER NOT NULL UNIQUE,
        `direccion` TEXT NOT NULL,
        PRIMARY KEY(`id_ubicacion` AUTOINCREMENT)
    )''')
        #vina
    cursor.execute('''CREATE TABLE IF NOT EXISTS vina (
        `id_vina` INTEGER NOT NULL UNIQUE,
        `nombre_vina` TEXT NOT NULL,
        PRIMARY KEY (`id_vina` AUTOINCREMENT)
    )''')
        #tour
    cursor.execute('''CREATE TABLE IF NOT EXISTS tour (
        `id_tour` INTEGER NOT NULL UNIQUE,
        `nombre_tour` TEXT NOT NULL UNIQUE,
        `fecha_tour` TEXT NOT NULL,
        `tipo_tour` TEXT NOT NULL,
        PRIMARY KEY ( `id_tour` AUTOINCREMENT)
    )''')
        #producto
    cursor.execute('''CREATE TABLE IF NOT EXISTS producto (
        `id_producto` INTEGER NOT NULL UNIQUE,
        `nombre_producto` TEXT NOT NULL,
        `precio_original` INTEGER NOT NULL,
        `tipo_producto` TEXT NOT NULL,
        PRIMARY KEY ( `id_producto` AUTOINCREMENT)
    )''')
        #descuento
    cursor.execute('''CREATE TABLE IF NOT EXISTS descuento (
        `id_descuento` INTEGER NOT NULL UNIQUE,
        `cantidad_descuento` INTEGER NOT NULL,
        PRIMARY KEY ( `id_descuento` AUTOINCREMENT)
    )''')
        #stock
    cursor.execute('''CREATE TABLE IF NOT EXISTS stock (
        `id_stock` INTEGER NOT NULL UNIQUE,
        `n_disponible` INTEGER NOT NULL,
        PRIMARY KEY (`id_stock` AUTOINCREMENT)
    )''')
        #cliente
    cursor.execute('''CREATE TABLE IF NOT EXISTS cliente (
                   `id_cliente` INTEGER NOT NULL UNIQUE,
                   `nombre_cliente` TEXT NOT NULL,
                   `apellido_cliente` TEXT NOT NULL,
                   `email_cliente` TEXT NOT NULL,
                   `telefono_cliente` INTEGER NOT NULL,
                   PRIMARY KEY (`id_cliente` AUTOINCREMENT))''')

    conexion.commit()
    print('Tablas creadas exitosamente')
crear_tablas_fuertes()

def insert_tabas_fuertes():
    cursor.execute('''INSERT INTO region (id_region,nombre_region)
                   VALUES (1,'Arica y Parinacota'),(2,'Tarapaca'),(3,'Antofagasta'),(4,'Atacama'),(5,'Coquimbo'),(6,'Valparaiso'),(7,'Metropolitana'),(8,'Ohiggins'),(9,'Maule'),(10,'Ñuble'),(11,'Bio Bio'),(12,'Araucania'),(13,'Los Rios'),(14,'Los lagos'),(15,'Aysen'),(16,'Magallanes') 
            ''')

    cursor.execute('''INSERT INTO ubicacion (id_ubicacion, direccion)
                   VALUES (1, 'Calle Independencia 342, Talca, Región del Maule (7ma)'),  
                          (2, 'Pasaje Los Naranjos 128, Rancagua, Región de OHiggins (6ta)'),  
                          (3, 'Avenida España 4567, Chillán, Región de Ñuble (8va)'),  
                          (4, 'Calle Baquedano 234, San Fernando, Región de OHiggins (6ta)'),  
                          (5, 'Pasaje Las Araucarias 78, Curicó, Región del Maule (7ma)'),  
                          (6, 'Avenida Prat 567, Concepción, Región del Biobío (8va)'),  
                          (7, 'Calle San Martín 912, Linares, Región del Maule (7ma)'),  
                          (8, 'Avenida Bernardo OHiggins 1430, Los Ángeles, Región del Biobío (8va)'),  
                          (9, 'Pasaje Los Olivos 231, San Vicente, Región de OHiggins (6ta)'),  
                          (10, 'Calle Arturo Prat 302, Cauquenes, Región del Maule (7ma)'),  
                          (11, 'Avenida Libertad 1001, Chillán Viejo, Región de Ñuble (8va)'),  
                          (12, 'Calle Los Aromos 120, Talagante, Región Metropolitana'),  
                          (13, 'Pasaje El Roble 78, Quillota, Región de Valparaíso (5ta)'),  
                          (14, 'Avenida Las Palmeras 200, Viña del Mar, Región de Valparaíso (5ta)'),  
                          (15, 'Calle José Miguel Carrera 302, Rengo, Región de OHiggins (6ta)'),  
                          (16, 'Avenida Las Camelias 540, San Javier, Región del Maule (7ma)'),  
                          (17, 'Pasaje Los Aromos 34, Coronel, Región del Biobío (8va)'),  
                          (18, 'Avenida Libertador 780, Lota, Región del Biobío (8va)'),  
                          (19, 'Calle Santa María 56, Melipilla, Región Metropolitana'),  
                          (20, 'Pasaje Manuel Rodríguez 142, San Antonio, Región de Valparaíso (5ta)')
    ''')

    cursor.execute('''INSERT INTO vina (id_vina, nombre_vina)
                VALUES (1, 'Viña Concha y Toro'), (2, 'Viña Santa Rita'), (3, 'Viña Montes'),
                       (4, 'Viña Casa Silva'), (5, 'Viña Undurraga'), (6, 'Viña Lapostolle'),
                       (7, 'Viña Emiliana'), (8, 'Viña Errazuriz'), (9, 'Viña San Pedro'),
                       (10, 'Viña Santa Carolina'), (11, 'Viña Ventisquero'), (12, 'Viña Tarapacá'),
                       (13, 'Viña Morandé'), (14, 'Viña Santa Ema'), (15, 'Viña Carmen'),
                       (16, 'Viña Koyle'), (17, 'Viña Viu Manent'), (18, 'Viña Los Vascos'),
                       (19, 'Viña Cono Sur'), (20, 'Viña El Principal')
    ''')

    cursor.execute('''INSERT INTO tour (id_tour, nombre_tour, fecha_tour, tipo_tour)
                   VALUES (1, 'Tour de Cata Clásico', '15/11/2024', 'Cata de Vinos'),
                          (2, 'Recorrido en Viñedo Premium', '16/11/2024', 'Recorrido en Viñedo'),
                          (3, 'Tour Historia y Tradición', '17/11/2024', 'Cultural'),
                          (4, 'Degustación Reserva', '18/11/2024', 'Degustación'),
                          (5, 'Tour Nocturno en Viña', '19/11/2024', 'Experiencia Nocturna'),
                          (6, 'Cata de Vinos Espumantes', '20/11/2024', 'Cata de Vinos'),
                          (7, 'Recorrido Valle de Colchagua', '21/11/2024', 'Recorrido en Viñedo'),
                          (8, 'Tour Enólogo por un Día', '22/11/2024', 'Experiencia Especial'),
                          (9, 'Picnic en el Viñedo', '23/11/2024', 'Experiencia al Aire Libre'),
                          (10, 'Tour de Vendimia', '24/11/2024', 'Cultural'),
                          (11, 'Experiencia Sensorial', '25/11/2024', 'Degustación'),
                          (12, 'Paseo Fotográfico en Viñedo', '26/11/2024', 'Recorrido en Viñedo'),
                          (13, 'Degustación de Gran Reserva', '27/11/2024', 'Cata de Vinos'),
                          (14, 'Paseo a Caballo entre Viñedos', '28/11/2024', 'Experiencia al Aire Libre'),
                          (15, 'Recorrido en Bodega y Cava', '29/11/2024', 'Cultural'),
                          (16, 'Maridaje de Vinos y Chocolates', '30/11/2024', 'Degustación'),
                          (17, 'Tour Premium Valle del Maipo', '01/12/2024', 'Recorrido en Viñedo'),
                          (18, 'Experiencia de Vinos Orgánicos', '02/12/2024', 'Cata de Vinos'),
                          (19, 'Cena en el Viñedo', '03/12/2024', 'Experiencia Nocturna'),
                          (20, 'Clase de Enología Básica', '04/12/2024', 'Experiencia Especial')
    ''')

    cursor.execute('''INSERT INTO producto (id_producto, nombre_producto, precio_original, tipo_producto)
                    VALUES (1, 'Vino Tinto Cabernet Sauvignon Reserva', 8500, 'Vino Tinto'),
                           (2, 'Vino Blanco Sauvignon Blanc Premium', 7500, 'Vino Blanco'),
                           (3, 'Vino Tinto Carmenere Gran Reserva', 12000, 'Vino Tinto'),
                           (4, 'Vino Rosé Valle Central', 6500, 'Vino Rosado'),
                           (5, 'Vino Tinto Merlot Reserva', 7000, 'Vino Tinto'),
                           (6, 'Vino Blanco Chardonnay Reserva', 9000, 'Vino Blanco'),
                           (7, 'Vino Tinto Syrah Valle del Maipo', 9500, 'Vino Tinto'),
                           (8, 'Vino Blanco Viognier Reserva', 8500, 'Vino Blanco'),
                           (9, 'Gran Carménère Valle de Colchagua', 14000, 'Vino Tinto'),
                           (10, 'Late Harvest Dulce', 10500, 'Vino Dulce'),
                           (11, 'Espumante Brut Nature', 13000, 'Espumante'),
                           (12, 'Vino Tinto Pinot Noir Reserva', 11000, 'Vino Tinto'),
                           (13, 'Pack Degustación Tintos', 25000, 'Pack Degustación'),
                           (14, 'Aceite de Oliva Extra Virgen del Maule', 6000, 'Otros'),
                           (15, 'Vinagre Balsámico del Valle del Itata', 4500, 'Otros'),
                           (16, 'Blend del Enólogo Colchagua', 15000, 'Vino Tinto'),
                           (17, 'Espumante Rosé', 13500, 'Espumante'),
                           (18, 'Gran Reserva Chardonnay Valle de Limarí', 12500, 'Vino Blanco'),
                           (19, 'Sauvignon Gris', 9500, 'Vino Blanco'),
                           (20, 'Pack Premium', 45000, 'Pack Degustación')
    ''')

    cursor.execute('''INSERT INTO descuento (id_descuento, cantidad_descuento)
                    VALUES (1, 0.05),
                           (2, 0.1),
                           (3, 0.15),
                           (4, 0.2),
                           (5, 0.25),
                           (6, 0.3),
                           (7, 0.35),
                           (8, 0.4),
                           (9, 0.45),
                           (10, 0.5),
                           (11, 0.08),
                           (12, 0.6),
                           (13, 0.04),
                           (14, 0.18),
                           (15, 0.22),
                           (16, 0.3),
                           (17, 0.55),
                           (18, 0.65),
                           (19, 0.06),
                           (20, 0.32)''')
    cursor.execute(''' INSERT INTO stock (id_stock,n_disponible)
                   VALUES (1, 50),
                          (2, 30),
                          (3, 75),
                          (4, 20),
                          (5, 60),
                          (6, 45),
                          (7, 80),
                          (8, 25),
                          (9, 100),
                          (10, 15),
                          (11, 40),
                          (12, 90),
                          (13, 35),
                          (14, 55),
                          (15, 70),
                          (16, 65),
                          (17, 85),
                          (18, 95),
                          (19, 10),
                          (20, 120)''')
    
    cursor.execute('''INSERT INTO cliente (id_cliente,nombre_cliente,apellido_cliente,email_cliente,telefono_cliente)
                   VALUES (1, 'María', 'González', 'maria.gonzalez@email.com', 912345678),
                   (2, 'Juan', 'Pérez', 'juan.perez@email.com', 987654321),
                   (3, 'Carolina', 'López', 'carolina.lopez@email.com', 923456789),
                   (4, 'Pedro', 'Morales', 'pedro.morales@email.com', 987651234),
                   (5, 'Francisca', 'Rodríguez', 'francisca.rodri@email.com', 956781234),
                   (6, 'Andrés', 'Soto', 'andres.soto@email.com', 943215678),
                   (7, 'Valentina', 'Rojas', 'valentina.rojas@email.com', 912348765),
                   (8, 'Felipe', 'Espinoza', 'felipe.espinoza@email.com', 934567812),
                   (9, 'Daniela', 'Martínez', 'daniela.martinez@email.com', 987634567),
                   (10, 'Alejandro', 'Fuentes', 'alejandro.fuentes@email.com', 923451678),
                   (11, 'Camila', 'Herrera', 'camila.herrera@email.com', 998765432),
                   (12, 'Ignacio', 'Pizarro', 'ignacio.pizarro@email.com', 965432198),
                   (13, 'Josefina', 'Torres', 'josefina.torres@email.com', 932165487),
                   (14, 'Cristóbal', 'Gutiérrez', 'cristobal.gutierrez@email.com', 923456782),
                   (15, 'Sofía', 'Castro', 'sofia.castro@email.com', 934561278),
                   (16, 'Nicolás', 'Vásquez', 'nicolas.vasquez@email.com', 976543219),
                   (17, 'Antonia', 'Díaz', 'antonia.diaz@email.com', 981234567),
                   (18, 'Sebastián', 'Ramírez', 'sebastian.ramirez@email.com', 943218765),
                   (19, 'Catalina', 'Salazar', 'catalina.salazar@email.com', 987654329),
                   (20, 'Tomás', 'Carrasco',  'tomas.carrasco@email.com', 965437812)''')
    
    print('datos insertados correctamente')
    conexion.commit()
insert_tabas_fuertes()

#______________________________________________________________________
#A CONTINUACION TODAS LAS ENTIDADES DEBILES
def crear_tablas_debiles():
    # Tabla "venta"
    cursor.execute('''CREATE TABLE IF NOT EXISTS venta (
                   `id_venta` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT, 
                   `fecha_venta` TEXT NOT NULL,
                   `total_venta` INTEGER NOT NULL,
                   `id_descuento` INTEGER NOT NULL,
                   FOREIGN KEY(`id_descuento`) REFERENCES descuento(`id_descuento`)
                   )''')

    # Tabla "precio_total"
    cursor.execute('''CREATE TABLE IF NOT EXISTS precio_total (
                   `id_precio_total` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                   `n_personas` INTEGER NOT NULL,
                   `precio_unitario` INTEGER NOT NULL)''')

    # Tabla "valoracion"
    cursor.execute('''CREATE TABLE IF NOT EXISTS valoracion (
                   `id_valoracion` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                   `fecha_valoracion` TEXT NOT NULL,
                   `opinion` TEXT NOT NULL)''')

    # Tabla "detalle_venta"
    cursor.execute('''CREATE TABLE IF NOT EXISTS detalle_venta (
                   `id_detalle_venta` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                   `id_venta` INTEGER NOT NULL,
                   `id_producto` INTEGER NOT NULL,
                   `precio_final` INTEGER NOT NULL,
                   FOREIGN KEY(`id_venta`) REFERENCES venta(`id_venta`),
                   FOREIGN KEY(`id_producto`) REFERENCES producto(`id_producto`))''')

    # Tabla "reserva"
    cursor.execute('''CREATE TABLE IF NOT EXISTS reserva (
                   `id_reserva` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                   `id_cliente` INTEGER NOT NULL,
                   `fecha_reserva` TEXT NOT NULL,
                   `precio_original` INTEGER NOT NULL,
                   `estado_reserva` TEXT NOT NULL,
                   FOREIGN KEY(`id_cliente`) REFERENCES cliente(`id_cliente`))''')

    # Tabla "acompanante"
    cursor.execute('''CREATE TABLE IF NOT EXISTS acompanante (
                   `id_acompanante` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                   `nombre_acompanante` TEXT NOT NULL,
                   `apellido_acompanante` TEXT NOT NULL,
                   `relacion_con_comprador` TEXT NOT NULL)''')

    # Tabla "detalle_reserva"
    cursor.execute('''CREATE TABLE IF NOT EXISTS detalle_reserva (
                   `id_detalle_reserva` INTEGER NOT NULL UNIQUE PRIMARY KEY AUTOINCREMENT,
                   `id_reserva` INTEGER NOT NULL,
                   `id_cliente` INTEGER NOT NULL, 
                   FOREIGN KEY(`id_reserva`) REFERENCES reserva(`id_reserva`),
                   FOREIGN KEY(`id_cliente`) REFERENCES cliente(`id_cliente`))''')

    # Confirmar los cambios en la base de datos
    conexion.commit()
# Llamar a la función
crear_tablas_debiles()

def insert_tablas_debiles():
            # Inserción en la tabla 'venta'
    cursor.execute('''INSERT INTO venta(id_venta,fecha_venta,total_venta,id_descuento)
                   VALUES (1, '15/01/2024', 150.00, 1),
                          (2, '20/02/2024', 200.00, 2),
                          (3, '10/03/2024', 120.00, 3),
                          (4, '05/04/2024', 180.00, 4),
                          (5, '12/05/2024', 210.00, 5),
                          (6, '18/06/2024', 250.00, 6),
                          (7, '22/07/2024', 160.00, 7),
                          (8, '30/08/2024', 220.00, 8),
                          (9, '04/09/2024', 190.00, 9),
                          (10, '17/10/2024', 170.00, 10),
                          (11, '09/11/2024', 160.00, 11),
                          (12, '14/12/2024', 200.00, 12),
                          (13, '23/01/2025', 180.00, 13),
                          (14, '11/02/2025', 150.00, 14),
                          (15, '16/03/2025', 210.00, 15),
                          (16, '03/04/2025', 220.00, 16),
                          (17, '07/05/2025', 230.00, 17),
                          (18, '21/06/2025', 240.00, 18),
                          (19, '10/07/2025', 260.00, 19),
                          (20, '15/08/2025', 280.00, 20)''')
        # Inserción en la tabla 'precio_total'
    cursor.execute('''INSERT INTO precio_total(id_precio_total,n_personas,precio_unitario)
                   VALUES (1, 4, 30.00),
                          (2, 2, 40.00),
                          (3, 6, 25.00),
                          (4, 5, 35.00),
                          (5, 3, 45.00),
                          (6, 7, 20.00),
                          (7, 8, 15.00),
                          (8, 10, 10.00),
                          (9, 2, 50.00),
                          (10, 4, 40.00),
                          (11, 6, 30.00),
                          (12, 3, 45.00),
                          (13, 5, 36.00),
                          (14, 4, 38.00),
                          (15, 7, 28.00),
                          (16, 2, 60.00),
                          (17, 8, 18.00),
                          (18, 9, 22.00),
                          (19, 6, 32.00),
                          (20, 3, 48.00)''')
        # Inserción en la tabla 'valoracion'
    cursor.execute('''INSERT INTO valoracion(id_valoracion,fecha_valoracion,opinion)
                   VALUES (1, '15/01/2024', 'Excelente experiencia, muy recomendada.'),
                          (2, '20/02/2024', 'El vino tiene un sabor único, volveremos pronto.'),
                          (3, '10/03/2024', 'Buen ambiente y vinos deliciosos.'),
                          (4, '05/04/2024', 'Una visita inolvidable, la cata fue maravillosa.'),
                          (5, '12/05/2024', 'Muy buena atención y el vino estaba espectacular.'),
                          (6, '18/06/2024', 'Una experiencia muy relajante, ideal para disfrutar.'),
                          (7, '22/07/2024', 'Los vinos son muy buenos, pero el tour fue corto.'),
                          (8, '30/08/2024', 'Excelente calidad en los productos y muy buena atención.'),
                          (9, '04/09/2024', 'Un lugar hermoso, la cata de vinos fue muy interesante.'),
                          (10, '17/10/2024', 'Maravillosa viña, excelente atención y deliciosos vinos.'),
                          (11, '09/11/2024', 'El ambiente es increíble, vinos con gran personalidad.'),
                          (12, '14/12/2024', 'Vinos de gran calidad, el lugar tiene mucha historia.'),
                          (13, '23/01/2025', 'Una experiencia muy enriquecedora, volveré sin duda.'),
                          (14, '11/02/2025', 'Una visita que vale la pena, muy buena relación calidad-precio.'),
                          (15, '16/03/2025', 'La mejor cata de vinos que he probado, 100% recomendable.'),
                          (16, '03/04/2025', 'Un lugar acogedor, perfectos para disfrutar de buenos vinos.'),
                          (17, '07/05/2025', 'Muy buen servicio y los vinos excepcionales.'),
                          (18, '21/06/2025', 'Un sitio perfecto para relajarse y disfrutar de un buen vino.'),
                          (19, '10/07/2025', 'Excelente, el vino es delicioso y el lugar hermoso.'),
                          (20, '15/08/2025', 'Un ambiente tranquilo y vinos que te hacen querer más.')''')
        # Inserción en la tabla 'detalle_venta'
    cursor.execute('''INSERT INTO detalle_venta(id_detalle_venta,id_venta,id_producto,precio_final)
                   VALUES (1, 1, 1, 8642.50),
                          (2, 2, 2, 7680.00),
                          (3, 3, 3, 12102.00),
                          (4, 4, 4, 6644.00),
                          (5, 5, 5, 7157.50),
                          (6, 6, 6, 9175.00),
                          (7, 7, 7, 9604.00),
                          (8, 8, 8, 8632.00),
                          (9, 9, 9, 14104.50),
                          (10, 10, 10, 10585.00),
                          (11, 11, 11, 13147.20),
                          (12, 12, 12, 11080.00),
                          (13, 13, 13, 25172.80),
                          (14, 14, 14, 6123.00),
                          (15, 15, 15, 4663.80),
                          (16, 16, 16, 15154.00),
                          (17, 17, 17, 13603.50),
                          (18, 18, 18, 12584.00),
                          (19, 19, 19, 9744.40),
                          (20, 20, 20, 45190.40)''')
        #para tabla 'reserva'
    cursor.execute('''INSERT INTO reserva(id_reserva,id_cliente,fecha_reserva,precio_original,estado_reserva)
               VALUES (1, 1, '15/01/2024', 8642.50, 'Confirmada'),
                      (2, 2, '20/02/2024', 7680.00, 'Cancelada'),
                      (3, 3, '10/03/2024', 12102.00, 'Confirmada'),
                      (4, 4, '05/04/2024', 6644.00, 'Pendiente'),
                      (5, 5, '12/05/2024', 7157.50, 'Confirmada'),
                      (6, 6, '18/06/2024', 9175.00, 'Cancelada'),
                      (7, 7, '22/07/2024', 9604.00, 'Confirmada'),
                      (8, 8, '30/08/2024', 8632.00, 'Pendiente'),
                      (9, 9, '04/09/2024', 14104.50, 'Confirmada'),
                      (10, 10, '17/10/2024', 10585.00, 'Cancelada'),
                      (11, 11, '09/11/2024', 13147.20, 'Pendiente'),
                      (12, 12, '14/12/2024', 11080.00, 'Confirmada'),
                      (13, 13, '23/01/2025', 25172.80, 'Pendiente'),
                      (14, 14, '11/02/2025', 6123.00, 'Confirmada'),
                      (15, 15, '16/03/2025', 4663.80, 'Cancelada'),
                      (16, 16, '03/04/2025', 15154.00, 'Pendiente'),
                      (17, 17, '07/05/2025', 13603.50, 'Confirmada'),
                      (18, 18, '21/06/2025', 12584.00, 'Cancelada'),
                      (19, 19, '10/07/2025', 9744.40, 'Confirmada'),
                      (20, 20, '15/08/2025', 45190.40, 'Pendiente') ''')

        #para tabla 'acompanante'
    cursor.execute('''INSERT INTO acompanante(id_acompanante,nombre_acompanante,apellido_acompanante,relacion_con_comprador)
               VALUES (1, 'Carlos', 'Pérez', 'Amigo'),
                      (2, 'María', 'González', 'Esposa'),
                      (3, 'Juan', 'López', 'Hermano'),
                      (4, 'Ana', 'Martínez', 'Compañera de trabajo'),
                      (5, 'Luis', 'Rodríguez', 'Amigo'),
                      (6, 'Elena', 'Sánchez', 'Madre'),
                      (7, 'Pedro', 'Ramírez', 'Padre'),
                      (8, 'Sofía', 'Torres', 'Novia'),
                      (9, 'Gabriel', 'Fernández', 'Colega'),
                      (10, 'Lucía', 'García', 'Hermana'),
                      (11, 'Miguel', 'Vásquez', 'Amigo'),
                      (12, 'Beatriz', 'Jiménez', 'Esposa'),
                      (13, 'Raúl', 'Castro', 'Primo'),
                      (14, 'Isabel', 'Delgado', 'Tía'),
                      (15, 'Ricardo', 'Hernández', 'Amigo'),
                      (16, 'Clara', 'Morales', 'Compañera de estudio'),
                      (17, 'José', 'Gil', 'Cuñado'),
                      (18, 'Carmen', 'Mendoza', 'Madre'),
                      (19, 'Antonio', 'Suárez', 'Amigo de la infancia'),
                      (20, 'Verónica', 'Reyes', 'Sobrina') ''')
        #para tabla 'detalle_reserva'
    cursor.execute('''INSERT INTO detalle_reserva(id_detalle_reserva,id_reserva,id_cliente)
               VALUES (1, 1, 1),
                      (2, 2, 2),
                      (3, 3, 3),
                      (4, 4, 4),
                      (5, 5, 5),
                      (6, 6, 6),
                      (7, 7, 7),
                      (8, 8, 8),
                      (9, 9, 9),
                      (10, 10, 10),
                      (11, 11, 11),
                      (12, 12, 12),
                      (13, 13, 13),
                      (14, 14, 14),
                      (15, 15, 15),
                      (16, 16, 16),
                      (17, 17, 17),
                      (18, 18, 18),
                      (19, 19, 19),
                      (20, 20, 20) ''')
    conexion.commit()
insert_tablas_debiles()

#______________________________________________________________________
#A CONTINUACION TODAS LAS ENTIDADES ASOCIATIVAS
def crear_tablas_asociativas():
    # Tabla "region_ubicacion"
    cursor.execute('''CREATE TABLE IF NOT EXISTS region_ubicacion (
                   `id_region` INTEGER NOT NULL,
                   `id_ubicacion` INTEGER NOT NULL,
                   FOREIGN KEY(`id_region`) REFERENCES region(`id_region`),
                   FOREIGN KEY(`id_ubicacion`) REFERENCES ubicacion(`id_ubicacion`) )''')

    # Tabla "vina_ubicacion"
    cursor.execute('''CREATE TABLE IF NOT EXISTS vina_ubicacion (
                   `id_vina` INTEGER NOT NULL,
                   `id_ubicacion` INTEGER NOT NULL,
                   FOREIGN KEY(`id_vina`) REFERENCES vina(`id_vina`),
                   FOREIGN KEY(`id_ubicacion`) REFERENCES ubicacion(`id_ubicacion`))''')

    # Tabla "vina_region"
    cursor.execute('''CREATE TABLE IF NOT EXISTS vina_region (
                `id_vina` INTEGER NOT NULL,
                `id_region` INTEGER NOT NULL,
                FOREIGN KEY(`id_vina`) REFERENCES vina(`id_vina`),
                FOREIGN KEY(`id_region`) REFERENCES region(`id_region`))''')

    # Tabla "producto_stock"
    cursor.execute('''CREATE TABLE IF NOT EXISTS producto_stock (
                `id_stock` INTEGER NOT NULL,
                `id_producto` INTEGER NOT NULL,
                FOREIGN KEY(`id_stock`) REFERENCES stock(`id_stock`),
                FOREIGN KEY(`id_producto`) REFERENCES producto(`id_producto`))''')

    # Tabla "descuento_producto"
    cursor.execute('''CREATE TABLE IF NOT EXISTS descuento_producto(
                `id_descuento` INTEGER NOT NULL,
                `id_producto` INTEGER NOT NULL,
                FOREIGN KEY(`id_descuento`) REFERENCES descuento(`id_descuento`),
                FOREIGN KEY(`id_producto`) REFERENCES producto(`id_producto`))''')

    # Tabla "vina_producto"
    cursor.execute('''CREATE TABLE IF NOT EXISTS vina_producto (
                `id_vina` INTEGER NOT NULL,
                `id_producto` INTEGER NOT NULL,
                FOREIGN KEY(`id_vina`) REFERENCES vina(`id_vina`),
                FOREIGN KEY(`id_producto`) REFERENCES producto(`id_producto`))''')

    # Tabla "producto_venta"
    cursor.execute('''CREATE TABLE IF NOT EXISTS producto_venta(
                `id_producto` INTEGER NOT NULL,
                `id_venta` INTEGER NOT NULL,
                FOREIGN KEY(`id_producto`) REFERENCES producto(`id_producto`),
                FOREIGN KEY(`id_venta`) REFERENCES venta(`id_venta`))''')

    # Tabla "venta_cliente"
    cursor.execute('''CREATE TABLE IF NOT EXISTS venta_cliente(
                `id_venta` INTEGER NOT NULL,
                `id_cliente` INTEGER NOT NULL,
                FOREIGN KEY(`id_venta`) REFERENCES venta(`id_venta`),
                FOREIGN KEY(`id_cliente`) REFERENCES cliente(`id_cliente`))''')

    # Tabla "reserva_descuento"
    cursor.execute('''CREATE TABLE IF NOT EXISTS reserva_descuento (
                `id_reserva` INTEGER NOT NULL,
                `id_descuento` INTEGER NOT NULL,
                FOREIGN KEY(`id_reserva`) REFERENCES reserva(`id_reserva`),
                FOREIGN KEY(`id_descuento`) REFERENCES descuento(`id_descuento`))''')

    # Tabla "vina_tour"
    cursor.execute('''CREATE TABLE IF NOT EXISTS vina_tour(
                `id_vina` INTEGER NOT NULL,
                `id_tour` INTEGER NOT NULL,
                FOREIGN KEY(`id_vina`) REFERENCES vina(`id_vina`),
                FOREIGN KEY(`id_tour`) REFERENCES tour(`id_tour`))''')

    # Tabla "valoracion_tour"
    cursor.execute('''CREATE TABLE IF NOT EXISTS valoracion_tour (
                `id_valoracion` INTEGER NOT NULL,
                `id_tour` INTEGER NOT NULL,
                FOREIGN KEY(`id_valoracion`) REFERENCES valoracion(`id_valoracion`),
                FOREIGN KEY(`id_tour`) REFERENCES tour(`id_tour`))''')

    # Tabla "tour_precio_total"
    cursor.execute('''CREATE TABLE IF NOT EXISTS tour_precio_total (
                `id_tour` INTEGER NOT NULL,
                `id_precio_total` INTEGER NOT NULL,
                FOREIGN KEY(`id_tour`) REFERENCES tour(`id_tour`),
                FOREIGN KEY(`id_precio_total`) REFERENCES precio_total(`id_precio_total`))''')

    # Tabla "reserva_tour"
    cursor.execute('''CREATE TABLE IF NOT EXISTS reserva_tour (
                `id_reserva` INTEGER NOT NULL,
                `id_tour` INTEGER NOT NULL,
                FOREIGN KEY(`id_reserva`) REFERENCES reserva(`id_reserva`),
                FOREIGN KEY(`id_tour`) REFERENCES tour(`id_tour`))''')

    # Tabla "reserva_acompanante"
    cursor.execute('''CREATE TABLE IF NOT EXISTS reserva_acompanante (
                `id_reserva` INTEGER NOT NULL,
                `id_acompanante` INTEGER NOT NULL,
                FOREIGN KEY(`id_reserva`) REFERENCES reserva(`id_reserva`),
                FOREIGN KEY(`id_acompanante`) REFERENCES acompanante(`id_acompanante`))''')

    # Confirmar los cambios en la base de datos
    conexion.commit()
crear_tablas_asociativas()

def insert_tablas_asociativas():
        #region_ubicacion
    cursor.execute('''INSERT INTO region_ubicacion (id_region, id_ubicacion)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #vina_direccion
    cursor.execute('''INSERT INTO vina_ubicacion (id_vina, id_ubicacion)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #vina_region
    cursor.execute('''INSERT INTO vina_region (id_vina, id_region)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #producto_stock
    cursor.execute('''INSERT INTO producto_stock (id_stock, id_producto)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #descuento_producto
    cursor.execute('''INSERT INTO descuento_producto (id_descuento, id_producto)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #vina_producto
    cursor.execute('''INSERT INTO vina_producto (id_vina, id_producto)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #producto_venta
    cursor.execute('''INSERT INTO producto_venta (id_producto, id_venta)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #venta_cliente
    cursor.execute('''INSERT INTO venta_cliente (id_venta, id_cliente)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #reserva_descuento
    cursor.execute('''INSERT INTO reserva_descuento (id_reserva, id_descuento)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #vina_tour
    cursor.execute('''INSERT INTO vina_tour (id_vina, id_tour)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #valoracion_tour
    cursor.execute('''INSERT INTO valoracion_tour (id_valoracion, id_tour)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #tour_precio_total
    cursor.execute('''INSERT INTO tour_precio_total (id_tour, id_precio_total)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #reserva_tour
    cursor.execute('''INSERT INTO reserva_tour (id_reserva, id_tour)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
        #reserva_acompanante 
    cursor.execute('''INSERT INTO reserva_acompanante (id_reserva, id_acompanante)
                   VALUES 
                   (1, 1), (2, 2), (3, 3), (4, 4), (5, 5), 
                   (6, 6), (7, 7), (8, 8), (9, 9), (10, 10), 
                   (11, 11), (12, 12), (13, 13), (14, 14), 
                   (15, 15), (16, 16), (17, 17), (18, 18), 
                   (19, 19), (20, 20)
                ''')
    conexion.commit()
insert_tablas_asociativas()

#MENU