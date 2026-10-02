"""Advent of Code 2025 · Día 8: Playground · Parte 2

Sigue uniendo pares por distancia hasta que queda un solo grupo.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os


# --- Estructura Union-Find ---
class UnionFind:
    def __init__(self, n):
        self.parent = list(range(n))
        self.size = [1] * n
        # Mantenemos un contador de cuántos grupos aislados quedan
        self.num_groups = n

    def find(self, i):
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Compresión de ruta
        return self.parent[i]

    def union(self, i, j):
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Unimos los grupos
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]

            # Reducimos el contador de grupos totales
            self.num_groups -= 1
            return True  # Indica que se realizó una unión exitosa
        return False  # Ya estaban conectados


def resolver_parte_dos_day8(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    # 1. Leer las coordenadas
    puntos = []
    with open(nombre_archivo, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue
            # Parsear [X, Y, Z]
            parts = list(map(int, line.split(",")))
            puntos.append(parts)

    n = len(puntos)
    print(f"Puntos leídos: {n}")

    # 2. Calcular distancias entre TODOS los pares posibles
    # Guardamos: (distancia_cuadrada, indice_A, indice_B)
    pares = []
    for i in range(n):
        for j in range(i + 1, n):
            p1 = puntos[i]
            p2 = puntos[j]
            dist_sq = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
            pares.append((dist_sq, i, j))

    # 3. Ordenar por distancia (de menor a mayor)
    # Esto es crucial: queremos conectar siempre los más cercanos primero
    print("Ordenando pares por distancia...")
    pares.sort(key=lambda x: x[0])

    # 4. Conectar hasta que quede UN SOLO circuito
    uf = UnionFind(n)

    print("Conectando circuitos...")

    for dist, u, v in pares:
        # Intentamos unir los nodos u y v
        se_unieron = uf.union(u, v)

        if se_unieron:
            # Si se unieron, verificamos si ya hemos alcanzado el objetivo
            # El objetivo es que num_groups sea 1
            if uf.num_groups == 1:
                # ¡Esta fue la última conexión necesaria!
                x1 = puntos[u][0]
                x2 = puntos[v][0]
                resultado = x1 * x2

                print("-" * 40)
                print("¡Circuito completo alcanzado!")
                # print("Última conexión entre nodo {u} (X={x1}) y nodo {v} (X={x2})")
                print("Resultado final (X1 * X2): ", resultado)
                print("-" * 40)
                return

    print(
        "Se recorrieron todos los pares y no se unificó el circuito (algo raro pasó)."
    )


if __name__ == "__main__":
    resolver_parte_dos_day8(ENTRADA)
