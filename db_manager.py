import sqlite3
import pandas as pd
from fpdf import FPDF
from tkinter import messagebox

# Funcion para conectar a la base de datos
def obtener_conexion():
    """
    Establece y devuelve una conexión a la base de datos SQLite.

    - La función utiliza el archivo `gestion_bebidas.db` como base de datos.
    - El parámetro `check_same_thread=False` permite compartir la conexión entre múltiples hilos,
      lo cual es útil si se utiliza la base de datos en aplicaciones multihilo.

    Retorna:
        sqlite3.Connection: Objeto de conexión a la base de datos.
    """

    return sqlite3.connect("gestion_bebidas.db", check_same_thread=False)

# Opcional
def insertar_usuario_admin():
    """
    Inserta un usuario con privilegios de administrador en la base de datos al iniciar el programa por primera vez.
    
    - Verifica si el usuario administrador ya existe mediante una bandera en la base de datos.
    - Si no existe, lo crea con valores predeterminados (nombre: 'admin', contraseña: 'admin123').
    - Solo se ejecuta una vez al iniciar el programa por primera vez.
    
    Parámetros:
        Ninguno.
    """

    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Crear la tabla de configuración si no existe
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS configuracion (
                clave TEXT PRIMARY KEY,
                valor TEXT
            )
        """)

        # Verificar si ya se creó el usuario administrador
        cursor.execute("SELECT valor FROM configuracion WHERE clave = 'admin_creado'")
        admin_creado = cursor.fetchone()

        if admin_creado and admin_creado[0] == "true":
            # Si ya existe el administrador, no hacer nada
            return

        # Insertar el usuario administrador
        cursor.execute("INSERT INTO usuarios (nombre, contrasena, rol) VALUES (?, ?, ?)",
                       ("admin", "admin123", "admin"))

        # Registrar que el administrador ha sido creado
        cursor.execute("INSERT OR REPLACE INTO configuracion (clave, valor) VALUES (?, ?)",
                       ("admin_creado", "true"))

        conexion.commit()
        print("Usuario administrador creado exitosamente.")
    except Exception as e:
        print(f"Error al insertar usuario administrador: {e}")
    finally:
        conexion.close()

def agregar_producto_db(nombre, tipo, precio_compra, precio_venta, stock):
    """
    Agrega un nuevo producto a la base de datos.

    Parámetros:
        nombre (str): Nombre del producto.
        tipo (str): Tipo o categoría del producto (por ejemplo, "bebida alcohólica", "refresco").
        precio_compra (float): Precio de compra del producto.
        precio_venta (float): Precio de venta del producto.
        stock (int): Cantidad inicial de unidades disponibles en inventario.

    Manejo de errores:
    - La función asume que la conexión con la base de datos está correctamente configurada.
    - Si los parámetros proporcionados no coinciden con los tipos esperados o si la tabla `productos` no existe, puede generar errores.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("INSERT INTO productos (nombre, tipo, precio_compra, precio_venta, stock) VALUES (?, ?, ?, ?, ?)",
                   (nombre, tipo, precio_compra, precio_venta, stock))
    conexion.commit()
    conexion.close()

def registrar_transaccion_db(producto_id, tipo, cantidad):
    """
    Registra una transacción en la base de datos y actualiza el stock del producto correspondiente.

    Parámetros:
        producto_id (int): ID del producto involucrado en la transacción.
        tipo (str): Tipo de transacción ("compra" o "venta").
        cantidad (int): Cantidad de producto que se compra o vende.

    Manejo de errores:
    - Si el producto no se encuentra, muestra un mensaje de error y no realiza ninguna operación.
    - Si el stock es insuficiente para una venta, detiene la operación y muestra un mensaje de advertencia.
    
    Retorna:
        True si la transacción se registra correctamente, False en caso contrario.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    try:
        # Obtener información del producto
        cursor.execute("SELECT stock, precio_compra, precio_venta FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()

        if not producto:
            messagebox.showerror("Error", "Producto no encontrado.")
            return False

        stock_actual, precio_compra, precio_venta = producto

        # Determinar el nuevo stock
        nuevo_stock = stock_actual + cantidad if tipo == "compra" else stock_actual - cantidad
        if nuevo_stock < 0:
            messagebox.showwarning("Error", "Stock insuficiente para realizar la venta.")
            return False

        # Determinar el total de la transacción
        precio = precio_compra if tipo == "compra" else precio_venta
        total = precio * cantidad

        # Actualizar el stock del producto
        cursor.execute("UPDATE productos SET stock = ? WHERE id = ?", (nuevo_stock, producto_id))

        # Registrar la transacción
        cursor.execute("""
            INSERT INTO transacciones (tipo, producto_id, cantidad, total)
            VALUES (?, ?, ?, ?)
        """, (tipo, producto_id, cantidad, total))

        # Confirmar los cambios
        conexion.commit()
        return True  # Transacción exitosa

    except sqlite3.Error as e:
        messagebox.showerror("Error", f"No se pudo registrar la transacción: {e}")
        return False

    finally:
        conexion.close()

def reorganizar_ids():
    """
    Reorganiza los IDs de la tabla `productos` de manera secuencial eliminando 
    los posibles saltos en el contador autoincremental.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Crear tabla temporal con los datos existentes
    cursor.execute("""
        CREATE TEMPORARY TABLE productos_temp AS
        SELECT * FROM productos;
    """)

    # Borrar la tabla original
    cursor.execute("DROP TABLE productos;")

    # Crear la tabla original nuevamente
    cursor.execute("""
        CREATE TABLE productos (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT NOT NULL,
            tipo TEXT NOT NULL,
            precio_compra REAL NOT NULL,
            precio_venta REAL NOT NULL,
            stock INTEGER NOT NULL
        );
    """)

    # Insertar los datos de la tabla temporal
    cursor.execute("""
        INSERT INTO productos (nombre, tipo, precio_compra, precio_venta, stock)
        SELECT nombre, tipo, precio_compra, precio_venta, stock FROM productos_temp;
    """)

    # Borrar la tabla temporal
    cursor.execute("DROP TABLE productos_temp;")

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

def reiniciar_transacciones():
    """
    Reinicia la tabla de transacciones eliminando todos los registros y 
    restableciendo el contador de IDs autoincrementales.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Eliminar todos los registros de la tabla transacciones
    cursor.execute("DELETE FROM transacciones;")

    # Restablecer el contador autoincremental de la tabla transacciones
    cursor.execute("DELETE FROM sqlite_sequence WHERE name = 'transacciones';")

    # Confirmar los cambios y cerrar la conexión
    conexion.commit()
    conexion.close()

def registrar_modificacion_db(producto_id, valor_compra, valor_venta):
    """
    Actualiza los valores de compra y venta de un producto en la base de datos.

    Parámetros:
    - producto_id (int): ID del producto que se desea modificar.
    - valor_compra (float): Nuevo precio de compra para el producto.
    - valor_venta (float): Nuevo precio de venta para el producto.

    Retorno:
    - (str): 
      - "Producto no encontrado" si el ID del producto no existe en la base de datos.
      - "Modificación registrada." si la operación se realiza con éxito.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()

    # Obtener información del producto
    cursor.execute("SELECT precio_compra, precio_venta FROM productos WHERE id = ?", (producto_id,))
    producto = cursor.fetchone()

    if not producto:
        conexion.close()    
        return "Producto no encontrado"

    # Actualizar modificaciones del producto
    cursor.execute("UPDATE productos SET precio_compra = ? WHERE id = ?", (valor_compra, producto_id))
    cursor.execute("UPDATE productos SET precio_venta = ? WHERE id = ?", (valor_venta, producto_id))

    conexion.commit()
    conexion.close()
    return "Modificación registrada."

def generar_reporte_excel(nombre):
    """
    Exporta las transacciones registradas en la base de datos a un archivo Excel.
    """
    # Consulta de datos desde la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM transacciones")  # Cambia según tu tabla
    datos = cursor.fetchall()
    conexion.close()

    # Crear DataFrame para exportar
    columnas = ["ID", "Tipo", "Producto ID", "Cantidad", "Fecha", "Total"]
    df = pd.DataFrame(datos, columns=columnas)

    # Exportar a Excel
    try:
        df.to_excel(nombre, index=False, engine="openpyxl")
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el reporte en Excel: {e}")

def generar_reporte_pdf(nombre):
    """
    Genera un reporte en formato PDF con los datos de transacciones almacenados en la base de datos.

    Parámetros:
    - nombre (str): Ruta y nombre del archivo donde se guardará el reporte PDF.

    Return:
    - No retorna valores. Crea un archivo PDF en la ubicación especificada.
    """
    # Consulta de datos desde la base de datos
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT * FROM transacciones")  # Cambia según tu tabla
    datos = cursor.fetchall()
    conexion.close()

    # Crear el PDF
    pdf = FPDF()
    pdf.set_auto_page_break(auto=True, margin=15)
    pdf.add_page()
    pdf.set_font("Arial", size=12)

    # Título
    pdf.set_font("Arial", style="B", size=16)
    pdf.cell(200, 10, txt="Reporte de Transacciones", ln=True, align="C")
    pdf.ln(10)

    # Encabezados
    pdf.set_font("Arial", style="B", size=12)
    encabezados = ["ID", "Tipo", "Producto ID", "Cantidad", "Fecha", "Total"]
    for encabezado in encabezados:
        pdf.cell(30, 10, encabezado, border=1, align="C")
    pdf.ln()

    # Datos
    pdf.set_font("Arial", size=10)
    for fila in datos:
        for columna in fila:
            pdf.cell(30, 10, str(columna), border=1, align="C")
        pdf.ln()

    # Guardar el archivo
    try:
        pdf.output(nombre)
    except Exception as e:
        messagebox.showerror("Error", f"No se pudo generar el reporte en PDF: {e}")

def verificar_stock_bajo(umbral=5):
    """
    Verifica qué productos tienen un nivel de stock igual o por debajo del umbral especificado
    y muestra una alerta si existen productos en esta condición.

    Parámetros:
    - umbral (int, opcional): Cantidad mínima de stock para que un producto se considere
      como "bajo stock". Por defecto es 5.

    Retunr:
        None

    Consideraciones futuras:
    - Podrías añadir un registro en la base de datos para alertas generadas.
    - Implementar configuraciones dinámicas para el umbral según tipo de producto.
    """
    conexion = obtener_conexion()
    cursor = conexion.cursor()
    cursor.execute("SELECT id, nombre, stock FROM productos WHERE stock <= ?", (umbral,))
    productos_bajo_stock = cursor.fetchall()
    conexion.close()

    if productos_bajo_stock:
        mensaje = """¡ALERTA!
        Productos con bajo stock: \n\n"""
        for producto in productos_bajo_stock:
            mensaje += f"ID: {producto[0]}, Nombre: {producto[1]}, Stock: {producto[2]}\n"

        messagebox.showwarning("Stock Bajo", mensaje)