"""Advent of Code 2025 · Día 12: Christmas Tree Farm · Parte 1

Decide en qué regiones caben todas las piezas, con rotaciones y simetrías: vuelta atrás.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import sys

# Aumentar límite de recursión por seguridad
sys.setrecursionlimit(2000)


def parse_input(filename):
    with open(filename, "r") as f:
        content = f.read().strip()

    parts = content.split("\n\n")

    # 1. Parsear las formas (Shapes)
    shapes_raw = []
    regions_raw = []

    parsing_shapes = True
    for block in parts:
        # Detectar si hemos llegado a la sección de regiones (contiene 'x' como 12x5)
        if "x" in block.split(":")[0]:
            parsing_shapes = False

        if parsing_shapes:
            lines = block.split("\n")
            # El formato es "ID:" seguido de la forma
            # A veces el bloque puede tener la cabecera en la misma linea o no, normalizamos
            # Buscamos donde empieza el dibujo
            grid_lines = []
            for line in lines:
                if ":" in line:
                    continue
                if line.strip():
                    grid_lines.append(line.strip())

            # Convertir grid a coordenadas
            coords = set()
            for r, row in enumerate(grid_lines):
                for c, char in enumerate(row):
                    if char == "#":
                        coords.add((r, c))
            shapes_raw.append(coords)
        else:
            # Es una región o lista de regiones
            lines = block.split("\n")
            for line in lines:
                if line.strip():
                    regions_raw.append(line.strip())

    return shapes_raw, regions_raw


# --- Geometría y Normalización ---


def normalize(coords):
    """Mueve la forma para que empiece en 0,0 y sea un set inmutable (frozenset)"""
    if not coords:
        return frozenset()
    min_r = min(r for r, c in coords)
    min_c = min(c for r, c in coords)
    return frozenset((r - min_r, c - min_c) for r, c in coords)


def rotate(coords):
    """Rota 90 grados horario"""
    return set((c, -r) for r, c in coords)


def flip(coords):
    """Espejo horizontal"""
    return set((r, -c) for r, c in coords)


def get_variants(base_shape_coords):
    """Genera todas las rotaciones y flips únicos"""
    variants = set()
    current = base_shape_coords

    # 4 rotaciones
    for _ in range(4):
        variants.add(normalize(current))  # Normal
        variants.add(normalize(flip(current)))  # Flippeada
        current = rotate(current)

    # Convertir a lista de listas para iterar fácil
    # Cada variante es un set de (r,c) con dimensiones calculadas
    final_variants = []
    for var in variants:
        max_r = max(r for r, c in var)
        max_c = max(c for r, c in var)
        final_variants.append({"coords": var, "height": max_r + 1, "width": max_c + 1})
    return final_variants


# --- Solver ---


def solve(width, height, pieces_to_fit, all_variants):
    """
    width, height: dimensiones de la región
    pieces_to_fit: lista de IDs de piezas [0, 4, 4, 5...] (deben estar ordenadas para optimizar)
    all_variants: diccionario {id: [variantes...]}
    """

    # Grid representado como un set de coordenadas ocupadas
    occupied = set()

    # Ordenamos piezas: Las más grandes primero (heurística crítica)
    # Calculamos el área de cada pieza para ordenar
    pieces_with_size = []
    for pid in pieces_to_fit:
        # Cualquier variante sirve para ver el tamaño (área es constante)
        area = len(all_variants[pid][0]["coords"])
        pieces_with_size.append((area, pid))

    # Ordenar por área descendente
    pieces_with_size.sort(key=lambda x: x[0], reverse=True)
    sorted_pieces = [p[1] for p in pieces_with_size]

    # Verificación rápida de área total
    total_area_pieces = sum(p[0] for p in pieces_with_size)
    if total_area_pieces > width * height:
        return False

    n_pieces = len(sorted_pieces)

    def backtrack(idx, current_occupied):
        # Caso base: todas las piezas colocadas
        if idx == n_pieces:
            return True

        pid = sorted_pieces[idx]
        variants = all_variants[pid]

        # Poda por simetría:
        # Si la pieza actual es IGUAL a la anterior (mismo ID y mismo tamaño),
        # podemos forzar un orden para evitar probar (A, B) y (B, A) si A==B.
        # (Implementación simplificada: simplemente probamos todas las posiciones válidas)

        # Iterar sobre todas las celdas del grid
        # Nota: Esto puede ser lento. Una optimización común es encontrar la primera celda libre
        # y forzar a que la pieza cubra esa celda. PERO esto solo vale si queremos LLENAR el grid (Exact Cover).
        # Aquí pueden sobrar espacios. Así que iteramos posiciones.

        for r in range(height):
            for c in range(width):
                # Optimización: Si la celda está ocupada, no podemos poner la 'esquina' de la pieza aquí.
                # (Aunque la pieza podría tener un hueco en 0,0, hemos normalizado al bounding box,
                # pero no necesariamente el 0,0 de la pieza tiene un bloque. Sin embargo, normalize()
                # asegura que min_r y min_c sean 0, así que al menos hay UN bloque en fila 0 y UN bloque en col 0).

                # Intentar cada variante
                for var in variants:
                    v_h = var["height"]
                    v_w = var["width"]
                    v_coords = var["coords"]

                    # Chequeo de límites del bounding box
                    if r + v_h > height or c + v_w > width:
                        continue

                    # Chequeo de colisiones
                    # Calculamos las coordenadas absolutas de la pieza
                    abs_coords = set()
                    collision = False
                    for vr, vc in v_coords:
                        nr, nc = r + vr, c + vc
                        if (nr, nc) in current_occupied:
                            collision = True
                            break
                        abs_coords.add((nr, nc))

                    if not collision:
                        # Colocar pieza
                        # Optimizacion de estado: usamos un set nuevo o modificamos/restauramos
                        # Modificar es más rápido en Python si se hace con cuidado
                        current_occupied.update(abs_coords)

                        if backtrack(idx + 1, current_occupied):
                            return True

                        # Backtrack: quitar pieza
                        current_occupied.difference_update(abs_coords)

        return False

    return backtrack(0, occupied)


def main():
    try:
        shapes_raw, regions_raw = parse_input(ENTRADA)
    except FileNotFoundError:
        print(f"Error: No se encuentra '{ENTRADA}'")
        return

    # 1. Preprocesar variantes de todas las formas
    all_variants = {}
    for i, shape in enumerate(shapes_raw):
        all_variants[i] = get_variants(shape)

    success_count = 0
    total_regions = len(regions_raw)

    print(f"Procesando {total_regions} regiones...")

    for i, line in enumerate(regions_raw):
        # Formato: "12x5: 1 0 1 0 2 2"
        dims_part, counts_part = line.split(":")
        w_str, h_str = dims_part.strip().split("x")
        W, H = int(w_str), int(h_str)

        counts = list(map(int, counts_part.strip().split()))

        # Expandir la lista de piezas: si dice "2" en el índice 4, añadimos [4, 4]
        pieces_to_fit = []
        for pid, count in enumerate(counts):
            pieces_to_fit.extend([pid] * count)

        if solve(W, H, pieces_to_fit, all_variants):
            success_count += 1
            # print(f"Region {i+1}: SÍ cabe")
        else:
            # print(f"Region {i+1}: NO cabe")
            pass

        if (i + 1) % 5 == 0:
            print(f" -> Progreso: {i+1}/{total_regions}")

    print("-" * 40)
    print(f"Total regiones válidas: {success_count}")
    print("-" * 40)


if __name__ == "__main__":
    main()
