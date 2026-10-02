"""Advent of Code 2025 · Día 11: Reactor · Parte 1

Cuenta los caminos entre dos nodos de un grafo dirigido con búsqueda en profundidad y memoria.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os
import sys

# Aumentamos el límite de recursión por seguridad,
# aunque para este tipo de grafos no suele ser tan profundo.
sys.setrecursionlimit(20000)


def resolver_day11(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    # 1. Construir el Grafo (Lista de Adyacencia)
    # graph = { 'nodo_origen': ['destino1', 'destino2'], ... }
    graph = {}

    with open(nombre_archivo, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Formato: "aaa: you hhh"
            if ":" in line:
                source, dests_str = line.split(":")
                source = source.strip()
                # Separar los destinos por espacio
                dests = [d.strip() for d in dests_str.strip().split(" ") if d.strip()]
                graph[source] = dests

    # 2. Algoritmo de Búsqueda con Memorización (DFS + Memo)
    # memo guardará el número de caminos desde un nodo X hasta 'out'
    memo = {}

    def contar_caminos(nodo_actual):
        # CASO BASE 1: Llegamos al final
        if nodo_actual == "out":
            return 1

        # CASO BASE 2: Ya hemos calculado este nodo antes
        if nodo_actual in memo:
            return memo[nodo_actual]

        # CASO BASE 3: Es un callejón sin salida (no es 'out' y no tiene conexiones)
        if nodo_actual not in graph:
            return 0

        # RECURSIÓN: Sumar los caminos de todos los vecinos
        total_paths = 0
        for vecino in graph[nodo_actual]:
            total_paths += contar_caminos(vecino)

        # Guardamos en caché y devolvemos
        memo[nodo_actual] = total_paths
        return total_paths

    # 3. Ejecutar desde 'you'
    if "you" not in graph:
        print("Error: No se encontró el punto de partida 'you' en el archivo.")
        return

    resultado = contar_caminos("you")

    print("-" * 40)
    print(f"Grafo cargado con {len(graph)} dispositivos.")
    print(f"Número total de caminos desde 'you' hasta 'out': {resultado}")
    print("-" * 40)


if __name__ == "__main__":
    resolver_day11(ENTRADA)
