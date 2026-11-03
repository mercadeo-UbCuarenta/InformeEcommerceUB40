# Informe Semanal Ecommerce · UB Cuarenta

Informe semanal del canal digital (tienda online ubcuarenta.com) para la Gerencia de UB Cuarenta.

- `index.html`: semana más reciente.
- `semanas/<mes>-<semana>.html`: cada semana publicada (semana retail de lunes a domingo; la semana pertenece al mes en que cae su jueves).
- `archivo.html`: archivo de todas las semanas con sus cifras clave; cada informe trae un selector para saltar a otra semana.
- `semanas.json`: una fila por semana publicada (fuente del archivo y del selector).

## Agregar una semana

1. Copia la página nueva a `semanas/<mes>-<semana>.html` y a `index.html`.
2. Agrega su fila al final de `semanas.json`.
3. Corre `python3 herramientas/archivo.py`: actualiza el selector en todas las páginas y regenera `archivo.html`.

Fuentes: venta y PV del SEGUIMIENTO PV (Mahalo), tráfico y pedidos de Shopify, pauta de Meta y Google Ads, campañas del calendario comercial.
