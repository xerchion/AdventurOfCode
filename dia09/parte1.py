"""Advent of Code 2025 · Día 9: Movie Theater · Parte 1

Mayor rectángulo con dos puntos de la lista como esquinas opuestas.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os


def resolver_day9(nombre_archivo):
    # 1. Verificar archivo
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    # 2. Leer coordenadas
    puntos = []
    with open(nombre_archivo, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parsear "7,1" -> [7, 1]
            try:
                parts = list(map(int, line.split(",")))
                if len(parts) == 2:
                    puntos.append(parts)
            except ValueError:
                continue

    n = len(puntos)
    print(f"Baldosas rojas encontradas: {n}")

    if n < 2:
        print("Necesitas al menos 2 puntos para formar un rectángulo.")
        return

    max_area = 0
    mejor_par = (None, None)

    # 3. Fuerza bruta: Comparar cada punto con todos los demás
    # Como N suele ser pequeño (unos cientos o pocos miles), esto es muy rápido.
    for i in range(n):
        for j in range(i + 1, n):
            p1 = puntos[i]
            p2 = puntos[j]

            # Calcular ancho y alto (recordando el +1 porque es inclusivo)
            ancho = abs(p1[0] - p2[0]) + 1
            alto = abs(p1[1] - p2[1]) + 1

            area = ancho * alto

            if area > max_area:
                max_area = area
                mejor_par = (p1, p2)

    # 4. Resultado
    print("-" * 40)
    if mejor_par[0]:
        print(f"Mejor par encontrado: {mejor_par[0]} y {mejor_par[1]}")
    print(f"El área del rectángulo más grande es: {max_area}")
    print("-" * 40)


if __name__ == "__main__":
    resolver_day9(ENTRADA)
