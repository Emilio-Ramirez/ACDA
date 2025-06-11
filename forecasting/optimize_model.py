# forecasting/optimize_model.py
import pandas as pd
import numpy as np
from sklearn.metrics import mean_absolute_percentage_error
import xgboost as xgb
from sklearn.preprocessing import LabelEncoder
import optuna


def prepare_data():
    df = pd.read_parquet("forecasting/dataset_with_features.parquet")
    df = df.copy()

    # Encode categorías
    for col in ["Categoría", "Marca", "Región"]:
        df[col] = LabelEncoder().fit_transform(df[col])

    # Features y split
    feature_cols = [
        col for col in df.columns if col not in ["Fecha", "Ventas", "Ventas_Monto"]
    ]
    X, y = df[feature_cols], df["Ventas"]

    cutoff = df["Fecha"].max() - pd.Timedelta(weeks=8)
    train_mask = df["Fecha"] <= cutoff

    return X[train_mask], X[~train_mask], y[train_mask], y[~train_mask]


def objective(trial):
    X_train, X_test, y_train, y_test = prepare_data()

    params = {
        "n_estimators": trial.suggest_int("n_estimators", 100, 500),
        "max_depth": trial.suggest_int("max_depth", 3, 10),
        "learning_rate": trial.suggest_float("learning_rate", 0.01, 0.3),
        "subsample": trial.suggest_float("subsample", 0.6, 1.0),
        "random_state": 42,
    }

    model = xgb.XGBRegressor(**params)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)

    return mean_absolute_percentage_error(y_test, y_pred)


if __name__ == "__main__":
    study = optuna.create_study(direction="minimize")
    study.optimize(objective, n_trials=50)

    print(f"Best MAPE: {study.best_value:.3f} ({study.best_value*100:.1f}%)")
    print(f"Best params: {study.best_params}")
