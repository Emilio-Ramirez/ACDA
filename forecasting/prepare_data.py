import pandas as pd
from pathlib import Path


def consolidate_data():
    """Consolida datos limpios en dataset único para forecasting"""

    # Crear directorio
    Path("forecasting").mkdir(exist_ok=True)

    # Cargar datasets limpios
    ventas = pd.read_parquet("datasets_clean/ventas_historicas.parquet")
    productos = pd.read_parquet("datasets_clean/catalogo_productos.parquet")
    tiendas = pd.read_parquet("datasets_clean/catalogo_tiendas.parquet")
    clima = pd.read_parquet("datasets_clean/clima_regiones.parquet")

    # Join principal: ventas + productos + tiendas + clima
    df = ventas.merge(productos, on="Producto", how="left")
    df = df.merge(tiendas, on="Tienda", how="left")
    df = df.merge(clima, on=["Fecha", "Región"], how="left")

    # Convertir fecha
    df["Fecha"] = pd.to_datetime(df["Fecha"])

    # Ordenar por fecha
    df = df.sort_values(["Tienda", "Producto", "Fecha"]).reset_index(drop=True)

    print(f"Dataset consolidado: {len(df)} registros")
    print(f"Periodo: {df['Fecha'].min()} - {df['Fecha'].max()}")
    print(f"Columnas: {list(df.columns)}")

    # Guardar
    df.to_parquet("forecasting/forecasting_dataset.parquet", index=False)

    return df


if __name__ == "__main__":
    df = consolidate_data()
    print(df.head())
