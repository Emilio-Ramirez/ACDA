# Examen Técnico - Analítica y Ciencia de Datos Avanzada

## 🚀 Instalación

```bash
pip install -r requirements.txt
```

## 🎯 Contexto del Proyecto

**Cliente:** Retailer con 10 tiendas distribuidas por regiones
**Objetivo:** Optimizar reposición de inventarios mediante modelos predictivos y dashboards interactivos
**Alcance:** Análisis de elasticidad de precios e impacto climático en demanda

## 📊 Datasets Disponibles

- 📈 Ventas históricas (2 años)
- 📦 Inventarios actuales
- 🏷️ Catálogo de productos
- 🏪 Catálogo de tiendas por región
- 🌤️ Información climática semanal por región

## ✅ Procesos Realizados

### 📁 Preparación de Archivos

- **Conversión:** Excel → Parquet para mejor rendimiento
- **Estructura:** Separación por datasets individuales
- **Encoding:** Normalización de caracteres especiales y tildes en los títulos

### 🧹 Limpieza de Datos

- **IDs consistentes:** Convertí "Producto_1", "Tienda_1" → números enteros (1, 2, 3...)
- **Fechas:** Formato datetime64[ns] para análisis temporal
- **Marcas:** Minúsculas sin prefijos ("marca_a" → "a")
- **Sin duplicados:** Verificado en todos los datasets
- **Outliers:** Mantenidos (son datos de negocio válidos, no errores)
- **Rangos:** Validados precios, descuentos y fechas

### 🗃️ Base de Datos SQL

**Tecnología:** SQLite local para análisis

- **Migración:** Datasets limpios → Tablas SQL
- **Vista integrada:** `vista_inventario_ventas` (datos agregados)
- **Vista detallada:** `vista_analisis_detallado` (datos granulares)
  - Combina ventas históricas + clima + descuentos por fecha
  - Incluye información de productos y regiones
- **Scripts:** `create_database.py`, `execute_views.py`, `views.sql`

## 📈 Visualizaciones Dashboard

### **Análisis Básico**

1. **Ventas entre tiendas y regiones** - Gráfica de barras apiladas por región
2. **Evolución de Ventas por Región (2023-2025)** - Serie de tiempo con múltiples líneas
3. **Impacto Climático en Ventas** - Serie temporal: ventas vs temperatura promedio

### **Sistema de Alertas**

4. **Detección de Anomalías en Ventas Semanales** - Scatter plot temporal con código de colores
5. **Inventario Crítico** - Gráfica de barras con días de stock restante
6. **Períodos en Declive** - Scatter plot por mes agrupado

### **Análisis de Elasticidad**

7. **Sensibilidad a Descuentos por Producto** - Scatter plot: descuento vs ventas
8. **Ranking de Elasticidad** - Barras horizontales ordenadas por elasticidad

**Total: 8 visualizaciones** cubriendo análisis completo de retail

## 📊 Análisis de Datos

**20,800 registros con campos:**

- **Temporales:** Fecha
- **Identificadores:** Tienda (1-10), Producto (1-20)
- **Ventas:** Unidades, Monto, Descuento_Aplicado
- **Inventario:** Stock actual por tienda-producto
- **Productos:** Categoría, Marca, Precio, Costo
- **Geografía:** Región (Centro, Este, Oeste, Sur)
- **Clima:** Temperatura, Precipitación

**Periodo:** Marzo 2023 - Febrero 2025

## 🎯 OBJETIVO

Identificar patrones para optimizar estrategia de descuentos e inventarios considerando factores climáticos

## ⚠️ BIAS IDENTIFICADOS

- **Sesgo por volumen:** Agregaciones SUM() favorecen grupos con más registros
- **Distribución desigual:** Centro: 4 tiendas, Este: 1 tienda, Oeste: 4, Sur: 1
- **Canibalización aparente:** Descuentos altos muestran menores ventas promedio
- **Sesgo temporal:** 2025 y 2024 incompletos
