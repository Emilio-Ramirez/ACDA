import pandas as pd
import os
from pathlib import Path


def extract_id_from_column(df, column_name):
    """Estrae el nuemero (ID) del texto covirtiendolo a un entero."""
    df[column_name] = df[column_name].str.extract(r"(\d+)").astype(int)
    return df


def clean_ventas(df):
    """Limpieza de ventas"""
    df = extract_id_from_column(df, "Tienda")  # Fixed: was "Producto"
    df = extract_id_from_column(df, "Producto")  # Added missing line
    return df


def clean_productos(df):
    """Clean product catalog data"""
    df = extract_id_from_column(df, "Producto")
    df["Marca"] = df["Marca"].str.lower().str.replace("marca_", "")
    return df


def clean_tiendas(df):
    """Limpieza de tiedas"""
    df = extract_id_from_column(df, "Tienda")
    return df


def clean_inventarios(df):
    """Limpieza de inventarioo"""
    df = extract_id_from_column(df, "Tienda")
    df = extract_id_from_column(df, "Producto")
    return df


def clean_clima(df):
    """Limpieza de clima - no necesario pero lo deje por escalabilidad y orden"""
    return df


def process_dataset(file_path, dataset_name, cleaning_functions):
    """Procesa los datasets."""
    df = pd.read_parquet(file_path)

    if dataset_name in cleaning_functions:
        print(f"\n---Cleaning dataset: {dataset_name}---\n")
        df = cleaning_functions[dataset_name](df)

        # Se guarda el archivo limpio
        output_path = Path("datasets_clean") / Path(file_path).name
        df.to_parquet(output_path, index=False)

        print(df.head())
        print(df.dtypes)
    return df


def main():
    Path("datasets_clean").mkdir(exist_ok=True)

    cleaning_functions = {
        "ventas_historicas": clean_ventas,
        "catalogo_productos": clean_productos,
        "catalogo_tiendas": clean_tiendas,
        "inventarios_actuales": clean_inventarios,
        "clima_regiones": clean_clima,
    }

    # Procesar archivos
    raw_data_path = Path("datasets_raw")
    for file_path in raw_data_path.glob("*.parquet"):
        dataset_name = file_path.stem
        process_dataset(file_path, dataset_name, cleaning_functions)


if __name__ == "__main__":
    main()
