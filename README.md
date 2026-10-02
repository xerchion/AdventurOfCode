# Advent of Code 2025

Soluciones en Python a los 12 retos de [Advent of Code 2025](https://adventofcode.com/2025). Solo usan la biblioteca estándar.

## Retos

| Día | Reto | Parte 1 | Parte 2 |
| --- | --- | --- | --- |
| [1](dia01) | [Secret Entrance](https://adventofcode.com/2025/day/1) | Aritmética modular | División entera para contar los pasos por cero |
| [2](dia02) | [Gift Shop](https://adventofcode.com/2025/day/2) | Comparación de las dos mitades de un número | Búsqueda de un patrón repetido en la cadena |
| [3](dia03) | [Lobby](https://adventofcode.com/2025/day/3) | El mayor dígito y el mayor de los que le siguen | Selección voraz con una pila |
| [4](dia04) | [Printing Department](https://adventofcode.com/2025/day/4) | Rejilla y recuento de los 8 vecinos | Simulación por rondas hasta que no hay cambios |
| [5](dia05) | [Cafeteria](https://adventofcode.com/2025/day/5) | Pertenencia a rangos | Ordenación y fusión de intervalos |
| [6](dia06) | [Trash Compactor](https://adventofcode.com/2025/day/6) | Operaciones por columnas | Lectura de la hoja en vertical, de derecha a izquierda |
| [7](dia07) | [Laboratories](https://adventofcode.com/2025/day/7) | Simulación fila a fila con conjuntos | Recuento de caminos acumulando por columna |
| [8](dia08) | [Playground](https://adventofcode.com/2025/day/8) | Union-Find sobre los pares más cercanos | Union-Find hasta que queda un solo grupo |
| [9](dia09) | [Movie Theater](https://adventofcode.com/2025/day/9) | Fuerza bruta sobre pares de puntos | Segmentos del polígono y trazado de rayos |
| [10](dia10) | [Factory](https://adventofcode.com/2025/day/10) | Fuerza bruta sobre combinaciones de botones | Eliminación de Gauss-Jordan y búsqueda sobre las variables libres |
| [11](dia11) | [Reactor](https://adventofcode.com/2025/day/11) | Búsqueda en profundidad con memoria | Producto de los caminos de cada tramo |
| [12](dia12) | [Christmas Tree Farm](https://adventofcode.com/2025/day/12) | Vuelta atrás con rotaciones y simetrías | — |

El día 12 solo tiene una parte.

## Cómo ejecutarlas

Requisitos: Python 3.10 o superior.

Las entradas no están en el repositorio, porque Advent of Code pide no redistribuirlas. Descarga la tuya desde la página de cada reto y guárdala como `entrada.txt` en la carpeta del día.

```bash
python dia01/parte1.py                # lee dia01/entrada.txt
python dia01/parte1.py otro.txt       # o el fichero que le indiques
```

Todas terminan en pocos segundos, salvo el día 12, que tarda alrededor de un minuto.

## Estructura

```
dia01/
    parte1.py
    parte2.py
    entrada.txt     (tu entrada; no se sube)
...
dia12/
    parte1.py
```

## Autor

Sergio Ucedo · [Portafolio](https://xerchion.github.io/webPortfolio/) · [LinkedIn](https://www.linkedin.com/in/sergio-ucedo)
