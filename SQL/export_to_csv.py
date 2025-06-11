import sqlite3
import pandas as pd
from pathlib import Path


def export_data_for_tableau():
    """Exporta datos de SQLite a CSV para Tableau"""

    conn = sqlite3.connect("SQL/database.db")  # Corregido nombre de DB

    # Crear carpeta para exports
    Path("tableau_data").mkdir(parents=True, exist_ok=True)

    # Exportar vista de inventario y ventas
    df_vista = pd.read_sql_query("SELECT * FROM vista_inventario_ventas", conn)
    df_vista.to_csv("tableau_data/vista_inventario_ventas.csv", index=False)
    print(f"✅ Exportado: vista_inventario_ventas.csv ({len(df_vista)} registros)")

    # Exportar nueva vista detallada
    df_detalle = pd.read_sql_query("SELECT * FROM vista_analisis_detallado", conn)
    df_detalle.to_csv("tableau_data/vista_analisis_detallado.csv", index=False)
    print(f"✅ Exportado: vista_analisis_detallado.csv ({len(df_detalle)} registros)")

    # Exportar ventas históricas originales
    df_ventas = pd.read_sql_query("SELECT * FROM ventas_historicas", conn)
    df_ventas.to_csv("tableau_data/ventas_historicas.csv", index=False)
    print(f"✅ Exportado: ventas_historicas.csv ({len(df_ventas)} registros)")

    # Exportar datos climáticos
    df_clima = pd.read_sql_query("SELECT * FROM clima_regiones", conn)
    df_clima.to_csv("tableau_data/clima_regiones.csv", index=False)
    print(f"✅ Exportado: clima_regiones.csv ({len(df_clima)} registros)")

    conn.close()
    print("\n🎉 Datos listos para Tableau!")


if __name__ == "__main__":
    export_data_for_tableau()
