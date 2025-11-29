# Inventario con Flask
### Sistema de gestion de inventario con flask
### Maestro: Jose Luis Aguilera Luzania
### Alumno: Anduaga Nieblas Sebastian
![imagen no esta funcionando.](/static/imagenes/logoUnison.png)
## Características

- Autenticación segura con roles (ADMIN, PRODUCTOS, ALMACENES)

- Gestión completa de productos y almacenes

- Filtros avanzados de búsqueda y fechas

- Auditoría completa de cambios y usuarios

- Interfaz responsive con diseño Universidad de Sonora

- Validaciones y confirmaciones de eliminación</p>

## Tecnologías

- Backend: Flask, SQLite

- Frontend: HTML5, CSS3, JavaScript

- Estilos: CSS personalizado con colores UNISON

- Base de datos: SQLite con auditoría integrada

# VISTAS Y FUNCIONALIDADES

## Vista: Login (login.html)
![imagen no esta funcionando.](/static/imagenes/login.png)
### Funcionalidades:

- Autenticación segura con encriptación MD5

- Validación de credenciales en tiempo real

- Redirección automática si ya está autenticado

- Diseño con colores institucionales UNISON

- Botón externo de acceso para mejor UX

### Características de seguridad:

- No permite registro de nuevos usuarios

- No mantiene sesiones abiertas

- Actualiza timestamp de último acceso

## Vista: Inicio (index.html)
![imagen no esta funcionando.](/static/imagenes/inicio.png)
### Funcionalidades:

- Dashboard principal con logo institucional

- Navegación rápida mediante botones grandes

- Información del desarrollador

- Barra de navegación con rol de usuario

- Diseño responsive y profesional

### Elementos principales:

- Logo de la empresa/institución

- Botones de acceso rápido (Inicio, Productos, Almacenes)

- Información de auditoría visible

## Vista: Productos (productos.html)
![imagen no esta funcionando.](/static/imagenes/productos1.png)
![imagen no esta funcionando.](/static/imagenes/productos2.png)
### Funcionalidades principales:

#### Sistema de filtros avanzados:

  - Búsqueda por nombre y departamento

  - Filtro por almacén específico

  - Rangos de precio (mínimo y máximo)

  - Rangos de cantidad (mínimo y máximo)

  - Filtro por fechas de modificación

  - Búsqueda por último usuario que modificó

####  Tabla interactiva:

- Scroll vertical y horizontal

- Selección de filas con click

- Doble-click para edición rápida

- Cabecera fija al hacer scroll

- Columnas de auditoría visibles

#### Sistema de acciones:

  - Botones debajo de la tabla (Agregar, Editar, Eliminar)

  - Botones se habilitan solo con elemento seleccionado

  - Confirmación de eliminación con ventana emergente

  - Botón "Regresar" para navegación
#### Campos mostrados:

  - ID, Nombre, Departamento, Precio, Cantidad, Almacén

  - Fecha creación, Última modificación, Último usuario

## Vista: Almacenes (almacenes.html)
![imagen no esta funcionando.](/static/imagenes/almacenes1.png)
![imagen no esta funcionando.](/static/imagenes/almacenes2.png)
### Funcionalidades principales:

#### Sistema de filtros:

   - Búsqueda por nombre

   - Filtro por fechas de modificación

   - Búsqueda por último usuario que modificó

#### Tabla interactiva:

- Mismo sistema de selección que productos

- Scroll integrado

- Doble-click para edición rápida

#### Sistema de acciones:

- Botones debajo de la tabla

- Validación antes de eliminar (verifica productos asociados)

- Confirmación de eliminación

- Campos mostrados:

- ID, Nombre, Fecha creación, Última modificación, Último usuario

## Vista: Agregar Producto (agregar_producto.html)
![imagen no esta funcionando.](/static/imagenes/agregarProducto.png)
### Funcionalidades:

- Formulario de creación con validaciones
 
- Campos requeridos marcados con asterisco

- Selección de almacén desde dropdown

- Placeholders informativos

- Botones de acción (Guardar, Cancelar)

- Captura automática de usuario y timestamp

#### Campos del formulario:

- Nombre* (requerido)

- Departamento

- Precio* (requerido, numérico)

- Cantidad* (requerido, entero)

- Almacén* (requerido, dropdown)

## Vista: Editar Producto (editar_producto.html)
![imagen no esta funcionando.](/static/imagenes/editarProducto.png)
### Funcionalidades:

- Formulario pre-cargado con datos existentes

- Sección de auditoría visible

- Actualización automática de timestamps

- Registro del usuario que modificó

- Mismas validaciones que agregar

### Información de auditoria mostrada:

- Fecha de creación

- Última modificación (si existe)

- Último usuario que modificó


## Vista: Agregar Almacén (agregar_almacen.html)
![imagen no esta funcionando.](/static/imagenes/agregarAlmacen.png)
### Funcionalidades:

- Formulario simple y limpio

- Solo campo nombre (requerido)

- Validaciones de entrada

- Captura automática de auditoría

## Vista: Editar Almacén (editar_almacen.html)
![imagen no esta funcionando.](/static/imagenes/editarAlmacen.png)
### Funcionalidades:

- Formulario de edición minimalista

- Información de auditoría completa

- Actualización de usuario y timestamp

## Funcion de eliminado
![imagen no esta funcionando.](/static/imagenes/eliminarProducto1.png)
![imagen no esta funcionando.](/static/imagenes/eliminarProducto2.png)

- Permite eliminar de manera permanente datos de la tabla productos y almacenes
- Una ventana emergente aparecera para confirmar la eliminacion de los datos

## SISTEMA DE ROLES Y PERMISOS
### Rol ADMIN:
- Acceso completo a todas las funcionalidades

- Gestión de productos y almacenes

- Eliminación de registros

### Rol PRODUCTOS:
- Solo gestión de productos

- Sin acceso a gestión de almacenes

- Agregar, editar y eliminar productos

### Rol ALMACENES:
- Solo gestión de almacenes

- Sin acceso a gestión de productos

- Agregar, editar y eliminar almacenes

## ESTRUCTURA DE LA BASE DE DATOS
### Tabla: usuarios
- id (INTEGER PRIMARY KEY)

- nombre (TEXT UNIQUE NOT NULL)

- password (TEXT NOT NULL) - Encriptado MD5

- fecha_hora_ultimo_inicio (DATETIME)

- rol (TEXT CHECK) - ADMIN, PRODUCTOS, ALMACENES

### Tabla: productos
- id (INTEGER PRIMARY KEY)

- nombre (TEXT NOT NULL)

- departamento (TEXT)

- precio (REAL NOT NULL)

- cantidad (INTEGER NOT NULL)

- almacen (INTEGER FOREIGN KEY)

- fecha_hora_creacion (DATETIME)

- fecha_hora_ultima_modificacion (DATETIME)

- ultimo_usuario_en_modificar (TEXT)

### Tabla: almacenes
- id (INTEGER PRIMARY KEY)

- nombre (TEXT NOT NULL)

- fecha_hora_creacion (DATETIME)

- fecha_hora_ultima_modificacion (DATETIME)

- ultimo_usuario_en_modificar (TEXT)

### Colores institucionales UNISON:

- 🔵 Azul Unison: #00529e

- 🔵 Azul Oscuro: #015294

- 🟡 Dorado Unison: #f8bb00

- 🟡 Dorado Oscuro: #d99e30

## Características de diseño:
- Tipografía Segoe UI en todos los textos

- Bordes redondeados de 4px

- Diseño responsive (mobile-first)

- Efectos hover y transiciones suaves

- Scrollbars personalizados

- Tablas con cabeceras fijas

- Botones con gradientes y efectos



