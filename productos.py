import sqlite3
from db_manager import reorganizar_ids
from tkinter import messagebox

def agregar_producto(nombre, tipo, precio_compra, precio_venta, stock):
    """
    Agrega un nuevo producto a la base de datos de gestión de bebidas.

    Parámetros:
    - nombre (str): Nombre del producto a agregar. Ejemplo: "Coca Cola".
    - tipo (str): Categoría o tipo del producto. Ejemplo: "Bebida gaseosa".
    - precio_compra (float): Costo del producto para el negocio. Ejemplo: 10.50.
    - precio_venta (float): Precio al que el producto será vendido. Ejemplo: 15.00.
    - stock (int): Cantidad inicial del producto en inventario. Ejemplo: 50.

    Return:
        None
    """
    conexion = sqlite3.connect("gestion_bebidas.db")
    cursor = conexion.cursor()

    consulta = """
    INSERT INTO productos (nombre, tipo, precio_compra, precio_venta, stock)
    VALUES (?, ?, ?, ?, ?)
    """

    datos = (nombre, tipo, precio_compra, precio_venta, stock)
    cursor.execute(consulta, datos)
    conexion.commit()

    print(f"Producto '{nombre}' agregado exitosamente.")
    listar_productos()
    conexion.close()


def eliminar_producto_por_nombre(nombre):
    """
    Elimina un producto de la base de datos basado en su nombre.
    Si hay múltiples productos con el mismo nombre, permite seleccionar un ID.
    """
    conexion = sqlite3.connect("gestion_bebidas.db")
    cursor = conexion.cursor()

    try:
        # Verificar si existen productos con ese nombre
        cursor.execute("SELECT * FROM productos WHERE nombre = ?", (nombre,))
        productos = cursor.fetchall()

        if not productos:
            messagebox.showerror("Error", "No se encontró ningún producto con ese nombre.")
            return False

        # Si hay múltiples productos con el mismo nombre, mostrar opciones
        if len(productos) > 1:
            print("Se encontraron múltiples productos con ese nombre:")
            print(f"{'ID':<5} {'Nombre':<20} {'Compra':<10} {'Venta':<10} {'Stock':<10}")
            print("-" * 60)
            for producto in productos:
                id_producto, nombre_producto, precio_compra, precio_venta, stock = producto
                print(f"{id_producto:<5} {nombre_producto:<20} {precio_compra:<10.2f} {precio_venta:<10.2f} {stock:<10}")

            try:
                producto_id = int(input("Ingrese el ID del producto a eliminar: "))
            except ValueError:
                messagebox.showerror("Error", "ID no válido. Operación cancelada.")
                return False

            # Verificar que el ID ingresado esté en la lista
            if not any(p[0] == producto_id for p in productos):
                messagebox.showerror("Error", "El ID ingresado no coincide con ningún producto.")
                return False

            # Llamar a la función existente para eliminar por ID
            eliminar_producto_por_id(producto_id)

        else:
            # Eliminar directamente si solo hay un producto con ese nombre
            producto_id = productos[0][0]
            eliminar_producto_por_id(producto_id)

        return True

    except sqlite3.Error as e:
        print(f"Error al eliminar el producto: {e}")
        return False

    finally:
        conexion.close()


def eliminar_producto_por_id(producto_id):
    """
    Elimina un producto de la base de datos basado en su ID.
    También reorganiza los IDs después de la eliminación.
    """
    conexion = sqlite3.connect("gestion_bebidas.db")
    cursor = conexion.cursor()

    try:
        # Verificar si el producto existe
        cursor.execute("SELECT * FROM productos WHERE id = ?", (producto_id,))
        producto = cursor.fetchone()
        if not producto:
            messagebox.showerror("Error", "No se encontró un producto con ese ID.")
            return False

        # Eliminar el producto
        cursor.execute("DELETE FROM productos WHERE id = ?", (producto_id,))
        conexion.commit()
        print(f"Producto con ID {producto_id} eliminado exitosamente.")

        # Llamar a la función para reorganizar IDs
        reorganizar_ids()
        return True

    except sqlite3.Error as e:
        print(f"Error al eliminar el producto: {e}")
        return False

    finally:
        conexion.close()

def listar_productos():
    """
    Lista todos los productos de la base de datos y los muestra en formato de tabla.

    Cada producto incluye su ID, nombre, precio de compra, precio de venta y stock disponible.
    """
    try:
        with sqlite3.connect("gestion_bebidas.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            if not productos:
                print("No hay productos registrados en la base de datos.")
                return

            # Encabezados de tabla
            print("------------- Lista de Productos -------------")
            print(f"{'ID':<5} {'Nombre':<20} {'Compra':<10} {'Venta':<10} {'Stock':<10}")
            print("-" * 60)

            # Imprimir cada producto
            for producto in productos:
                id_producto, nombre, precio_compra, precio_venta, stock = producto
                print(f"{id_producto:<5} {nombre:<20} {precio_compra:<10.2f} {precio_venta:<10.2f} {stock:<10}")

    except sqlite3.Error as e:
        print(f"Error al listar los productos: {e}")