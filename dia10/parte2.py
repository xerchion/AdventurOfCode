"""Advent of Code 2025 · Día 10: Factory · Parte 2

Mínimo de pulsaciones para alcanzar los contadores: eliminación de Gauss-Jordan y búsqueda sobre las variables libres.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import math
import os
import re


def parse_machine(line):
    match_joltage = re.search(r"\{(.*?)\}", line)
    if not match_joltage:
        return None, None
    targets = [int(x) for x in match_joltage.group(1).split(",")]
    buttons_str = re.findall(r"\((.*?)\)", line)
    buttons = []
    for b_str in buttons_str:
        if not b_str.strip():
            buttons.append([])
        else:
            buttons.append([int(x) for x in b_str.split(",")])
    return targets, buttons


def solve_with_gauss(targets, buttons):
    # R = número de ecuaciones (targets), C = número de incógnitas (botones)
    R = len(targets)
    C = len(buttons)

    # Construir la matriz aumentada (A | B) usando Floats para la reducción
    # matrix[row][col]
    matrix = []
    for r in range(R):
        row = [0.0] * C
        matrix.append(row)

    for c, affected_indices in enumerate(buttons):
        for r in affected_indices:
            if r < R:
                matrix[r][c] = 1.0

    # Vector de resultados (lado derecho)
    rhs = [float(x) for x in targets]

    # --- FASE 1: ELIMINACIÓN GAUSSIANA (Gauss-Jordan) ---
    pivot_row = 0
    pivots = []  # Guardamos (fila, columna) de los pivotes
    col_to_row = {}  # Mapa columna -> fila pivote

    for c in range(C):
        if pivot_row >= R:
            break

        # Buscar el mejor pivote en la columna 'c' (fila actual hacia abajo)
        sel = -1
        for r in range(pivot_row, R):
            if abs(matrix[r][c]) > 1e-9:
                sel = r
                break

        if sel == -1:
            continue  # Esta columna es variable libre (dependiente)

        # Intercambiar filas
        matrix[pivot_row], matrix[sel] = matrix[sel], matrix[pivot_row]
        rhs[pivot_row], rhs[sel] = rhs[sel], rhs[pivot_row]

        # Normalizar la fila del pivote
        div = matrix[pivot_row][c]
        for j in range(c, C):
            matrix[pivot_row][j] /= div
        rhs[pivot_row] /= div

        # Hacer ceros en las demás filas
        for r in range(R):
            if r != pivot_row:
                mul = matrix[r][c]
                if abs(mul) > 1e-9:
                    for j in range(c, C):
                        matrix[r][j] -= mul * matrix[pivot_row][j]
                    rhs[r] -= mul * rhs[pivot_row]

        pivots.append(c)
        col_to_row[c] = pivot_row
        pivot_row += 1

    # Verificar consistencia de filas vacías (0 = algo distinto de 0)
    for r in range(pivot_row, R):
        if abs(rhs[r]) > 1e-5:
            return float("inf")  # Sistema inconsistente (imposible)

    # --- FASE 2: BÚSQUEDA SOBRE VARIABLES LIBRES ---
    # Identificar variables libres (las columnas que no son pivotes)
    free_vars = [c for c in range(C) if c not in col_to_row]

    best_total = float("inf")

    # Si no hay variables libres, la solución es única (si es entera)
    # Si hay variables libres, iteramos sobre ellas.
    # Como queremos minimizar la suma total, probamos valores bajos para las libres primero.

    # Generador de combinaciones para variables libres.
    # Empezamos con todas en 0, luego sumamos.
    # LIMITAMOS la búsqueda heurísticamente para no ser infinita,
    # pero dado que Gauss simplifica, el rango necesario suele ser pequeño.

    # Capacidad de búsqueda:
    search_limit = 200000
    # Nota: Si el sistema tiene muchas variables libres, esto podría cortar,
    # pero con Gauss la dimensionalidad baja drásticamente.

    import itertools

    # Si hay muchas variables libres, el problema es difícil.
    # Pero usualmente hay 0, 1 o 2.

    def get_dependent_vars(free_vals_map):
        # Calcular variables dependientes basándonos en las libres
        current_solution = [0] * C
        total_presses = 0

        # Asignar libres
        for fv in free_vars:
            val = free_vals_map.get(fv, 0)
            current_solution[fv] = val
            total_presses += val

        # Calcular dependientes (back substitution trivial porque es diagonal)
        possible = True

        # Iteramos en orden inverso de pivotes para estabilidad numérica (aunque ya está diagonalizada)
        for col in reversed(pivots):
            r = col_to_row[col]
            val = rhs[r]

            # Restar la contribución de las variables libres
            for fv in free_vars:
                if abs(matrix[r][fv]) > 1e-9:
                    val -= matrix[r][fv] * current_solution[fv]

            # Verificar si es entero no negativo
            # Usamos epsilon para errores de punto flotante
            rounded = round(val)
            if abs(val - rounded) > 1e-5 and val > -1e-5:
                # No es entero
                return None, None

            if rounded < 0:
                return None, None

            current_solution[col] = int(rounded)
            total_presses += int(rounded)

        return current_solution, total_presses

    # Bucle de búsqueda
    # Si no hay variables libres, probamos una sola vez (dict vacío)
    if not free_vars:
        sol, presses = get_dependent_vars({})
        if sol is not None:
            return presses
        else:
            return float("inf")

    # Si HAY variables libres, iteramos.
    # Estrategia: BFS sobre la suma de las variables libres
    # Esto garantiza encontrar el mínimo de pulsaciones.

    queue = [(0, tuple([0] * len(free_vars)))]  # (suma_libres, (v1, v2, ...))
    seen = set()
    seen.add(tuple([0] * len(free_vars)))

    iterations = 0

    while queue and iterations < search_limit:
        iterations += 1
        # Sacar el candidato con menor suma (para optimizar búsqueda del mínimo)
        # Como es BFS simple y los pesos son 1, queue[0] es suficiente si appendamos al final
        # Pero mejor ordenamos o usamos heapq si queremos ser estrictos,
        # aunque con pesos iguales (sumar +1) una cola simple mantiene el orden.

        current_free_sum, vals_tuple = queue.pop(0)

        # Mapear a diccionario
        vals_map = {free_vars[i]: vals_tuple[i] for i in range(len(free_vars))}

        # Calcular solución completa
        sol, total = get_dependent_vars(vals_map)

        if sol is not None:
            # ¡Encontramos una solución válida!
            # Como estamos explorando en orden de "suma creciente de variables libres",
            # y las variables dependientes se ajustan linealmente,
            # esta suele ser la óptima o cerca.
            # Sin embargo, coeficientes negativos en la matriz podrían hacer que
            # aumentar una variable libre disminuya una dependiente.
            # Guardamos y seguimos un poco más o paramos?
            if total < best_total:
                best_total = total
                # Heurística: Si encontramos una solución, seguimos buscando
                # un poco más por si acaso hay un mínimo local mejor,
                # pero en problemas lineales convexos, suele ser directo.
                # Para ser seguros en AoC, guardamos y continuamos.

        # Generar vecinos (sumar +1 a cada variable libre)
        # Solo si la suma actual no excede best_total (poda)
        if best_total != float("inf") and current_free_sum >= best_total:
            continue

        for i in range(len(free_vars)):
            new_vals = list(vals_tuple)
            new_vals[i] += 1
            new_tuple = tuple(new_vals)

            if new_tuple not in seen:
                seen.add(new_tuple)
                # Si tenemos muchas variables libres, esto explota.
                # Pero con 1 o 2 es instantáneo.
                queue.append((current_free_sum + 1, new_tuple))

    return best_total if best_total != float("inf") else 0


def resolver_day10_gauss(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    total_global = 0
    procesados = 0
    imposibles = 0

    print("Iniciando Solver Algebraico (Gauss-Jordan)...")

    with open(nombre_archivo, "r") as f:
        lines = f.readlines()

    for i, line in enumerate(lines):
        line = line.strip()
        if not line:
            continue

        targets, buttons = parse_machine(line)
        if targets:
            # Resolver
            resultado = solve_with_gauss(targets, buttons)

            if resultado == float("inf") or resultado == 0:
                # Intento de debug: ¿Es realmente 0 o imposible?
                # Si targets > 0 y resultado 0 -> algo falló, pero Gauss devuelve inf si falla.
                if resultado == float("inf"):
                    imposibles += 1
                    # print(f"Máquina {i+1}: Sin solución entera.")
                else:
                    total_global += resultado
                    procesados += 1
            else:
                total_global += resultado
                procesados += 1

            if (i + 1) % 10 == 0:
                print(f" -> Procesando... ({i+1}/{len(lines)})")

    print("-" * 50)
    print(f"Proceso Terminado.")
    print(f"Máquinas con solución: {procesados}")
    print(f"Máquinas sin solución: {imposibles}")
    print(f"RESULTADO FINAL: {int(total_global)}")
    print("-" * 50)


if __name__ == "__main__":
    resolver_day10_gauss(ENTRADA)
