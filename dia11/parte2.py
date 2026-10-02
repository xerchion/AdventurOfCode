"""Advent of Code 2025 · Día 11: Reactor · Parte 2

Cuenta los caminos que pasan por dos nodos obligatorios multiplicando los caminos de cada tramo.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os
import sys

# Aumentamos el límite de recursión
sys.setrecursionlimit(20000)


def resolver_day11_part2(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    # 1. Construir el Grafo
    graph = {}
    with open(nombre_archivo, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            # Formato: "aaa: bbb ccc"
            if ":" in line:
                source, dests_str = line.split(":")
                source = source.strip()
                dests = [d.strip() for d in dests_str.strip().split(" ") if d.strip()]
                graph[source] = dests

    # 2. Función Genérica para contar caminos entre A y B
    # Creamos una función que genere su propia memoria (memo) cada vez que se llama
    def contar_entre(origen, destino):
        memo = {}

        def dfs(actual):
            # Si llegamos al destino, cuenta como 1 camino válido
            if actual == destino:
                return 1

            # Si ya lo calculamos, devolver valor guardado
            if actual in memo:
                return memo[actual]

            # Si es callejón sin salida
            if actual not in graph:
                return 0

            total = 0
            for vecino in graph[actual]:
                total += dfs(vecino)

            memo[actual] = total
            return total

        # Si el origen no existe en el grafo, no hay caminos
        if origen not in graph and origen != destino:
            return 0

        return dfs(origen)

    # 3. Calcular los segmentos clave
    print("Calculando segmentos...")

    # Opción A: svr -> dac -> fft -> out
    tramo_A1 = contar_entre("svr", "dac")
    tramo_A2 = contar_entre("dac", "fft")
    tramo_A3 = contar_entre("fft", "out")
    total_A = tramo_A1 * tramo_A2 * tramo_A3

    # Opción B: svr -> fft -> dac -> out
    tramo_B1 = contar_entre("svr", "fft")
    tramo_B2 = contar_entre("fft", "dac")
    tramo_B3 = contar_entre("dac", "out")
    total_B = tramo_B1 * tramo_B2 * tramo_B3

    # Resultado final
    total_final = total_A + total_B

    print("-" * 40)
    print(
        f"Opción A (svr->dac->fft->out): {tramo_A1} * {tramo_A2} * {tramo_A3} = {total_A}"
    )
    print(
        f"Opción B (svr->fft->dac->out): {tramo_B1} * {tramo_B2} * {tramo_B3} = {total_B}"
    )
    print(f"Total de caminos que pasan por ambos: {total_final}")
    print("-" * 40)


if __name__ == "__main__":
    resolver_day11_part2(ENTRADA)
