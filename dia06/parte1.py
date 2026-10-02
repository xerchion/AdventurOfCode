"""Advent of Code 2025 · Día 6: Trash Compactor · Parte 1

Cada columna de números se suma o se multiplica según el operador de la última fila; suma los resultados.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

# --- 1. CARGA DE DATOS ---
def carga_datos(fichero):
    datos = []
    with open(fichero, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            partes = linea.split()
            if partes:
                datos.append(partes)
    return datos


def haz_opers(datos):
    # Extraigo la ultima fila, la de los operadaores y la borro de datos
    opers = datos[-1]
    datos = datos[:-1]
    tam = len(opers)
    # bucle general para los operandos (anchura de numeros)
    suma_total = 0
    for i in range(tam):
        producto = 1
        sum_parcial = 0
        for linea in datos:
            if opers[i] == "+":
                sum_parcial += int(linea[i])
            else:
                producto *= int(linea[i])
        # cada columna aporta solo el resultado de su operacion
        if opers[i] == "+":
            suma_total += sum_parcial
        else:
            suma_total += producto

    return suma_total


# 1- carga datos
datos = carga_datos(ENTRADA)
# 2- realiza los calculos
result = haz_opers(datos)

print("TOTAL ", result)
