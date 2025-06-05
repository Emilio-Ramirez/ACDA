import sqlite3
import pandas as pd
from pathlib import Path


def create_database():
    # Conexion SQLite
    conn = sqlite3.connect("SQL/database.db")

    # Path datos limpios
    clean_data_path = Path("datasets_clean")

    # Mapeo de archivos a nombres de tabls
    table_names = {
        "ventas_historicas.parquet": "ventas_historicas",
        "inventarios_actuales.parquet": "inventarios_actuales",
        "catalogo_productos.parquet": "catalogo_productos",
        "catalogo_tiendas.parquet": "catalogo_tiendas",
        "clima_regiones.parquet": "clima_regiones",
    }

    for file_name, table_name in table_names.items():
        file_path = clean_data_path / file_name
        if file_path.exists():
            df = pd.read_parquet(file_path)

            # Guardar  en SQLite
            df.to_sql(table_name, conn, if_exists="replace", index=False)
            print(f"Tabla '{table_name}' creada con {len(df)} registros")
        else:
            print(f"Archivo {file_name} no encontrado en {clean_data_path}")

    # Mostrar tables creadas
    cursor = conn.cursor()
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()
    print(f"Tablas creadas: {[table[0] for table in tables]}")

    conn.close()
    print("Base de datos creada exitosamente.")


if __name__ == "__main__":
    create_database()
