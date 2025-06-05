````markdown
# Examen Técnico - Analítica y Ciencia de Datos Avanzada

## 🚀 Instalación

```bash
pip install -r requirements.txt
```
````

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

---

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
- **Vista integrada:** `vista_inventario_ventas`
  - Combina inventario actual + ventas históricas totales
  - Incluye información de productos (categoría, marca) y tiendas (región)
  - Calcula precio promedio por tienda-producto
- **Scripts:** `create_database.py`, `execute_views.py`, `views.sql`

```

```
