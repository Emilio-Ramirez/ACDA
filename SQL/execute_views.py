import sqlite3
import pandas as pd
from pathlib import Path


def execute_views():
    # Conexion SQLite
    conn = sqlite3.connect("SQL/database.db")

    # Leer el archivo
    with open("SQL/views.sql", "r") as file:
        sql_script = file.read()

    # Ejecutar el script SQL
    conn.executescript(sql_script)

    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='view';")
    views = cursor.fetchall()

    print(f"Vistas creadas: {[view[0] for view in views]}")

    # Ver la vista
    cursor.execute("SELECT * FROM vista_inventario_ventas ;")
    results = cursor.fetchall()

    print("Primeros 5 registros de la vista 'ventas_por_tienda':")
    for row in results:
        print(row)

    conn.close()


if __name__ == "__main__":
    execute_views()
