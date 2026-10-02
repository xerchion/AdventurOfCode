"""Advent of Code 2025 · Día 7: Laboratories · Parte 2

Cuenta los caminos posibles del rayo acumulando, fila a fila, cuántos llegan a cada columna.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os


def resolver_parte_dos(nombre_archivo):
    # 1. Verificación y lectura del archivo
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    with open(nombre_archivo, "r") as f:
        lines = [line.rstrip() for line in f.readlines() if line.strip()]

    if not lines:
        print("El archivo está vacío.")
        return

    # Preparar la rejilla (grid)
    ancho_max = max(len(line) for line in lines)
    alto = len(lines)
    grid = [line.ljust(ancho_max, ".") for line in lines]

    # 2. Encontrar la posición inicial 'S'
    # Usaremos un diccionario para contar cuántas líneas temporales existen en cada coordenada X
    # { coordenada_x : cantidad_de_lineas_temporales }
    posiciones_actuales = {}

    start_y = 0
    for y in range(alto):
        if "S" in grid[y]:
            start_x = grid[y].index("S")
            posiciones_actuales[start_x] = 1  # Empezamos con 1 línea temporal
            start_y = y
            break

    total_lineas_finalizadas = 0

    # 3. Simulación paso a paso (fila por fila)
    # Recorremos desde la fila de inicio hacia abajo
    for y in range(start_y, alto):
        siguientes_posiciones = {}

        # Procesamos cada posición donde hay partículas en la fila actual
        for x, cantidad in posiciones_actuales.items():

            # Calculamos dónde intenta ir la partícula (fila siguiente)
            target_y = y + 1

            # Si target_y es igual a la altura, significa que ha salido del mapa
            if target_y >= alto:
                total_lineas_finalizadas += cantidad
                continue

            # Miramos qué hay en la celda de destino
            celda = grid[target_y][x]

            if celda == "^":
                # DIVISOR: El universo se divide.
                # La cantidad de líneas actuales se duplica (izq y der)

                # Izquierda
                izq_x = x - 1
                if izq_x >= 0:
                    siguientes_posiciones[izq_x] = (
                        siguientes_posiciones.get(izq_x, 0) + cantidad
                    )

                # Derecha
                der_x = x + 1
                if der_x < ancho_max:
                    siguientes_posiciones[der_x] = (
                        siguientes_posiciones.get(der_x, 0) + cantidad
                    )

            else:
                # ESPACIO / TUBERÍA: La línea temporal continúa recta
                # Sumamos la cantidad actual a la posición de destino
                siguientes_posiciones[x] = siguientes_posiciones.get(x, 0) + cantidad

        # Avanzamos al siguiente paso
        posiciones_actuales = siguientes_posiciones

    # Si quedaran partículas en el último paso (justo en el borde), las sumamos
    # (El bucle anterior ya las suma al detectar que salen, pero por seguridad)
    # En esta lógica, al salir del bucle 'y', las que quedaran en 'posiciones_actuales'
    # técnicamente no han salido "fuera" del array todavía si el bucle termina,
    # pero nuestra condición `if target_y >= alto` maneja la salida.

    print("-" * 30)
    print("Cálculo Multiverso completado.")
    print("Total de líneas temporales activas: ", total_lineas_finalizadas)
    print("-" * 30)


if __name__ == "__main__":
    resolver_parte_dos(ENTRADA)
