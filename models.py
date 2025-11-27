import sqlite3
import hashlib
from datetime import datetime


def init_db():
    conn = sqlite3.connect('InventarioBD.db')
    cursor = conn.cursor()

    print("🔄 Inicializando base de datos...")

    # Crear tabla de usuarios si no existe
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS usuarios (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            nombre TEXT UNIQUE NOT NULL,
            password TEXT NOT NULL,
            fecha_hora_ultimo_inicio DATETIME,
            rol TEXT CHECK(rol IN ('ADMIN', 'PRODUCTOS', 'ALMACENES')) NOT NULL
        )
    ''')
    print("✅ Tabla 'usuarios' creada/verificada")

    # Crear usuarios base
    usuarios = [
        ('ADMIN', 'admin23', 'ADMIN'),
        ('PRODUCTOS', 'productos19', 'PRODUCTOS'),
        ('ALMACENES', 'almacenes11', 'ALMACENES')
    ]

    for nombre, password, rol in usuarios:
        password_encriptada = hashlib.md5(password.encode()).hexdigest()
        cursor.execute('''
            INSERT OR IGNORE INTO usuarios (nombre, password, rol) 
            VALUES (?, ?, ?)
        ''', (nombre, password_encriptada, rol))
    print("✅ Usuarios base creados")

    # Verificar y agregar columnas faltantes a productos (SIN DEFAULT)
    columnas_productos = [
        ('fecha_hora_creacion', 'DATETIME'),  # SIN DEFAULT
        ('fecha_hora_ultima_modificacion', 'DATETIME'),
        ('ultimo_usuario_en_modificar', 'TEXT'),
        ('departamento', 'TEXT')
    ]

    print("🔄 Verificando columnas de 'productos'...")
    cursor.execute("PRAGMA table_info(productos)")
    columnas_existentes = [col[1] for col in cursor.fetchall()]
    print(f"Columnas existentes en productos: {columnas_existentes}")

    for columna, tipo in columnas_productos:
        if columna not in columnas_existentes:
            try:
                cursor.execute(f'ALTER TABLE productos ADD COLUMN {columna} {tipo}')
                print(f"✅ Columna '{columna}' agregada a productos")
            except Exception as e:
                print(f"❌ Error agregando '{columna}': {e}")
        else:
            print(f"✅ Columna '{columna}' ya existe")

    # Verificar y agregar columnas faltantes a almacenes (SIN DEFAULT)
    columnas_almacenes = [
        ('fecha_hora_creacion', 'DATETIME'),  # SIN DEFAULT
        ('fecha_hora_ultima_modificacion', 'DATETIME'),
        ('ultimo_usuario_en_modificar', 'TEXT')
    ]

    print("🔄 Verificando columnas de 'almacenes'...")
    cursor.execute("PRAGMA table_info(almacenes)")
    columnas_existentes = [col[1] for col in cursor.fetchall()]
    print(f"Columnas existentes en almacenes: {columnas_existentes}")

    for columna, tipo in columnas_almacenes:
        if columna not in columnas_existentes:
            try:
                cursor.execute(f'ALTER TABLE almacenes ADD COLUMN {columna} {tipo}')
                print(f"✅ Columna '{columna}' agregada a almacenes")
            except Exception as e:
                print(f"❌ Error agregando '{columna}': {e}")
        else:
            print(f"✅ Columna '{columna}' ya existe")

    conn.commit()
    conn.close()
    print("🎉 Base de datos inicializada correctamente!")


# Función para verificar la estructura actual
def verificar_estructura():
    conn = sqlite3.connect('InventarioBD.db')
    cursor = conn.cursor()

    print("\n📊 ESTRUCTURA ACTUAL:")

    print("\nTabla productos:")
    cursor.execute("PRAGMA table_info(productos)")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")

    print("\nTabla almacenes:")
    cursor.execute("PRAGMA table_info(almacenes)")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")

    conn.close()


if __name__ == '__main__':
    init_db()
    verificar_estructura()