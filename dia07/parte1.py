"""Advent of Code 2025 · Día 7: Laboratories · Parte 1

Simula el rayo fila a fila y cuenta cuántas veces se divide.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os


def resolver_desde_archivo(nombre_archivo):
    # Verificar si el archivo existe
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra el archivo '{nombre_archivo}'.")
        print("Asegúrate de crearlo en la misma carpeta que este script.")
        return

    # Leer el archivo
    with open(nombre_archivo, "r") as f:
        # Leemos las líneas y quitamos espacios en blanco sobrantes al final
        lines = [line.rstrip() for line in f.readlines() if line.strip()]

    if not lines:
        print("El archivo está vacío.")
        return

    # Convertir a matriz (grid)
    # Buscamos el ancho máximo para evitar errores si las líneas son desiguales
    ancho_max = max(len(line) for line in lines)
    alto = len(lines)

    # Rellenamos con espacios vacíos si alguna línea es más corta
    grid = [line.ljust(ancho_max, ".") for line in lines]

    # 1. Encontrar la posición inicial 'S'
    rayos_actuales = set()
    for y in range(alto):
        for x in range(ancho_max):
            if grid[y][x] == "S":
                rayos_actuales.add((x, y))

    if not rayos_actuales:
        print("Error: No se encontró la 'S' (punto de inicio) en el archivo.")
        return

    total_divisiones = 0

    # 2. Simulación
    while rayos_actuales:
        siguientes_rayos = set()

        for x, y in rayos_actuales:
            # El rayo intenta bajar
            target_x = x
            target_y = y + 1

            # Si se sale del mapa por abajo, el rayo termina
            if target_y >= alto:
                continue

            celda = grid[target_y][target_x]

            if celda == "^":
                # ¡SE DIVIDE!
                total_divisiones += 1

                # El rayo golpea el divisor y salen dos nuevos
                # desde la izquierda y derecha del divisor (en la misma fila del divisor)
                izq_x = target_x - 1
                der_x = target_x + 1

                # Verificar límites laterales y añadir a la siguiente ronda
                if izq_x >= 0:
                    siguientes_rayos.add((izq_x, target_y))
                if der_x < ancho_max:
                    siguientes_rayos.add((der_x, target_y))

            else:
                # Si es espacio vacío o tubería, el rayo avanza a esa posición
                siguientes_rayos.add((target_x, target_y))

        # Actualizamos el estado
        rayos_actuales = siguientes_rayos

    print("-" * 30)
    print("Proceso completado.")
    print("El rayo se dividió un total de: ", total_divisiones, " veces")
    print("-" * 30)


# --- EJECUCIÓN ---
if __name__ == "__main__":
    resolver_desde_archivo(ENTRADA)
