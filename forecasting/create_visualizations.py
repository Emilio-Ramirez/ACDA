# forecasting/create_visualizations.py
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go


def create_forecast_plots():
    """Crea visualizaciones para el dashboard"""

    # Cargar predicciones
    forecast = pd.read_parquet("forecasting/predicciones_futuras.parquet")
    historical = pd.read_parquet("forecasting/dataset_with_features.parquet")

    # 1. Forecast vs Histórico por tienda
    fig = go.Figure()

    for tienda in [1, 2, 3]:  # Top 3 tiendas
        # Histórico
        hist_tienda = (
            historical[historical["Tienda"] == tienda].groupby("Fecha")["Ventas"].sum()
        )
        fig.add_trace(
            go.Scatter(
                x=hist_tienda.index,
                y=hist_tienda.values,
                name=f"Histórico T{tienda}",
                line=dict(dash="solid"),
            )
        )

        # Forecast
        fore_tienda = (
            forecast[forecast["Tienda"] == tienda]
            .groupby("Fecha")["Prediccion_Ventas"]
            .sum()
        )
        fig.add_trace(
            go.Scatter(
                x=fore_tienda.index,
                y=fore_tienda.values,
                name=f"Forecast T{tienda}",
                line=dict(dash="dash"),
            )
        )

    fig.update_layout(
        title="Ventas: Histórico vs Forecast por Tienda",
        xaxis_title="Fecha",
        yaxis_title="Ventas Semanales",
    )
    fig.write_html("forecasting/forecast_por_tienda.html")

    # 2. Top productos forecast
    top_products = (
        forecast.groupby("Producto")["Prediccion_Ventas"]
        .sum()
        .sort_values(ascending=False)
        .head(10)
    )

    fig2 = px.bar(
        x=top_products.index,
        y=top_products.values,
        title="Top 10 Productos - Ventas Forecast 3 meses",
    )
    fig2.write_html("forecasting/top_productos_forecast.html")

    print("Visualizaciones creadas:")
    print("- forecast_por_tienda.html")
    print("- top_productos_forecast.html")


if __name__ == "__main__":
    create_forecast_plots()
