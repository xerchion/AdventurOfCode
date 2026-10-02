"""Advent of Code 2025 · Día 2: Gift Shop · Parte 1

Suma los identificadores cuyas dos mitades son iguales (por ejemplo, 123123).

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

result = 0
suma = 0
todos = []
with open(ENTRADA, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        # 1. strip() elimina espacios y saltos de línea al inicio/final
        # 2. split(',') corta la linea cada vez que ve una coma
        elementos = linea.strip().split(",")
        for elemento in elementos:
            if elemento != "":
                todos.append(elemento)

        # Cogemos cada par de numeros
for elemento in todos:
    # Dividimos de cada elemento sus partes, inicial y final
    partes = elemento.strip().split("-")
    # Cada parte la pasamos a entero
    initial = int(partes[0]) if partes[0] != "" else 0
    end = int(partes[1]) if partes[1] != "" else 0
    for num in range(initial, end + 1):
        alfa = str(num)
        size = len(alfa)
        if size % 2 == 0:
            half = size // 2
            if alfa[0:half] == alfa[half:]:
                # Los numero son iguales, por lo tanto es NO valido
                # asi que se suma
                result = result + 1
                suma = suma + num

print("suma: ", suma)
