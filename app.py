from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import sqlite3
import hashlib
from datetime import datetime
import os

app = Flask(__name__)
app.secret_key = 'clave_secreta_muy_segura'

# Configuración de la base de datos
DATABASE = 'InventarioBD.db'

def get_db_connection():
    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn

# Función para encriptar contraseñas
def encrypt_password(password):
    return hashlib.md5(password.encode()).hexdigest()


@app.route('/index')
def index():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    conn = get_db_connection()
    total_productos = conn.execute('SELECT COUNT(*) as count FROM productos').fetchone()['count']
    total_almacenes = conn.execute('SELECT COUNT(*) as count FROM almacenes').fetchone()['count']
    conn.close()

    return render_template('index.html',
                           total_productos=total_productos,
                           total_almacenes=total_almacenes)


@app.route('/productos')
def productos():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    # Obtener parámetros de filtro (incluyendo los nuevos)
    nombre_filter = request.args.get('nombre', '')
    departamento_filter = request.args.get('departamento', '')
    almacen_filter = request.args.get('almacen', '')
    precio_min = request.args.get('precio_min', '')
    precio_max = request.args.get('precio_max', '')
    cantidad_min = request.args.get('cantidad_min', '')
    cantidad_max = request.args.get('cantidad_max', '')
    usuario_modifico = request.args.get('usuario_modifico', '')
    fecha_modificacion_desde = request.args.get('fecha_modificacion_desde', '')
    fecha_modificacion_hasta = request.args.get('fecha_modificacion_hasta', '')

    conn = get_db_connection()

    # Construir consulta con filtros
    query = '''
        SELECT 
            p.id, p.nombre, p.departamento, p.precio, p.cantidad, p.almacen,
            p.fecha_hora_creacion, p.fecha_hora_ultima_modificacion, p.ultimo_usuario_en_modificar,
            a.nombre as almacen_nombre 
        FROM productos p 
        LEFT JOIN almacenes a ON p.almacen = a.id 
        WHERE 1=1
    '''
    params = []

    if nombre_filter:
        query += ' AND p.nombre LIKE ?'
        params.append(f'%{nombre_filter}%')

    if departamento_filter:
        query += ' AND p.departamento LIKE ?'
        params.append(f'%{departamento_filter}%')

    if almacen_filter:
        query += ' AND p.almacen = ?'
        params.append(int(almacen_filter))

    if precio_min:
        query += ' AND p.precio >= ?'
        params.append(float(precio_min))

    if precio_max:
        query += ' AND p.precio <= ?'
        params.append(float(precio_max))

    if cantidad_min:
        query += ' AND p.cantidad >= ?'
        params.append(int(cantidad_min))

    if cantidad_max:
        query += ' AND p.cantidad <= ?'
        params.append(int(cantidad_max))

    if usuario_modifico:
        query += ' AND p.ultimo_usuario_en_modificar LIKE ?'
        params.append(f'%{usuario_modifico}%')

    if fecha_modificacion_desde:
        query += ' AND DATE(p.fecha_hora_ultima_modificacion) >= ?'
        params.append(fecha_modificacion_desde)

    if fecha_modificacion_hasta:
        query += ' AND DATE(p.fecha_hora_ultima_modificacion) <= ?'
        params.append(fecha_modificacion_hasta)

    query += ' ORDER BY p.nombre'

    productos = conn.execute(query, params).fetchall()
    almacenes = conn.execute('SELECT * FROM almacenes ORDER BY nombre').fetchall()
    conn.close()

    return render_template('productos.html', productos=productos, almacenes=almacenes)


@app.route('/agregar_producto', methods=['GET', 'POST'])
def agregar_producto():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if session['usuario_rol'] not in ['ADMIN', 'PRODUCTOS']:
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('productos'))

    conn = get_db_connection()
    almacenes = conn.execute('SELECT * FROM almacenes ORDER BY nombre').fetchall()

    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form.get('departamento', '')
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        almacen_id = int(request.form['almacen'])

        try:
            # ✅ CAPTURAR FECHA Y USUARIO ACTUAL
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            usuario_actual = session['usuario_nombre']

            conn.execute('''
                INSERT INTO productos 
                (nombre, departamento, precio, cantidad, almacen, 
                 fecha_hora_creacion, ultimo_usuario_en_modificar)
                VALUES (?, ?, ?, ?, ?, ?, ?)
            ''', (nombre, departamento, precio, cantidad, almacen_id,
                  fecha_actual, usuario_actual))
            conn.commit()
            flash('Producto agregado exitosamente', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            flash(f'Error al agregar producto: {str(e)}', 'error')
        finally:
            conn.close()

    return render_template('agregar_producto.html', almacenes=almacenes)

@app.route('/editar_producto/<int:id>', methods=['GET', 'POST'])
def editar_producto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if session['usuario_rol'] not in ['ADMIN', 'PRODUCTOS']:
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('productos'))

    conn = get_db_connection()

    if request.method == 'POST':
        nombre = request.form['nombre']
        departamento = request.form.get('departamento', '')
        precio = float(request.form['precio'])
        cantidad = int(request.form['cantidad'])
        almacen_id = int(request.form['almacen'])

        try:
            # ✅ CAPTURAR FECHA Y USUARIO ACTUAL
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            usuario_actual = session['usuario_nombre']

            conn.execute('''
                UPDATE productos 
                SET nombre = ?, departamento = ?, precio = ?, cantidad = ?, almacen = ?,
                    fecha_hora_ultima_modificacion = ?, ultimo_usuario_en_modificar = ?
                WHERE id = ?
            ''', (nombre, departamento, precio, cantidad, almacen_id,
                  fecha_actual, usuario_actual, id))
            conn.commit()
            flash('Producto actualizado exitosamente', 'success')
            return redirect(url_for('productos'))
        except Exception as e:
            flash(f'Error al actualizar producto: {str(e)}', 'error')

    producto = conn.execute('SELECT * FROM productos WHERE id = ?', (id,)).fetchone()
    almacenes = conn.execute('SELECT * FROM almacenes ORDER BY nombre').fetchall()
    conn.close()

    if not producto:
        flash('Producto no encontrado', 'error')
        return redirect(url_for('productos'))

    return render_template('editar_producto.html', producto=producto, almacenes=almacenes)

@app.route('/eliminar_producto/<int:id>', methods=['POST'])
def eliminar_producto(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if session['usuario_rol'] not in ['ADMIN', 'PRODUCTOS']:
        return jsonify({'success': False, 'message': 'No tienes permisos para esta acción'})

    conn = get_db_connection()
    try:
        # ✅ OPCIONAL: Guardar registro de quién eliminó (si quieres auditoría de eliminaciones)
        print(f"Usuario {session['usuario_nombre']} eliminó el producto ID: {id}")

        conn.execute('DELETE FROM productos WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Producto eliminado exitosamente'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': f'Error al eliminar producto: {str(e)}'})


@app.route('/almacenes')
def almacenes():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    # Obtener parámetros de filtro (incluyendo los nuevos)
    nombre_filter = request.args.get('nombre', '')
    usuario_modifico = request.args.get('usuario_modifico', '')
    fecha_modificacion_desde = request.args.get('fecha_modificacion_desde', '')
    fecha_modificacion_hasta = request.args.get('fecha_modificacion_hasta', '')

    conn = get_db_connection()

    # Construir consulta con filtros
    query = '''
        SELECT 
            id, nombre,
            fecha_hora_creacion, fecha_hora_ultima_modificacion, ultimo_usuario_en_modificar
        FROM almacenes 
        WHERE 1=1
    '''
    params = []

    if nombre_filter:
        query += ' AND nombre LIKE ?'
        params.append(f'%{nombre_filter}%')

    if usuario_modifico:
        query += ' AND ultimo_usuario_en_modificar LIKE ?'
        params.append(f'%{usuario_modifico}%')

    if fecha_modificacion_desde:
        query += ' AND DATE(fecha_hora_ultima_modificacion) >= ?'
        params.append(fecha_modificacion_desde)

    if fecha_modificacion_hasta:
        query += ' AND DATE(fecha_hora_ultima_modificacion) <= ?'
        params.append(fecha_modificacion_hasta)

    query += ' ORDER BY nombre'

    almacenes = conn.execute(query, params).fetchall()
    conn.close()

    return render_template('almacenes.html', almacenes=almacenes)


@app.route('/agregar_almacen', methods=['GET', 'POST'])
def agregar_almacen():
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if session['usuario_rol'] not in ['ADMIN', 'ALMACENES']:
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('almacenes'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        # Solo nombre, sin capacidad ni descripción

        conn = get_db_connection()
        try:
            # ✅ CAPTURAR FECHA Y USUARIO ACTUAL (solo nombre)
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            usuario_actual = session['usuario_nombre']

            conn.execute('''
                INSERT INTO almacenes 
                (nombre, fecha_hora_creacion, ultimo_usuario_en_modificar)
                VALUES (?, ?, ?)
            ''', (nombre, fecha_actual, usuario_actual))
            conn.commit()
            flash('Almacén agregado exitosamente', 'success')
            return redirect(url_for('almacenes'))
        except Exception as e:
            flash(f'Error al agregar almacén: {str(e)}', 'error')
        finally:
            conn.close()

    return render_template('agregar_almacen.html')

@app.route('/editar_almacen/<int:id>', methods=['GET', 'POST'])
def editar_almacen(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if session['usuario_rol'] not in ['ADMIN', 'ALMACENES']:
        flash('No tienes permisos para esta acción', 'error')
        return redirect(url_for('almacenes'))

    conn = get_db_connection()

    if request.method == 'POST':
        nombre = request.form['nombre']
        # Solo nombre, sin capacidad ni descripción

        try:
            # ✅ CAPTURAR FECHA Y USUARIO ACTUAL (solo nombre)
            fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
            usuario_actual = session['usuario_nombre']

            conn.execute('''
                UPDATE almacenes 
                SET nombre = ?,
                    fecha_hora_ultima_modificacion = ?, ultimo_usuario_en_modificar = ?
                WHERE id = ?
            ''', (nombre, fecha_actual, usuario_actual, id))
            conn.commit()
            flash('Almacén actualizado exitosamente', 'success')
            return redirect(url_for('almacenes'))
        except Exception as e:
            flash(f'Error al actualizar almacén: {str(e)}', 'error')

    almacen = conn.execute('SELECT * FROM almacenes WHERE id = ?', (id,)).fetchone()
    conn.close()

    if not almacen:
        flash('Almacén no encontrado', 'error')
        return redirect(url_for('almacenes'))

    return render_template('editar_almacen.html', almacen=almacen)


@app.route('/eliminar_almacen/<int:id>', methods=['POST'])
def eliminar_almacen(id):
    if 'usuario_id' not in session:
        return redirect(url_for('login'))

    if session['usuario_rol'] not in ['ADMIN', 'ALMACENES']:
        return jsonify({'success': False, 'message': 'No tienes permisos para esta acción'})

    # Verificar si hay productos en este almacén
    conn = get_db_connection()
    productos_count = conn.execute('SELECT COUNT(*) as count FROM productos WHERE almacen = ?', (id,)).fetchone()[
        'count']

    if productos_count > 0:
        conn.close()
        return jsonify({'success': False,
                        'message': f'No se puede eliminar el almacén porque tiene {productos_count} producto(s) asociado(s)'})

    try:
        conn.execute('DELETE FROM almacenes WHERE id = ?', (id,))
        conn.commit()
        conn.close()
        return jsonify({'success': True, 'message': 'Almacén eliminado exitosamente'})
    except Exception as e:
        conn.close()
        return jsonify({'success': False, 'message': f'Error al eliminar almacén: {str(e)}'})


@app.route('/', methods=['GET', 'POST'])
@app.route('/login', methods=['GET', 'POST'])
def login():
    # ✅ Si el usuario ya está logueado, redirigir al index
    if 'usuario_id' in session:
        return redirect(url_for('index'))

    if request.method == 'POST':
        nombre = request.form['nombre']
        password = request.form['password']
        password_encriptada = encrypt_password(password)

        conn = get_db_connection()
        usuario = conn.execute(
            'SELECT * FROM usuarios WHERE nombre = ? AND password = ?',
            (nombre, password_encriptada)
        ).fetchone()
        conn.close()

        if usuario:
            # Actualizar último inicio de sesión
            conn = get_db_connection()
            conn.execute(
                'UPDATE usuarios SET fecha_hora_ultimo_inicio = ? WHERE id = ?',
                (datetime.now(), usuario['id'])
            )
            conn.commit()
            conn.close()

            session['usuario_id'] = usuario['id']
            session['usuario_nombre'] = usuario['nombre']
            session['usuario_rol'] = usuario['rol']
            return redirect(url_for('index'))
        else:
            flash('Credenciales incorrectas', 'error')

    return render_template('login.html')


@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True)
