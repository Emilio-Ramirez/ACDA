# forecasting/predict_future.py
import pandas as pd
import numpy as np
import joblib
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
from pathlib import Path


def create_future_dates():
    """Crea fechas para próximos 3 meses (12 semanas)"""
    last_date = pd.read_parquet("forecasting/dataset_with_features.parquet")[
        "Fecha"
    ].max()
    future_dates = pd.date_range(
        start=last_date + pd.Timedelta(weeks=1), periods=12, freq="W"
    )
    return future_dates


def prepare_future_data():
    """Prepara dataset para predicciones futuras"""
    # Cargar datos históricos
    df = pd.read_parquet("forecasting/dataset_with_features.parquet")

    # Crear combinaciones tienda-producto para futuras fechas
    future_dates = create_future_dates()
    tiendas = df["Tienda"].unique()
    productos = df["Producto"].unique()

    future_data = []
    for date in future_dates:
        for tienda in tiendas:
            for producto in productos:
                future_data.append(
                    {"Fecha": date, "Tienda": tienda, "Producto": producto}
                )

    future_df = pd.DataFrame(future_data)

    # Agregar features base (asumiendo valores promedio)
    # En producción usarías datos reales de clima/descuentos
    future_df["Descuento_Aplicado"] = 0  # Sin descuentos por defecto
    future_df["Temperatura_Promedio_C"] = df["Temperatura_Promedio_C"].mean()
    future_df["Precipitacion_mm"] = df["Precipitacion_mm"].mean()

    print(f"Dataset futuro: {len(future_df)} predicciones por hacer")
    return future_df


def add_missing_features(future_df, historical_df):
    """Agrega features faltantes basado en datos históricos"""

    # Primero necesitamos agregar las columnas categóricas desde historical
    productos_info = historical_df[
        ["Producto", "Categoría", "Precio", "Costo", "Descuento_Max", "Marca"]
    ].drop_duplicates()
    tiendas_info = historical_df[["Tienda", "Región"]].drop_duplicates()

    # Merge con info de productos y tiendas
    future_df = future_df.merge(productos_info, on="Producto", how="left")
    future_df = future_df.merge(tiendas_info, on="Tienda", how="left")

    # Encode categorías (necesitamos los mismos mapeos que en entrenamiento)
    le_categoria = LabelEncoder()
    le_marca = LabelEncoder()
    le_region = LabelEncoder()

    # Fit con datos históricos
    le_categoria.fit(historical_df["Categoría"])
    le_marca.fit(historical_df["Marca"])
    le_region.fit(historical_df["Región"])

    # Transform future data
    future_df["Categoría"] = le_categoria.transform(future_df["Categoría"])
    future_df["Marca"] = le_marca.transform(future_df["Marca"])
    future_df["Región"] = le_region.transform(future_df["Región"])

    # Features temporales
    future_df["year"] = future_df["Fecha"].dt.year
    future_df["month"] = future_df["Fecha"].dt.month
    future_df["week"] = future_df["Fecha"].dt.isocalendar().week
    future_df["day_of_year"] = future_df["Fecha"].dt.dayofyear

    # Lags y rolling: usar últimos valores históricos por tienda-producto
    lag_columns = [
        "ventas_lag_1",
        "ventas_lag_2",
        "ventas_lag_4",
        "ventas_lag_8",
        "monto_lag_1",
        "monto_lag_2",
        "monto_lag_4",
        "monto_lag_8",
    ]
    rolling_columns = [
        "ventas_rolling_4",
        "ventas_rolling_8",
        "ventas_rolling_12",
        "monto_rolling_4",
        "monto_rolling_8",
        "monto_rolling_12",
    ]

    # Initialize columns
    for col in lag_columns + rolling_columns:
        future_df[col] = np.nan

    for tienda in future_df["Tienda"].unique():
        for producto in future_df["Producto"].unique():
            hist_mask = (historical_df["Tienda"] == tienda) & (
                historical_df["Producto"] == producto
            )
            hist_data = historical_df[hist_mask].sort_values("Fecha")

            if len(hist_data) > 0:
                future_mask = (future_df["Tienda"] == tienda) & (
                    future_df["Producto"] == producto
                )

                # Lags - usar últimos valores
                if len(hist_data) >= 1:
                    future_df.loc[future_mask, "ventas_lag_1"] = hist_data[
                        "Ventas"
                    ].iloc[-1]
                    future_df.loc[future_mask, "monto_lag_1"] = hist_data[
                        "Ventas_Monto"
                    ].iloc[-1]
                if len(hist_data) >= 2:
                    future_df.loc[future_mask, "ventas_lag_2"] = hist_data[
                        "Ventas"
                    ].iloc[-2]
                    future_df.loc[future_mask, "monto_lag_2"] = hist_data[
                        "Ventas_Monto"
                    ].iloc[-2]
                if len(hist_data) >= 4:
                    future_df.loc[future_mask, "ventas_lag_4"] = hist_data[
                        "Ventas"
                    ].iloc[-4]
                    future_df.loc[future_mask, "monto_lag_4"] = hist_data[
                        "Ventas_Monto"
                    ].iloc[-4]
                if len(hist_data) >= 8:
                    future_df.loc[future_mask, "ventas_lag_8"] = hist_data[
                        "Ventas"
                    ].iloc[-8]
                    future_df.loc[future_mask, "monto_lag_8"] = hist_data[
                        "Ventas_Monto"
                    ].iloc[-8]

                # Rolling - usar últimas ventanas
                if len(hist_data) >= 4:
                    future_df.loc[future_mask, "ventas_rolling_4"] = (
                        hist_data["Ventas"].tail(4).mean()
                    )
                    future_df.loc[future_mask, "monto_rolling_4"] = (
                        hist_data["Ventas_Monto"].tail(4).mean()
                    )
                if len(hist_data) >= 8:
                    future_df.loc[future_mask, "ventas_rolling_8"] = (
                        hist_data["Ventas"].tail(8).mean()
                    )
                    future_df.loc[future_mask, "monto_rolling_8"] = (
                        hist_data["Ventas_Monto"].tail(8).mean()
                    )
                if len(hist_data) >= 12:
                    future_df.loc[future_mask, "ventas_rolling_12"] = (
                        hist_data["Ventas"].tail(12).mean()
                    )
                    future_df.loc[future_mask, "monto_rolling_12"] = (
                        hist_data["Ventas_Monto"].tail(12).mean()
                    )

    # Fill remaining NaNs with median values
    for col in lag_columns + rolling_columns:
        if future_df[col].isna().any():
            future_df[col] = future_df[col].fillna(historical_df[col].median())

    return future_df


def make_predictions():
    """Genera predicciones futuras"""

    # Cargar datos históricos
    historical_df = pd.read_parquet("forecasting/dataset_with_features.parquet")

    # Preparar datos futuros
    future_df = prepare_future_data()
    future_complete = add_missing_features(future_df, historical_df)

    # Crear modelo con mejores parámetros
    model = xgb.XGBRegressor(
        n_estimators=176,
        max_depth=3,
        learning_rate=0.13704097193553108,
        subsample=0.876336097822409,
        random_state=42,
    )

    # Entrenar con todos los datos históricos
    feature_cols = [
        col
        for col in historical_df.columns
        if col not in ["Fecha", "Ventas", "Ventas_Monto"]
    ]

    # Encode categorías en historical data
    historical_encoded = historical_df.copy()
    for col in ["Categoría", "Marca", "Región"]:
        historical_encoded[col] = LabelEncoder().fit_transform(historical_encoded[col])

    X_all = historical_encoded[feature_cols]
    y_all = historical_encoded["Ventas"]

    print("Entrenando modelo con todos los datos históricos...")
    model.fit(X_all, y_all)

    # Hacer predicciones
    print("Generando predicciones futuras...")
    X_future = future_complete[feature_cols]
    predictions = model.predict(X_future)

    # Agregar predicciones al dataframe
    future_complete["Prediccion_Ventas"] = predictions
    future_complete["Prediccion_Monto"] = predictions * future_complete["Precio"]

    # Guardar resultados
    future_complete.to_parquet("forecasting/predicciones_futuras.parquet", index=False)
    print("Predicciones guardadas: predicciones_futuras.parquet")

    # Mostrar resumen
    print(f"\nResumen de predicciones:")
    print(f"Total predicciones: {len(future_complete)}")
    print(f"Ventas promedio predichas: {predictions.mean():.1f} unidades")
    print(f"Rango: {predictions.min():.1f} - {predictions.max():.1f}")
    print(
        f"Periodo: {future_complete['Fecha'].min()} - {future_complete['Fecha'].max()}"
    )

    return future_complete


# Agregar al final de SQL/export_to_csv.py
def export_forecast_data():
    """Exporta predicciones futuras para Tableau"""
    if Path("forecasting/predicciones_futuras.parquet").exists():
        df_forecast = pd.read_parquet("forecasting/predicciones_futuras.parquet")
        df_forecast.to_csv("tableau_data/predicciones_futuras.csv", index=False)
        print(f"✅ Exportado: predicciones_futuras.csv ({len(df_forecast)} registros)")
    else:
        print("⚠️  No se encontraron predicciones. Ejecuta predict_future.py primero")


if __name__ == "__main__":
    predictions = make_predictions()
    export_forecast_data()  # Agregar esta línea

    # Mostrar algunas predicciones
    print("\nPrimeras 10 predicciones:")
    print(
        predictions[
            ["Fecha", "Tienda", "Producto", "Prediccion_Ventas", "Prediccion_Monto"]
        ].head(10)
    )
