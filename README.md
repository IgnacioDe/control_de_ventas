# Aplicación de Gestión de Ventas de Productos

## Descripción

Esta aplicación está diseñada para gestionar compras y ventas de Productos, proporcionando cálculos automáticos de gastos, ganancias y porcentajes al final del mes. Es ideal para pequeños negocios que buscan optimizar su administración diaria.

La aplicación incluye funcionalidades como:

- Registro de compras y ventas.
- Autenticación de usuarios (administrador y usuarios regulares).
- Generación de reportes de ganancias.
- Interfaz gráfica intuitiva.

## Requisitos

### Software

- Python 3.10 o superior
- SQLite3 (incluido con Python)

### Librerías de Python

Asegúrate de instalar las siguientes librerías:

```bash
pip install tkinter pillow
pip install ttkbootstrap pandas fpdf
```

## Estructura del Proyecto

```
control_de_ventas/
|-- crear_bd.py     # Conexión y operaciones con la base de datos
|-- db_manager.py   # Gestión de la base de datos
|-- gestion_bebidas.db  # Archivo de base de datos generado automáticamente
|-- interfaz.py       # Interfaz gráfica principal
|-- productos.py    # Gestión de productos
|-- README.md         # Documento actual
|-- transacciones.py    # Gestión de transacciones
```

## Instalación y Uso

### 1. Clonar el repositorio

```bash
git clone <URL_DEL_REPOSITORIO>
cd control_de_ventas
```

### 2. Crear el ejecutable

Usa PyInstaller para generar un archivo ejecutable:

```bash
pyinstaller --onefile --noconsole --icon=icono.ico --name "Gestion de Ventas" interfaz.py
```

El ejecutable estará disponible en la carpeta `dist`.

### 3. Ejecutar la aplicación

Puedes iniciar la aplicación desde el ejecutable generado o ejecutando directamente el archivo `interfaz.py`:

```bash
python interfaz.py
```

### 4. Primer inicio

En el primer inicio:

- Se crea la base de datos automáticamente.
- Un usuario administrador predeterminado es generado:
  - **Usuario**: admin
  - **Contraseña**: admin123

Recomendamos cambiar las credenciales del administrador después del primer inicio.

## Características del Usuario Administrador

- Acceso completo a todas las funciones de la aplicación.
- Puede crear, editar y eliminar productos.
- Gestión de usuarios.
- Visualización y exportación de reportes detallados.

## Resolución de Problemas

### Error: `no such table: usuarios`

Este error ocurre si las tablas de la base de datos no se crean correctamente. Asegúrate de:

1. Eliminar cualquier archivo previo de base de datos (`base_de_datos.db`).
2. Reiniciar la aplicación para que las tablas se generen automáticamente.

### Error al ejecutar el ejecutable

Si recibes un error relacionado con virus o software no deseado al generar el ejecutable, asegúrate de:

- Deshabilitar temporalmente tu antivirus para el proceso de creación.
- Utilizar un entorno limpio y actualizado de Python.

## Autor

Desarrollado por Ignacio Denis. Si tienes preguntas o sugerencias, no dudes en contactarme.

---

¡Gracias por usar la aplicación de Gestión de Ventas de Bebidas!
