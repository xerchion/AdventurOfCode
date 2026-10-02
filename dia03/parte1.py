"""Advent of Code 2025 · Día 3: Lobby · Parte 1

En cada fila elige dos dígitos, en orden, que formen el mayor número posible, y suma los resultados.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

result = 0
izda_max = dcha_max = 0
# 1 extraer datos
with open(ENTRADA, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        # inicializacion por linea
        izda_max = dcha_max = 0
        izda_index = dcha_indez = 0
        # quitar el salto de linea
        linea = linea.strip()
        if not linea:
            continue
        # extraer tamaño
        tam = len(linea)
        # extraer maximo izdo
        # bucle sin el ultimo elemento
        for i in range(0, tam - 1):
            # ver que saca los 15
            # print(i)
            # obtener izda max
            num = int(linea[i])
            if num > izda_max:
                izda_max = num
                izda_index = i
        # extraer maximo derecho
        # bucle con el ultimo elemento
        for i in range(izda_index + 1, tam):
            # ver que saca los que faltan
            # print(i)
            # obtener dcha max
            num = int(linea[i])
            if num > dcha_max:
                dcha_max = num
                dcha_indez = i
        # juntar numero
        numero = int(str(izda_max) + str(dcha_max))
        # mostrar numero
        # print("numero :", numero)
        # sumar a resultado
        result = result + numero

print("resultado ", result)
