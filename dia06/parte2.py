"""Advent of Code 2025 · Día 6: Trash Compactor · Parte 2

Los números se leen en vertical, columna a columna y de derecha a izquierda.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import math
import os


def resolver_parte_dos(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    # 1. Leer el archivo y normalizar la cuadrícula
    with open(nombre_archivo, "r") as f:
        lines = [
            line.strip("\n") for line in f.readlines()
        ]  # Mantener espacios a la derecha es importante, pero strip('\n') quita el salto de linea

    if not lines:
        return

    # Encontrar el ancho máximo para rellenar (padding)
    max_width = max(len(line) for line in lines)
    height = len(lines)

    # Rellenar con espacios las líneas más cortas para tener una matriz perfecta
    grid = [line.ljust(max_width, " ") for line in lines]

    grand_total = 0

    # Variables temporales para el problema actual
    current_numbers = []
    current_operator = None

    # 2. Iterar columnas de DERECHA a IZQUIERDA
    for x in range(max_width - 1, -1, -1):
        # Extraer la columna actual
        col_chars = [grid[y][x] for y in range(height)]

        # Verificar si es una columna separadora (todo espacios)
        is_separator = all(c == " " for c in col_chars)

        if is_separator:
            # Si encontramos un separador y tenemos números acumulados, resolvemos el problema anterior
            if current_numbers:
                if current_operator == "+":
                    grand_total += sum(current_numbers)
                elif current_operator == "*":
                    grand_total += math.prod(current_numbers)

                # Reiniciar para el siguiente problema
                current_numbers = []
                current_operator = None
            continue

        # Si NO es separador, procesamos la columna

        # A. Extraer el operador (está en la última fila)
        op_char = col_chars[-1]
        if op_char in ["+", "*"]:
            current_operator = op_char

        # B. Extraer el número (está en las filas anteriores, de 0 a height-2)
        # "Most significant digit at the top" -> Leemos de arriba a abajo
        digits = []
        for y in range(height - 1):
            char = col_chars[y]
            if char.isdigit():
                digits.append(char)

        # Si la columna tenía dígitos, formamos el número
        if digits:
            number_str = "".join(digits)
            current_numbers.append(int(number_str))

    # 3. Resolver el último problema pendiente (el que está más a la izquierda)
    if current_numbers:
        if current_operator == "+":
            grand_total += sum(current_numbers)
        elif current_operator == "*":
            grand_total += math.prod(current_numbers)

    print("-" * 40)
    print(f"Gran Total: {grand_total}")
    print("-" * 40)


if __name__ == "__main__":
    resolver_parte_dos(ENTRADA)
