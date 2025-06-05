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
