# -------------- Importaciones ----------------
import tkinter as tk
import ttkbootstrap as ttkb
from crear_bd import crear_base_datos
from ttkbootstrap.constants import *
from tkinter import ttk, messagebox, filedialog
from productos import *
from transacciones import calcular_totales
from db_manager import *

tema_actual = "flatly" # Variable global, por defecto, tema claro para la ventanas

def cambiar_tema(ventana):
    """
    Cambia el tema visual de la aplicación.

    Esta función permite alternar entre una lista de temas predefinidos para modificar 
    la apariencia visual de las ventanas y los widgets de la interfaz. Al ejecutarse, 
    actualiza el tema global de la aplicación, registra nuevamente los estilos personalizados 
    y actualiza los widgets de la ventana principal para reflejar el cambio.

    Args:
        ventana (ttkb.Window): La ventana principal de la aplicación cuya apariencia 
        será actualizada tras el cambio de tema.

    Returns:
        None
    """
    global tema_actual

    # Lista de temas disponibles
    temas_disponibles = ["darkly", "cosmo", "flatly", "solar", "cyborg"]
    indice_actual = temas_disponibles.index(tema_actual)
    tema_actual = temas_disponibles[(indice_actual + 1) % len(temas_disponibles)]

    # Cambiar el tema globalmente
    style = ttkb.Style()
    style.theme_use(tema_actual)

    # Volver a registrar los estilos personalizados
    crear_estilos()

    # Actualizar los widgets de la interfaz principal
    actualizar_estilos(ventana)

def crear_estilos():
    """
    Define y aplica estilos personalizados para los widgets utilizados en la interfaz.

    Esta función utiliza el sistema de estilos de ttkbootstrap para personalizar la apariencia 
    de los botones y etiquetas de la aplicación, incluyendo características como fuente, 
    tamaño, formato y relleno. Los estilos personalizados permiten una apariencia coherente 
    y mejorada en toda la interfaz.

    Returns:
        None
    """
    style = ttkb.Style()

    # Estilo personalizado para botones
    style.configure(
        "Custom.TButton",  # Nombre del estilo
        font=("Amethysta", 8, "bold"),  # Fuente, tamaño y peso
        padding=10,  # Espaciado interno
    )

    # Estilo personalizado para etiquetas
    style.configure(
        "Custom.TLabel",  # Nombre del estilo
        font=("Arial", 20, "bold"),  # Fuente, tamaño y peso
        anchor="center",  # Alineación del texto
    )

def actualizar_estilos(ventana):
    """
    Reaplica estilos personalizados a los widgets existentes en la ventana.

    Esta función recorre todos los widgets hijos de una ventana específica y, dependiendo 
    del tipo de widget, actualiza su estilo para reflejar los ajustes personalizados definidos 
    previamente en la aplicación. Esto es útil cuando se cambian temas o estilos globales 
    durante la ejecución.

    Args:
        ventana (ttkb.Window): La ventana principal o secundaria cuyos widgets deben actualizarse.

    Returns:
        None
    """
    for widget in ventana.winfo_children():
        if isinstance(widget, ttk.Label):  # Si es una etiqueta
            widget.configure(style="Custom.TLabel")
        elif isinstance(widget, ttkb.Button):  # Si es un botón
            widget.configure(style="Custom.TButton")

def crear_widgets_principales(ventana, rol):
    """
    Crea los widgets principales de la interfaz gráfica.

    Esta función configura y agrega todos los botones y etiquetas necesarias para la ventana 
    principal de la aplicación. Los elementos creados incluyen botones para cambiar de tema, 
    acceder a distintas funciones como agregar/modificar productos, registrar transacciones, 
    gestionar usuarios, entre otros. Además, se aplican restricciones basadas en el rol del usuario.

    Args:
        ventana (ttkb.Window): La ventana principal de la aplicación.
        rol (str): El rol del usuario que ha iniciado sesión ("admin" o "usuario"). 
                   Este parámetro determina qué botones están habilitados o deshabilitados.

    Returns:
        None
    """
    global tema_actual

    # Configurar los estilos personalizados
    crear_estilos()

    # Estilo reutilizable para los botones
    estilo_boton = {"style": "Custom.TButton", "width": 20}

    # Botón para cambiar el tema de la aplicación
    btn_cambiar_tema = ttkb.Button(
        ventana, text="Cambiar Tema", command=lambda: cambiar_tema(ventana), **estilo_boton
    )
    btn_cambiar_tema.pack(pady=10)

    # Etiqueta con el título de la aplicación
    label_titulo = ttkb.Label(
        ventana, 
        text="GESTIÓN DE VENTAS",
        font=("Courgette", 18, "bold"),
        anchor="center"
    )
    label_titulo.pack(pady=20)

    # Definición de los botones principales y sus respectivas funciones
    botones = [
        ("Ver Tablas", abrir_ventana_tablas),
        ("Agregar Producto", ventana_agregar_producto),
        ("Modificar Producto", ventana_modificar_producto),
        ("Registrar Transacción", lambda: ventana_registrar_transaccion(rol_actual)),
        ("Eliminar Producto", ventana_eliminar_producto),
        ("Agregar Usuario", registrar_usuario),
        ("Ver Usuarios", ver_usuarios),
        ("Exportar Reporte", exportar_reporte),
        ("Reiniciar Transacciones", lambda: confirmar_reinicio()),
    ]

    # Crear los botones y configurarlos según el rol del usuario
    for texto, comando in botones:
        btn = ttkb.Button(ventana, text=texto, command=comando, **estilo_boton)
        btn.pack(pady=10)

        # Deshabilitar botones restringidos para usuarios con rol "usuario"
        if rol == "usuario" and texto in [
            "Agregar Usuario",
            "Modificar Producto",
            "Eliminar Producto",
            "Reiniciar Transacciones",
            "Agregar Producto",
            "Ver Usuarios",
            "Reiniciar Transacciones",
        ]:
            btn.config(state="disable")

def interfaz_principal(rol_actual):
    """
    Configura y lanza la ventana principal de la aplicación.

    Esta función inicia la interfaz principal de la aplicación de gestión de ventas. 
    Primero verifica que el usuario haya iniciado sesión correctamente, determinando 
    el rol ("admin" o "usuario") antes de mostrar la ventana principal. Si el inicio 
    de sesión falla, la aplicación se cierra automáticamente.

    Args:
        rol_actual (str): Rol del usuario que inicia sesión. Puede ser "admin" o "usuario". 
                          Si es None, se solicita iniciar sesión.

    Returns:
        None
    """
    global tema_actual

    insertar_usuario_admin()

    # Crear la ventana principal pero mantenerla oculta inicialmente
    ventana = ttkb.Window(themename=tema_actual)
    ventana.withdraw()  # Ocultar la ventana hasta que se complete el inicio de sesión
    ventana.title("Gestión de Ventas")
    ventana.geometry("400x650")

    # Iniciar sesión si el rol actual no ha sido definido
    if not rol_actual:
        rol_actual = iniciar_sesion()
        if not rol_actual:
            # Mostrar un mensaje de error si el inicio de sesión falla
            messagebox.showinfo(
                "Error de inicio de sesión",
                "Ingrese un usuario correcto para utilizar la App."
            )
            ventana.destroy()  # Cerrar la aplicación
            return

    # Mostrar la ventana principal y configurar los widgets
    ventana.deiconify()  # Hacer visible la ventana
    crear_widgets_principales(ventana, rol_actual)

    # Ejecutar el bucle principal de la interfaz
    ventana.mainloop()

def iniciar_sesion():
    """
    Muestra una ventana emergente para que el usuario inicie sesión y valida sus credenciales.

    Esta función abre una ventana modal para el inicio de sesión, solicita al usuario que ingrese 
    su nombre y contraseña, y verifica las credenciales en la base de datos. Si las credenciales 
    son válidas, se asigna el rol del usuario a la variable global `rol_actual` y se cierra la ventana.
    En caso contrario, muestra un mensaje de error y permite intentarlo nuevamente.

    Returns:
        str: El rol del usuario ("admin" o "usuario") si el inicio de sesión es exitoso.
             Devuelve None si el inicio de sesión falla.
    """
    global rol_actual

    # Crear ventana para el inicio de sesión
    ventana_login = ttkb.Toplevel()
    ventana_login.title("Iniciar Sesión")
    ventana_login.geometry("300x200")
    resultado = {"exitoso": False}  # Diccionario para almacenar el resultado del inicio de sesión

    # Widgets para el formulario de inicio de sesión
    ttkb.Label(ventana_login, text="Usuario:").pack(pady=5)
    entrada_usuario = ttkb.Entry(ventana_login)
    entrada_usuario.pack(pady=5)

    ttkb.Label(ventana_login, text="Contraseña:").pack(pady=5)
    entrada_contrasena = ttkb.Entry(ventana_login, show="*")
    entrada_contrasena.pack(pady=5)

    def verificar_credenciales():
        """
        Valida las credenciales del usuario ingresadas en los campos de texto.

        Si las credenciales coinciden con un registro en la base de datos, asigna el rol correspondiente 
        al usuario, cierra la ventana de inicio de sesión y permite el acceso a la aplicación. En caso de 
        error, muestra un mensaje de advertencia.
        """
        usuario = entrada_usuario.get()
        contrasena = entrada_contrasena.get()

        # Verificar credenciales en la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT rol FROM usuarios WHERE nombre=? AND contrasena=?", (usuario, contrasena))
        resultado_query = cursor.fetchone()
        conexion.close()

        if resultado_query:
            resultado["exitoso"] = True
            global rol_actual
            rol_actual = resultado_query[0]
            messagebox.showinfo("Éxito", f"Bienvenido {usuario} - Rol: {rol_actual}")
            ventana_login.destroy()  # Cerrar la ventana de inicio de sesión
        else:
            messagebox.showerror("Error", "Usuario o contraseña incorrectos")

    # Botón para iniciar sesión
    ttkb.Button(ventana_login, text="Iniciar Sesión", command=verificar_credenciales).pack(pady=10)

    # Esperar a que la ventana se cierre antes de continuar
    ventana_login.wait_window()
    return rol_actual

def registrar_usuario():
    """
    Abre una ventana para registrar un nuevo usuario en la base de datos con su respectivo rol.

    Esta función permite registrar nuevos usuarios junto con su rol en la aplicación. 
    El rol debe ser "admin" o "usuario". Solo los usuarios con el rol de "admin" pueden 
    ejecutar esta función. Los datos se almacenan en la base de datos y se valida que 
    el rol sea correcto antes de registrar al usuario.

    Returns:
        None
    """
    # Crear la ventana de registro
    ventana_registro = tk.Toplevel()
    ventana_registro.title("Registrar Nuevo Usuario")
    ventana_registro.geometry("300x250")

    # Campos para ingresar los datos del nuevo usuario
    ttkb.Label(ventana_registro, text="Nombre de Usuario:").pack()
    entrada_usuario = ttkb.Entry(ventana_registro)
    entrada_usuario.pack()

    ttkb.Label(ventana_registro, text="Contraseña:").pack()
    entrada_contrasena = ttkb.Entry(ventana_registro, show="*")
    entrada_contrasena.pack()

    ttkb.Label(ventana_registro, text="Rol (admin/usuario):").pack()
    entrada_rol = ttkb.Entry(ventana_registro)
    entrada_rol.pack()

    def agregar_usuario():
        """
        Registra al nuevo usuario en la base de datos.

        Valida que el rol ingresado sea "admin" o "usuario". Si los datos son válidos,
        agrega el nuevo usuario en la base de datos. En caso de error, muestra un mensaje
        al usuario.
        """
        nombre = entrada_usuario.get()
        contrasena = entrada_contrasena.get()
        rol = entrada_rol.get()

        # Validar el rol
        if rol not in ["admin", "usuario"]:
            messagebox.showerror("Error", "El rol debe ser 'admin' o 'usuario'")
            return

        # Conectar a la base de datos y registrar al usuario
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        try:
            cursor.execute("INSERT INTO usuarios (nombre, contrasena, rol) VALUES (?, ?, ?)",
                           (nombre, contrasena, rol))
            conexion.commit()
            messagebox.showinfo("Éxito", "Usuario registrado correctamente")
            ventana_registro.destroy()  # Cerrar la ventana tras el registro exitoso
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo registrar el usuario: {e}")
        finally:
            conexion.close()

    # Botón para confirmar el registro
    tk.Button(ventana_registro, text="Registrar", command=agregar_usuario).pack(pady=10)

def ver_usuarios():
    """
    Muestra una ventana con la lista de usuarios y contraseñas registradas en la base de datos,
    y permite eliminar usuarios. Solo es accesible si el usuario actual tiene permisos de administrador.

    Esta función utiliza un Treeview para presentar los datos y proporciona un botón para eliminar
    usuarios seleccionados de la base de datos.
    """

    def eliminar_usuario():
        """
        Elimina al usuario seleccionado de la base de datos y actualiza la lista de usuarios en la ventana.
        """
        try:
            # Obtener la selección actual
            seleccion = tree.selection()
            if not seleccion:
                messagebox.showwarning("Advertencia", "Debe seleccionar un usuario para eliminar.")
                return

            # Confirmar eliminación
            if not messagebox.askyesno("Confirmar", "¿Está seguro de que desea eliminar el usuario seleccionado?"):
                return

            # Obtener el nombre del usuario seleccionado
            usuario_seleccionado = tree.item(seleccion, "values")[0]

            # Eliminar el usuario de la base de datos
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("DELETE FROM usuarios WHERE nombre=?", (usuario_seleccionado,))
            conexion.commit()
            conexion.close()

            # Eliminar el usuario del Treeview
            tree.delete(seleccion)

            messagebox.showinfo("Éxito", f"Usuario '{usuario_seleccionado}' eliminado correctamente.")
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo eliminar el usuario: {e}")

    # Crear la ventana para mostrar los usuarios registrados
    ventana_usuarios = ttkb.Toplevel()
    ventana_usuarios.title("Usuarios Registrados")
    ventana_usuarios.geometry("500x400")

    # Crear un Treeview para mostrar los usuarios
    tree = ttkb.Treeview(ventana_usuarios, columns=("Usuario", "Contraseña"), show="headings")
    tree.heading("Usuario", text="Usuario")
    tree.heading("Contraseña", text="Contraseña")
    tree.pack(fill=tk.BOTH, expand=True, pady=10)

    # Botón para eliminar el usuario seleccionado
    ttkb.Button(ventana_usuarios, text="Eliminar Usuario", command=eliminar_usuario).pack(pady=10)

    # Conectar a la base de datos y cargar los datos de los usuarios
    try:
        conexion = obtener_conexion()
        cursor = conexion.cursor()
        cursor.execute("SELECT nombre, contrasena FROM usuarios")
        usuarios = cursor.fetchall()
        conexion.close()

        # Insertar los datos en el Treeview
        for usuario, contrasena in usuarios:
            tree.insert("", tk.END, values=(usuario, contrasena))
    except Exception as e:
        messagebox.showerror("Error", f"No se pudieron cargar los usuarios: {e}")

def ventana_agregar_producto():
    """
    Abre una ventana para agregar un nuevo producto. 
    Permite ingresar detalles como nombre, tipo, precio de compra, precio de venta y cantidad.
    """
    # Crear la ventana
    ventana_agregar = ttkb.Toplevel()
    ventana_agregar.title("Agregar Producto")
    ventana_agregar.geometry("600x400")

    # Etiquetas y entradas para los datos del producto
    ttkb.Label(ventana_agregar, text="Nombre del Producto:").pack(pady=5)
    entry_nombre = ttkb.Entry(ventana_agregar)
    entry_nombre.pack(pady=5)

    ttkb.Label(ventana_agregar, text="Tipo:").pack(pady=5)
    entry_tipo = ttkb.Entry(ventana_agregar)
    entry_tipo.pack(pady=5)

    ttkb.Label(ventana_agregar, text="Precio de Compra:").pack(pady=5)
    entry_precio_compra = ttkb.Entry(ventana_agregar)
    entry_precio_compra.pack(pady=5)

    ttkb.Label(ventana_agregar, text="Precio Venta:").pack(pady=5)
    entry_precio_venta = ttkb.Entry(ventana_agregar)
    entry_precio_venta.pack(pady=5)

    ttkb.Label(ventana_agregar, text="Cantidad:").pack(pady=5)
    entry_stock = ttkb.Entry(ventana_agregar)
    entry_stock.pack(pady=5)

    def agregar_producto():
        """
        Valida los datos ingresados, guarda el producto en la base de datos y actualiza la interfaz.
        """
        global ventana_tablas

        # Recoger y validar los datos ingresados
        nombre = entry_nombre.get().strip()
        tipo = entry_tipo.get().strip()
        try:
            precio_compra = float(entry_precio_compra.get())
            precio_venta = float(entry_precio_venta.get())
            cantidad = int(entry_stock.get())
        except ValueError:
            messagebox.showerror("Error", "Por favor, ingrese valores válidos en todos los campos.")
            return

        if not nombre or precio_compra <= 0 or precio_venta <= 0 or cantidad < 0:
            messagebox.showerror("Error", "Asegúrese de completar todos los campos con valores positivos.")
            return

        # Llamar a la función para guardar en la base de datos
        try:
            agregar_producto_db(nombre, tipo, precio_compra, precio_venta, cantidad)
        except Exception as e:
            messagebox.showerror("Error", f"No se pudo agregar el producto: {e}")
            return

        # Limpiar los campos
        entry_nombre.delete(0, tk.END)
        entry_tipo.delete(0, tk.END)
        entry_precio_compra.delete(0, tk.END)
        entry_precio_venta.delete(0, tk.END)
        entry_stock.delete(0, tk.END)

        # Actualizar la tabla de productos si está abierta
        if ventana_tablas is not None and ventana_tablas.winfo_exists():
            actualizar_tabla_productos()

        # Mostrar mensaje de éxito
        messagebox.showinfo("Éxito", f"Producto '{nombre}' agregado exitosamente.")
        ventana_agregar.destroy()

    # Botón para confirmar la acción
    ttkb.Button(ventana_agregar, text="Agregar Producto", command=agregar_producto).pack(pady=10)

def ventana_registrar_transaccion(rol):
    """
    Abre una ventana para registrar una transacción (compra o venta).
    El rol del usuario (admin o no) determina los tipos de transacción permitidos.
    """
    # Crear la ventana
    ventana_transaccion = ttkb.Toplevel()
    ventana_transaccion.title("Registrar Transacción")
    ventana_transaccion.geometry("600x300")

    # Etiquetas y entradas para los datos
    ttkb.Label(ventana_transaccion, text="Tipo de Transacción:").pack(pady=5)
    tipo_var = ttkb.StringVar(value="venta")  # Variable para el tipo de transacción

    # Opciones de transacción según el rol
    if rol == "admin":
        ttkb.Radiobutton(ventana_transaccion, text="Compra", variable=tipo_var, value="compra").pack(pady=5)
    ttkb.Radiobutton(ventana_transaccion, text="Venta", variable=tipo_var, value="venta").pack(pady=5)

    # Campos de entrada para el ID del producto y la cantidad
    ttkb.Label(ventana_transaccion, text="ID del Producto:").pack(pady=5)
    entry_id = ttkb.Entry(ventana_transaccion)
    entry_id.pack(pady=5)

    ttkb.Label(ventana_transaccion, text="Cantidad:").pack(pady=5)
    entry_cantidad = ttkb.Entry(ventana_transaccion)
    entry_cantidad.pack(pady=5)

    def registrar_transaccion():
        """
        Valida los datos ingresados y registra la transacción en la base de datos.
        """
        global ventana_tablas

        # Validar entradas del usuario
        try:
            producto_id = int(entry_id.get().strip())
            cantidad = int(entry_cantidad.get().strip())
            tipo = tipo_var.get()
        except ValueError:
            messagebox.showerror("Error", "El ID del producto y la cantidad deben ser números válidos.")
            return

        if cantidad <= 0:
            messagebox.showerror("Error", "La cantidad debe ser mayor a 0.")
            return

        # Registrar la transacción en la base de datos
        try:
            resultado = registrar_transaccion_db(producto_id, tipo, cantidad)  # Llamada a la función de base de datos
        except Exception as e:
            messagebox.showerror("Error", f"Error al registrar la transacción: {e}")
            return

        if resultado:
            # Mostrar mensaje de éxito
            messagebox.showinfo("Éxito", f"Transacción de tipo '{tipo}' registrada exitosamente.")

            # Limpiar los campos
            entry_id.delete(0, tk.END)
            entry_cantidad.delete(0, tk.END)
            tipo_var.set("venta")  # Reiniciar selección

            # Verificar stock bajo si es una venta
            if tipo == "venta":
                verificar_stock_bajo(umbral=5)

            # Actualizar tablas abiertas
            if ventana_tablas is not None and ventana_tablas.winfo_exists():
                actualizar_tabla_productos()
                actualizar_tabla_transacciones()
        else:
            messagebox.showerror("Error", "No se pudo registrar la transacción. Verifique los datos ingresados.")

        # Cerrar la ventana
        ventana_transaccion.destroy()

    # Botón para confirmar la transacción
    ttkb.Button(ventana_transaccion, text="Registrar Transacción", command=registrar_transaccion).pack(pady=10)

def ventana_eliminar_producto():
    """
    Crea una ventana para seleccionar el método de eliminación de un producto (por ID o por nombre).
    """
    ventana_eliminar = ttkb.Toplevel()
    ventana_eliminar.title("Eliminar Producto")
    ventana_eliminar.geometry("300x200")

    # Etiqueta para instrucción
    ttkb.Label(ventana_eliminar, text="Selecciona el método para eliminar:").pack(pady=10)

    # Botón para eliminar por ID
    ttkb.Button(
        ventana_eliminar, text="Eliminar por ID",
        command=lambda: ventana_eliminar_id(ventana_eliminar)
    ).pack(pady=5)

    # Botón para eliminar por nombre
    ttkb.Button(
        ventana_eliminar, text="Eliminar por Nombre",
        command=lambda: ventana_eliminar_nombre(ventana_eliminar)
    ).pack(pady=5)

    # Función para eliminar por ID
    def ventana_eliminar_id(parent):
        def eliminar():
            producto_id = entry_id.get().strip()
            if not producto_id.isdigit():
                messagebox.showerror("Error", "El ID debe ser un número.")
                return
            
            resultado = eliminar_producto_por_id(int(producto_id))  # Llama a la función de la base de datos
            if resultado:
                messagebox.showinfo("Éxito", f"Producto con ID {producto_id} eliminado correctamente.")
                parent.destroy()
                ventana_id.destroy()
            else:
                messagebox.showerror("Error", f"No se encontró un producto con ID {producto_id}.")

        ventana_id = ttkb.Toplevel()
        ventana_id.title("Eliminar por ID")
        ventana_id.geometry("300x150")

        ttkb.Label(ventana_id, text="Ingrese el ID del producto:").pack(pady=10)
        entry_id = ttkb.Entry(ventana_id)
        entry_id.pack(pady=5)

        ttkb.Button(ventana_id, text="Eliminar", command=eliminar).pack(pady=10)

    # Función para eliminar por nombre    
    def ventana_eliminar_nombre(parent):
        def eliminar():
            nombre = entry_nombre.get().strip()
            if not nombre:
                messagebox.showerror("Error", "Debe ingresar un nombre válido.")
                return

            resultado = eliminar_producto_por_nombre(nombre)  # Llama a la función de la base de datos
            if resultado:
                messagebox.showinfo("Éxito", f"Producto '{nombre}' eliminado correctamente.")
                parent.destroy()
                ventana_nombre.destroy()
            else:
                messagebox.showerror("Error", f"No se encontró un producto con nombre '{nombre}'.")

        ventana_nombre = ttkb.Toplevel()
        ventana_nombre.title("Eliminar por Nombre")
        ventana_nombre.geometry("300x150")

        ttkb.Label(ventana_nombre, text="Ingrese el nombre del producto:").pack(pady=10)
        entry_nombre = ttkb.Entry(ventana_nombre)
        entry_nombre.pack(pady=5)

        ttkb.Button(ventana_nombre, text="Eliminar", command=eliminar).pack(pady=10)

def actualizar_tabla_productos():
    """
    Actualiza la tabla de productos si está activa, obteniendo los datos de la base de datos.
    """
    global tabla_productos

    # Verifica si la tabla existe y está activa
    if 'tabla_productos' in globals() and tabla_productos.winfo_exists():
        try:
            # Limpiar la tabla de productos
            tabla_productos.delete(*tabla_productos.get_children())

            # Obtener datos desde la base de datos
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM productos")
            productos = cursor.fetchall()

            # Insertar los productos en la tabla
            for producto in productos:
                tabla_productos.insert("", "end", values=producto)
        except Exception as e:
            print(f"Error al actualizar la tabla de productos: {e}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals():
                conexion.close()
    else:
        print("La tabla de productos no está activa o no existe.")

def actualizar_tabla_transacciones():
    """
    Actualiza la tabla de transacciones si está activa, obteniendo los datos de la base de datos.
    """
    global tabla_transacciones

    # Verifica si la tabla existe y está activa
    if 'tabla_transacciones' in globals() and tabla_transacciones.winfo_exists():
        try:
            # Limpiar la tabla de transacciones
            tabla_transacciones.delete(*tabla_transacciones.get_children())

            # Obtener datos desde la base de datos
            conexion = obtener_conexion()
            cursor = conexion.cursor()
            cursor.execute("SELECT * FROM transacciones")
            transacciones = cursor.fetchall()

            # Insertar las transacciones en la tabla
            for transaccion in transacciones:
                tabla_transacciones.insert("", "end", values=transaccion)
        except Exception as e:
            print(f"Error al actualizar la tabla de transacciones: {e}")
        finally:
            # Asegúrate de cerrar la conexión
            if 'conexion' in locals():
                conexion.close()
    else:
        print("La tabla de transacciones no está activa o no existe.")

def abrir_ventana_tablas():
    """
    Abre una ventana con las tablas de productos y transacciones.
    Si la ventana ya está abierta, la trae al frente.
    """
    global ventana_tablas, tabla_productos, tabla_transacciones

    # Verificar si la ventana ya está abierta
    if ventana_tablas is not None and ventana_tablas.winfo_exists():
        ventana_tablas.lift()
        return

    # Crear nueva ventana
    ventana_tablas = ttkb.Toplevel()
    ventana_tablas.title("Tablas de Productos y Transacciones")
    ventana_tablas.geometry("1280x720")

    # Configuración para eliminar referencias al cerrar la ventana
    def on_close():
        """
        Limpia referencias globales al cerrar la ventana.
        """
        global tabla_productos, tabla_transacciones, ventana_tablas
        tabla_productos = None
        tabla_transacciones = None
        ventana_tablas.destroy()
        ventana_tablas = None

    ventana_tablas.protocol("WM_DELETE_WINDOW", on_close)

    # Configuración de estilos para las tablas
    estilo = ttkb.Style()
    estilo.configure(
        "Treeview",
        font=("Arial", 10),
        rowheight=25,
        background=estilo.colors.light,
        foreground=estilo.colors.dark,
        fieldbackground=estilo.colors.light,
    )
    estilo.configure(
        "Treeview.Heading",
        font=("Arial", 11, "bold"),
        background=estilo.colors.primary,
        foreground="white",
        anchor="center",
    )

    # Crear tabla de productos
    tabla_productos = crear_tabla(
        ventana_tablas,
        columnas=["ID", "Nombre", "Tipo", "Compra", "Venta", "Stock"],
        anchos={"ID": 50, "Nombre": 100, "Tipo": 80, "Compra": 80, "Venta": 80, "Stock": 40},
        titulo="Productos",
    )

    # Crear tabla de transacciones
    tabla_transacciones = crear_tabla(
        ventana_tablas,
        columnas=["ID", "Tipo", "Producto ID", "Cantidad", "Fecha", "Total"],
        anchos={"ID": 50, "Tipo": 60, "Producto ID": 50, "Cantidad": 80, "Fecha": 100, "Total": 80},
        titulo="Transacciones",
    )

    # Cargar datos
    actualizar_tabla_productos()
    actualizar_tabla_transacciones()
    verificar_stock_bajo(umbral=5)


def crear_tabla(parent, columnas, anchos, titulo):
    """
    Crea una tabla Treeview configurada con encabezados y anchos específicos.

    Args:
        parent: Widget padre donde se colocará la tabla.
        columnas: Lista de nombres de las columnas.
        anchos: Diccionario con anchos de las columnas.
        titulo: Título de la tabla (opcional, para claridad).

    Returns:
        ttkb.Treeview: Objeto tabla configurado.
    """
    tabla = ttkb.Treeview(parent, columns=columnas, show="headings")
    for columna in columnas:
        tabla.heading(columna, text=columna, anchor="center")
        tabla.column(columna, anchor="center", width=anchos.get(columna, 80))
    tabla.pack(fill="both", expand=True, padx=10, pady=10)
    return tabla

def confirmar_reinicio():
    """
    Confirma con el usuario si desea reiniciar las transacciones, mostrando un resumen de totales
    antes de realizar la acción. Permite guardar un reporte PDF antes del reinicio.
    """
    # Calcular totales
    total_ventas, total_compras, total_ganancia, porcentaje_ganancia = calcular_totales()

    # Mensaje de confirmación
    mensaje = (
        f"Antes de reiniciar las transacciones, aquí tienes los totales:\n"
        f"- Total de Ventas: ${total_ventas:.2f}\n"
        f"- Total de Compras: ${total_compras:.2f}\n"
        f"- Total de Ganancia: ${total_ganancia:.2f}\n"
        f"- Porcentaje de Ganancia: {porcentaje_ganancia:.2f}%\n\n"
        f"¿Estás seguro de que quieres reiniciar todas las transacciones? Esta acción no se puede deshacer."
    )

    # Confirmar acción con el usuario
    respuesta = messagebox.askyesno("Confirmación", mensaje)
    if respuesta:
        # Solicitar archivo para guardar el reporte
        archivo = filedialog.asksaveasfilename(
            defaultextension=".pdf",
            filetypes=[("Archivos PDF", "*.pdf")],
            title="Guardar reporte antes de reiniciar"
        )
        
        if archivo:  # Verificar que se haya seleccionado un archivo
            try:
                # Generar el reporte PDF
                generar_reporte_pdf(archivo)
                # Reiniciar transacciones
                reiniciar_transacciones()
                # Notificar éxito
                messagebox.showinfo("Éxito", "Las transacciones han sido reiniciadas y el reporte se ha guardado correctamente.")
            except Exception as e:
                # Manejar errores durante el guardado o reinicio
                messagebox.showerror("Error", f"Ocurrió un error al guardar el reporte o reiniciar las transacciones.\n\n{str(e)}")
        else:
            # Si no se seleccionó archivo, cancelar operación
            messagebox.showinfo("Cancelado", "La operación fue cancelada. Las transacciones no se han reiniciado.")

def calcular_totales():
    """
    Calcula los totales de ventas, compras, ganancias y el porcentaje de ganancia
    a partir de las transacciones almacenadas en la base de datos.

    Returns:
        tuple: (total_ventas, total_compras, total_ganancias, porcentaje_ganancia)
    """
    try:
        # Conexión a la base de datos
        conexion = obtener_conexion()
        cursor = conexion.cursor()

        # Total de ventas
        cursor.execute("SELECT SUM(total) FROM transacciones WHERE tipo = 'venta';")
        total_ventas = cursor.fetchone()[0] or 0

        # Total de compras
        cursor.execute("SELECT SUM(total) FROM transacciones WHERE tipo = 'compra';")
        total_compras = cursor.fetchone()[0] or 0

        # Ganancias totales
        total_ganancias = total_ventas - total_compras

        # Porcentaje de ganancia
        porcentaje_ganancia = (
            ((total_ventas - total_compras) / total_compras) * 100 if total_compras > 0 else 0
        )
    except Exception as e:
        # Manejo de errores
        print(f"Error al calcular los totales: {e}")
        total_ventas = total_compras = total_ganancias = porcentaje_ganancia = 0
    finally:
        # Asegurarse de cerrar la conexión
        conexion.close()

    return total_ventas, total_compras, total_ganancias, porcentaje_ganancia

def ventana_modificar_producto():
    """
    Crea una ventana para modificar los valores de compra y venta de un producto en la base de datos.
    """
    ventana_modificar = ttkb.Toplevel()
    ventana_modificar.title("Modificar Producto")
    ventana_modificar.geometry("600x300")

    # Etiquetas y campos de entrada para los datos
    ttkb.Label(ventana_modificar, text="ID del Producto:").pack(pady=5)
    entry_id = ttkb.Entry(ventana_modificar)
    entry_id.pack(pady=5)

    ttkb.Label(ventana_modificar, text="Nuevo Valor de Compra:").pack(pady=5)
    entry_compra = ttkb.Entry(ventana_modificar)
    entry_compra.pack(pady=5)

    ttkb.Label(ventana_modificar, text="Nuevo Valor de Venta:").pack(pady=5)
    entry_venta = ttkb.Entry(ventana_modificar)
    entry_venta.pack(pady=5)

    def registrar_modificacion():
        """
        Valida los datos de entrada y registra las modificaciones en la base de datos.
        """
        global ventana_tablas

        try:
            producto_id = int(entry_id.get())
            valor_compra = float(entry_compra.get())
            valor_venta = float(entry_venta.get())
        except ValueError:
            messagebox.showerror("Error", "El ID y los valores deben ser numéricos y válidos.")
            return

        if valor_compra <= 0 or valor_venta <= 0:
            messagebox.showerror("Error", "Los valores de compra y/o venta deben ser mayores a 0.")
            return

        # Llamar a la función que realiza el registro en la base de datos
        resultado = registrar_modificacion_db(producto_id, valor_compra, valor_venta)
        if resultado:
            messagebox.showinfo("Éxito", "Modificación registrada exitosamente.")
            # Limpiar los campos de entrada
            entry_id.delete(0, tk.END)
            entry_compra.delete(0, tk.END)
            entry_venta.delete(0, tk.END)

            # Actualizar las tablas si están abiertas
            if ventana_tablas is not None and ventana_tablas.winfo_exists():
                actualizar_tabla_productos()
                actualizar_tabla_transacciones()
        else:
            messagebox.showerror(
                "Error",
                "No se pudo registrar las modificaciones. Verifique que el ID del producto sea válido."
            )

        # Cerrar la ventana de modificación
        ventana_modificar.destroy()

    # Botón de confirmación
    ttkb.Button(
        ventana_modificar,
        text="Registrar Modificación",
        command=registrar_modificacion
    ).pack(pady=10)

def exportar_reporte():
    """
    Genera un reporte de transacciones en formato Excel o PDF según la elección del usuario.
    """
    # Mostrar cuadro de diálogo para elegir formato
    respuesta = messagebox.askquestion(
        "Generar Reporte",
        (
            "¿En qué formato desea generar el reporte de transacciones?\n\n"
            "Presione 'Sí' para Excel o 'No' para PDF."
        ),
    )

    if respuesta not in ("yes", "no"):
        return  # Si el usuario cierra el cuadro de diálogo, salir de la función

    # Configurar extensión y tipo de archivo según la elección del usuario
    extension = ".xlsx" if respuesta == "yes" else ".pdf"
    tipo_archivo = [("Archivos Excel", "*.xlsx"), ("Archivos PDF", "*.pdf")]

    # Mostrar diálogo para guardar el archivo
    archivo = filedialog.asksaveasfilename(
        defaultextension=extension,
        filetypes=tipo_archivo,
    )

    if not archivo:
        return  # Si el usuario cancela, no hacer nada

    # Generar el reporte según el formato elegido
    try:
        if respuesta == "yes":
            generar_reporte_excel(archivo)
        else:
            generar_reporte_pdf(archivo)

        messagebox.showinfo(
            "Reporte Generado",
            f"El reporte de transacciones se ha generado correctamente en {archivo}.",
        )
    except Exception as e:
        messagebox.showerror(
            "Error al Generar Reporte",
            f"Ocurrió un error al generar el reporte:\n{e}",
        )

if __name__ == "__main__":
    rol_actual = None # Variable global para guardar el rol actual
    ventana_tablas = None # Variable global de la tabla al iniciar 

    crear_base_datos()
    insertar_usuario_admin()
    interfaz_principal(rol_actual)