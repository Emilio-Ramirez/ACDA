# forecasting/feature_engineering.py
import pandas as pd
import numpy as np


def create_features(df):
    """Crea features para XGBoost"""

    df = df.copy()
    df = df.sort_values(["Tienda", "Producto", "Fecha"])

    # Features temporales
    df["year"] = df["Fecha"].dt.year
    df["month"] = df["Fecha"].dt.month
    df["week"] = df["Fecha"].dt.isocalendar().week
    df["day_of_year"] = df["Fecha"].dt.dayofyear

    # Lags por tienda-producto
    for lag in [1, 2, 4, 8]:
        df[f"ventas_lag_{lag}"] = df.groupby(["Tienda", "Producto"])["Ventas"].shift(
            lag
        )
        df[f"monto_lag_{lag}"] = df.groupby(["Tienda", "Producto"])[
            "Ventas_Monto"
        ].shift(lag)

    # Rolling stats - método corregido
    for window in [4, 8, 12]:
        df[f"ventas_rolling_{window}"] = df.groupby(["Tienda", "Producto"])[
            "Ventas"
        ].transform(lambda x: x.rolling(window).mean())
        df[f"monto_rolling_{window}"] = df.groupby(["Tienda", "Producto"])[
            "Ventas_Monto"
        ].transform(lambda x: x.rolling(window).mean())

    # Eliminar NaNs iniciales
    df = df.dropna()

    print(f"Features creados: {len(df)} registros válidos")
    print(f"Nuevas columnas: {len(df.columns)} total")

    return df


if __name__ == "__main__":
    df = pd.read_parquet("forecasting/forecasting_dataset.parquet")
    df_features = create_features(df)
    df_features.to_parquet("forecasting/dataset_with_features.parquet")
    print(f"Guardado: dataset_with_features.parquet")
