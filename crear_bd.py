import sqlite3

def crear_base_datos():
    """
    Crea y asegura la existencia de las tablas principales en la base de datos SQLite.

    Funcionalidad:
    - Conecta a la base de datos `gestion_bebidas.db` o la crea si no existe.
    - Crea las siguientes tablas, si no existen:
        1. `productos`: Almacena información sobre los productos.
        2. `transacciones`: Registra las compras y ventas realizadas.
        3. `usuarios`: Almacena la información de los usuarios y sus roles.

    Tablas:
    - `productos`:
        - id: Identificador único del producto.
        - nombre: Nombre del producto (texto, requerido).
        - tipo: Tipo del producto (texto, requerido).
        - precio_compra: Precio de compra del producto (real, requerido).
        - precio_venta: Precio de venta del producto (real, requerido).
        - stock: Cantidad de producto disponible en inventario (entero, requerido).

    - `transacciones`:
        - id: Identificador único de la transacción.
        - tipo: Tipo de transacción ('compra' o 'venta').
        - producto_id: Referencia al ID del producto (clave foránea).
        - cantidad: Cantidad involucrada en la transacción.
        - fecha: Fecha de la transacción (por defecto, la fecha actual).
        - total: Monto total de la transacción.

    - `usuarios`:
        - id: Identificador único del usuario.
        - nombre: Nombre del usuario (texto, requerido).
        - contrasena: Contraseña del usuario (texto, requerido).
        - rol: Rol del usuario ('admin' o 'usuario').

    Retorno:
    - Imprime un mensaje indicando que las tablas han sido creadas con éxito.
    - Cierra la conexión a la base de datos después de la creación.

    Consideraciones:
    - Utiliza `CREATE TABLE IF NOT EXISTS` para evitar errores si las tablas ya existen.
    - Asegúrate de manejar cualquier error de conexión o SQL en un bloque `try-except` para evitar interrupciones.
    """
    conexion = sqlite3.connect("gestion_bebidas.db")
    cursor = conexion.cursor()

    try:
        # Crear tabla de productos
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock INTEGER NOT NULL
        )
        """)

        # Crear tabla de transacciones
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS transacciones (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            tipo TEXT CHECK(tipo IN ('compra', 'venta')) NOT NULL,
            producto_id INTEGER NOT NULL,
            cantidad INTEGER NOT NULL,
            fecha TEXT DEFAULT CURRENT_TIMESTAMP,
            total REAL NOT NULL,
            FOREIGN KEY (producto_id) REFERENCES productos (id)
        )
        """)

        # Crear tabla de usuarios
        cursor.execute("""
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            contrasena TEXT NOT NULL,
            rol TEXT NOT NULL CHECK (rol IN ('admin', 'usuario'))
        )
        """)

        print("Base de datos y tablas creadas exitosamente.")
    except sqlite3.Error as e:
        print(f"Error al crear las tablas: {e}")
    finally:
        conexion.close()