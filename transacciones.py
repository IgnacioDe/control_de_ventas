import sqlite3

def registrar_transaccion(tipo, producto_id, cantidad, total):
    """
    Registra una transacción de compra o venta en la base de datos y actualiza el stock del producto.

    Args:
        tipo (str): Tipo de transacción ("venta" o "compra").
        producto_id (int): ID del producto.
        cantidad (int): Cantidad de productos.
        total (float): Total de la transacción.

    Returns:
        bool: True si la transacción se registró con éxito, False en caso de error.
    """
    if tipo not in ["venta", "compra"]:
        print("Error: Tipo de transacción inválido. Use 'venta' o 'compra'.")
        return False

    try:
        with sqlite3.connect("gestion_bebidas.db") as conexion:
            cursor = conexion.cursor()

            # Verificar stock para ventas
            if tipo == "venta":
                cursor.execute("SELECT stock FROM productos WHERE id = ?", (producto_id,))
                stock_disponible = cursor.fetchone()

                if stock_disponible is None:
                    print(f"Error: Producto con ID {producto_id} no encontrado.")
                    return False

                stock_disponible = stock_disponible[0]
                if stock_disponible < cantidad:
                    print("Error: Stock insuficiente para realizar la venta.")
                    return False

            # Registrar la transacción
            consulta = """
            INSERT INTO transacciones (tipo, producto_id, cantidad, total)
            VALUES (?, ?, ?, ?)
            """
            cursor.execute(consulta, (tipo, producto_id, cantidad, total))

            # Actualizar stock según el tipo de transacción
            if tipo == "venta":
                cursor.execute("UPDATE productos SET stock = stock - ? WHERE id = ?", (cantidad, producto_id))
            elif tipo == "compra":
                cursor.execute("UPDATE productos SET stock = stock + ? WHERE id = ?", (cantidad, producto_id))

            conexion.commit()
            print(f"Transacción de {tipo} registrada exitosamente.")
            return True

    except sqlite3.Error as e:
        print(f"Error al registrar la transacción: {e}")
        return False

def calcular_totales():
    """
    Calcula y muestra los totales de ingresos, egresos, ganancia neta y porcentaje de ganancia.
    """
    try:
        with sqlite3.connect("gestion_bebidas.db") as conexion:
            cursor = conexion.cursor()

            # Calcular ingresos (ventas)
            cursor.execute("SELECT SUM(total) FROM transacciones WHERE tipo = 'venta'")
            ingresos = cursor.fetchone()[0] or 0

            # Calcular egresos (compras)
            cursor.execute("SELECT SUM(total) FROM transacciones WHERE tipo = 'compra'")
            egresos = cursor.fetchone()[0] or 0

            # Calcular ganancias netas y porcentaje
            ganancia_neta = ingresos - egresos
            porcentaje_ganancia = (ganancia_neta / egresos * 100) if egresos > 0 else 0

        # Mostrar resultados
        print("\n------ Resumen Financiero ------")
        print(f"Ingresos por ventas:       ${ingresos:.2f}")
        print(f"Egresos por compras:       ${egresos:.2f}")
        print(f"Ganancia neta:             ${ganancia_neta:.2f}")
        print(f"Porcentaje de ganancia:    {porcentaje_ganancia:.2f}%")
        print("--------------------------------\n")

        return ingresos, egresos, ganancia_neta, porcentaje_ganancia

    except sqlite3.Error as e:
        print(f"Error al calcular totales: {e}")
        return 0, 0, 0, 0

def listar_transacciones():
    """
    Muestra todas las transacciones almacenadas en la base de datos de forma legible.
    """
    try:
        with sqlite3.connect("gestion_bebidas.db") as conexion:
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM transacciones")
            transacciones = cursor.fetchall()

        if not transacciones:
            print("No se encontraron transacciones registradas.")
            return

        print("------------- Lista de Transacciones -------------")
        print(f"{'ID':<5} {'Tipo':<10} {'Fecha':<15} {'Cantidad':<10} {'Total':<10}")
        print("-" * 50)

        for transaccion in transacciones:
            transaccion_id, tipo, fecha, cantidad, total = transaccion
            print(f"{transaccion_id:<5} {tipo:<10} {fecha:<15} {cantidad:<10} ${total:<10.2f}")

    except sqlite3.Error as e:
        print(f"Error al acceder a la base de datos: {e}")
