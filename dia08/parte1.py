"""Advent of Code 2025 · Día 8: Playground · Parte 1

Une los 1000 pares de puntos más cercanos (Union-Find) y multiplica los tamaños de los 3 grupos mayores.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os


# --- Estructura Union-Find (Disjoint Set Union) ---
# Nos ayuda a gestionar grupos conectados de forma muy eficiente.
class UnionFind:
    def __init__(self, n):
        # Al principio, cada nodo es su propio padre (grupo propio)
        self.parent = list(range(n))
        # Cada grupo tiene tamaño 1 inicialmente
        self.size = [1] * n

    def find(self, i):
        # Busca el representante (raíz) del grupo al que pertenece i
        if self.parent[i] != i:
            self.parent[i] = self.find(self.parent[i])  # Compresión de ruta
        return self.parent[i]

    def union(self, i, j):
        # Une los grupos de i y j
        root_i = self.find(i)
        root_j = self.find(j)

        if root_i != root_j:
            # Unimos el grupo más pequeño al más grande
            if self.size[root_i] < self.size[root_j]:
                root_i, root_j = root_j, root_i
            self.parent[root_j] = root_i
            self.size[root_i] += self.size[root_j]
            return True  # Se unieron con éxito
        return False  # Ya estaban en el mismo grupo


def resolver_puzzle_day8(nombre_archivo):
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
            # Parsear "162,817,812" -> [162, 817, 812]
            parts = list(map(int, line.split(",")))
            puntos.append(parts)

    n = len(puntos)
    print(f"Puntos leídos: {n}")

    # 2. Calcular distancias entre TODOS los pares posibles
    # Guardaremos tuplas: (distancia_cuadrada, indice_A, indice_B)
    # Usamos distancia cuadrada para evitar raíces cuadradas (más rápido y preciso para ordenar)
    pares = []
    for i in range(n):
        for j in range(i + 1, n):
            p1 = puntos[i]
            p2 = puntos[j]
            # Distancia Euclídea al cuadrado: (x2-x1)^2 + (y2-y1)^2 + (z2-z1)^2
            dist_sq = (p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2 + (p1[2] - p2[2]) ** 2
            pares.append((dist_sq, i, j))

    # 3. Ordenar por distancia (menor a mayor)
    print("Ordenando pares por distancia...")
    pares.sort(key=lambda x: x[0])

    # 4. Conectar los 1000 pares más cercanos
    uf = UnionFind(n)
    limite_conexiones = 1000

    # Nos aseguramos de no pasarnos si hay menos de 1000 pares totales
    total_a_procesar = min(len(pares), limite_conexiones)

    print(f"Procesando las {total_a_procesar} conexiones más cortas...")

    for k in range(total_a_procesar):
        dist, u, v = pares[k]
        uf.union(u, v)
        # Nota: Si ya estaban conectados, uf.union devuelve False y no hace nada,
        # pero el bucle avanza igual, consumiendo una de las 1000 "acciones".

    # 5. Calcular tamaños de los circuitos resultantes
    # Obtenemos el tamaño del grupo padre de cada nodo
    tamanos_circuitos = []
    raices_procesadas = set()

    for i in range(n):
        raiz = uf.find(i)
        if raiz not in raices_procesadas:
            tamanos_circuitos.append(uf.size[raiz])
            raices_procesadas.add(raiz)

    # 6. Obtener los 3 más grandes y multiplicar
    tamanos_circuitos.sort(reverse=True)

    # Asegurarnos de tener al menos 3 circuitos (rellenar con 1 si hace falta, aunque improbable)
    while len(tamanos_circuitos) < 3:
        tamanos_circuitos.append(1)

    top3 = tamanos_circuitos[:3]
    resultado = top3[0] * top3[1] * top3[2]

    print("-" * 40)
    print(f"Tamaños de los 3 circuitos más grandes: {top3}")
    print(f"Resultado final (multiplicación): {resultado}")
    print("-" * 40)


if __name__ == "__main__":
    resolver_puzzle_day8(ENTRADA)
