DROP VIEW IF EXISTS vista_inventario_ventas;

CREATE VIEW vista_inventario_ventas AS

SELECT 

    i.Tienda,
    i.Producto,
    i.Inventario_Actual,
    COALESCE(v.Ventas_Totales, 0) as Ventas_Totales,
    COALESCE(v.Monto_Total, 0.0) as Monto_Total_Ventas,

    CASE 
        WHEN v.Ventas_Totales > 0 
        THEN ROUND(v.Monto_Total / v.Ventas_Totales, 2) 
        ELSE 0 
    END as Precio_Promedio,

    p.Categoría,
    p.Marca,
    t.Región
FROM inventarios_actuales i

LEFT JOIN (
    SELECT 
        Tienda,
        Producto,
        SUM(Ventas) as Ventas_Totales,
        SUM(Ventas_Monto) as Monto_Total
    FROM ventas_historicas 
    GROUP BY Tienda, Producto
) v ON i.Tienda = v.Tienda AND i.Producto = v.Producto

LEFT JOIN catalogo_productos p ON i.Producto = p.Producto

LEFT JOIN catalogo_tiendas t ON i.Tienda = t.Tienda

ORDER BY i.Tienda, i.Producto;

DROP VIEW IF EXISTS vista_analisis_detallado;

CREATE VIEW vista_analisis_detallado AS
SELECT 
    vh.Fecha,
    vh.Tienda,
    vh.Producto,
    vh.Ventas,
    vh.Ventas_Monto,
    vh.Descuento_Aplicado,
    p.Categoría,
    t.Región,
    c.Temperatura_Promedio_C,
    c.Precipitacion_mm
FROM ventas_historicas vh
LEFT JOIN catalogo_productos p ON vh.Producto = p.Producto
LEFT JOIN catalogo_tiendas t ON vh.Tienda = t.Tienda
LEFT JOIN clima_regiones c ON vh.Fecha = c.Fecha AND t.Región = c.Región;
