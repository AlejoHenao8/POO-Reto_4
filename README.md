# POO-Reto_4
Este repositorio es una modificación del repositorio [POO-Reto_3](https://github.com/AlejoHenao8/POO-Reto_3), pero añadiendo métodos setter y getter y sobrescribiendo `total_price()` según la composición del pedido.
## Setters y Getters
Todos los atributos se renombraron a `_attr` (privado) y se expusieron a través de `@property / @<attr>.setter`:

| Clase        | Propiedades modificadas  |
| ------------ | ------------------------ |
| `MenuItem`   | `name`, `price`          |
| `Beverage`   | `is_alcoholic`, `mls`    |
| `Appetizer`  | `is_vegan`, `portion`    |
| `MainCourse` | `protein`, `has_garnish` |

## Oreden basada en descuentos
Dentro de la nueva función auxiliar `_compute_discounts()` se evalúan tres reglas, sin modificar las clases de los artículos:

| Regla                         | Descuento                            |
| ----------------------------- | ------------------------------------ |
| $\geq 1$ `MainCourse`         | 10% off every non-alcoholic beverage |
| $\geq 2$ `MainCourse`         | 15% off every appetizer<br>          |
| $\geq 2$ `Beverage` alcoholica | $1.00 off each alcoholic drink       |

Las reglas pueden acumularse.
La factura ahora muestra un subtotal, una sección de descuentos detallados que enumera solo las reglas que se aplicaron y el total final.
