"""Advent of Code 2025 · Día 1: Secret Entrance · Parte 1

Cuenta cuántas veces queda el dial apuntando a 0 al terminar una rotación.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

result = 0
pos_absoluta = 50
with open(ENTRADA, "r", encoding="utf-8") as file:

    for linea in file:
        linea = linea.strip()
        if not linea:
            continue
        rot = linea[0]
        num = int(linea[1:])
        if rot == "L":
            pos_absoluta -= num
        if rot == "R":
            pos_absoluta += num

        if pos_absoluta % 100 == 0:
            result = result + 1
print("El resultado es: ", result)
