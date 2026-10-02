"""Advent of Code 2025 · Día 1: Secret Entrance · Parte 2

Cuenta cuántas veces pasa el dial por 0, también en mitad de una rotación.

Uso: python parte2.py [fichero]
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
        veces = 0
        rot = linea[0]
        num = int(linea[1:])
        pos_anterior = pos_absoluta
        if rot == "L":
            pos_absoluta -= num
            # múltiplos de 100 que quedan entre la posición nueva y la anterior
            veces = ((pos_anterior - 1) // 100) - ((pos_absoluta - 1) // 100)
        if rot == "R":
            pos_absoluta += num
            veces = (pos_absoluta // 100) - (pos_anterior // 100)

        result += veces
print("El resultado es: ", result)
