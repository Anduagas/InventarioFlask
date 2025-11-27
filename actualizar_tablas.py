import sqlite3


def actualizar_tablas():
    conn = sqlite3.connect('InventarioBD.db')
    cursor = conn.cursor()

    print("🔄 Actualizando tabla productos...")

    # Columnas a agregar a productos
    columnas_productos = [
        'fecha_hora_creacion DATETIME DEFAULT CURRENT_TIMESTAMP',
        'fecha_hora_ultima_modificacion DATETIME',
        'ultimo_usuario_en_modificar TEXT',
        'departamento TEXT'
    ]

    for columna in columnas_productos:
        try:
            nombre_columna = columna.split(' ')[0]
            cursor.execute(f'ALTER TABLE productos ADD COLUMN {columna}')
            print(f'✅ Columna {nombre_columna} agregada a productos')
        except Exception as e:
            print(f'⚠️ Columna {nombre_columna}: {e}')

    print("🔄 Actualizando tabla almacenes...")

    # Columnas a agregar a almacenes
    columnas_almacenes = [
        'fecha_hora_creacion DATETIME DEFAULT CURRENT_TIMESTAMP',
        'fecha_hora_ultima_modificacion DATETIME',
        'ultimo_usuario_en_modificar TEXT'
    ]

    for columna in columnas_almacenes:
        try:
            nombre_columna = columna.split(' ')[0]
            cursor.execute(f'ALTER TABLE almacenes ADD COLUMN {columna}')
            print(f'✅ Columna {nombre_columna} agregada a almacenes')
        except Exception as e:
            print(f'⚠️ Columna {nombre_columna}: {e}')

    conn.commit()

    # Verificar estructura final
    print("\n📊 ESTRUCTURA FINAL:")
    print("Tabla productos:")
    cursor.execute("PRAGMA table_info(productos)")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")

    print("Tabla almacenes:")
    cursor.execute("PRAGMA table_info(almacenes)")
    for col in cursor.fetchall():
        print(f"  - {col[1]} ({col[2]})")

    conn.close()
    print("\n✅ Actualización completada!")


if __name__ == '__main__':
    actualizar_tablas()