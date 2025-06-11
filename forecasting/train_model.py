# forecasting/train_model.py
import pandas as pd
import numpy as np
from sklearn.model_selection import TimeSeriesSplit
from sklearn.metrics import mean_absolute_percentage_error, mean_squared_error
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder


def prepare_training_data(df):
    """Separa features y target, split temporal"""
    df = df.copy()

    # Encode categorías
    le_categoria = LabelEncoder()
    le_marca = LabelEncoder()
    le_region = LabelEncoder()

    # AGREGAR ESTAS LÍNEAS:
    df["Categoría"] = le_categoria.fit_transform(df["Categoría"])
    df["Marca"] = le_marca.fit_transform(df["Marca"])
    df["Región"] = le_region.fit_transform(df["Región"])

    # Features (excluir target y metadata)
    feature_cols = [
        col for col in df.columns if col not in ["Fecha", "Ventas", "Ventas_Monto"]
    ]

    X = df[feature_cols]
    y = df["Ventas"]  # Target: predecir unidades vendidas

    # Split temporal: últimas 8 semanas para test
    cutoff_date = df["Fecha"].max() - pd.Timedelta(weeks=8)

    train_mask = df["Fecha"] <= cutoff_date
    test_mask = df["Fecha"] > cutoff_date

    X_train, X_test = X[train_mask], X[test_mask]
    y_train, y_test = y[train_mask], y[test_mask]

    print(f"Train: {len(X_train)} | Test: {len(X_test)}")
    print(f"Features: {len(feature_cols)}")

    return X_train, X_test, y_train, y_test, feature_cols


def train_xgboost(X_train, y_train, X_test, y_test):
    """Entrena modelo XGBoost básico"""

    model = xgb.XGBRegressor(
        n_estimators=100, max_depth=6, learning_rate=0.1, random_state=42
    )

    model.fit(X_train, y_train)

    # Predicciones
    y_pred = model.predict(X_test)

    # Métricas
    mape = mean_absolute_percentage_error(y_test, y_pred)
    rmse = np.sqrt(mean_squared_error(y_test, y_pred))

    print(f"MAPE: {mape:.3f} ({mape*100:.1f}%)")
    print(f"RMSE: {rmse:.2f}")

    return model, y_pred


if __name__ == "__main__":
    df = pd.read_parquet("forecasting/dataset_with_features.parquet")
    X_train, X_test, y_train, y_test, features = prepare_training_data(df)
    model, predictions = train_xgboost(X_train, y_train, X_test, y_test)
