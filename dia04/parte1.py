"""Advent of Code 2025 · Día 4: Printing Department · Parte 1

Cuenta los rollos de la rejilla que tienen menos de 4 rollos entre sus 8 vecinos.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

result = 0
tabla = []

# --- 1. CARGA DE DATOS ---
with open(ENTRADA, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        # list(string) convierte "abc" en ['a', 'b', 'c'] automáticamente
        tabla.append(list(linea.strip()))

# Obtenemos dimensiones
filas_total = len(tabla)
cols_total = len(tabla[0])

# --- 2. DEFINIMOS LOS 8 VECINOS (DELTAS) ---
# Son las coordenadas relativas: (cambio_fila, cambio_columna)
# Ejemplo: (-1, 0) es mirar arriba. (1, 1) es abajo-derecha.
deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

print(f"Dimensiones: {filas_total} filas x {cols_total} columnas")

# --- 3. RECORREMOS TODO EL MAPA ---
for f in range(filas_total):
    for c in range(cols_total):

        # Si NO es un rollo de papel, pasamos al siguiente inmediatamente
        if tabla[f][c] != "@":
            continue

        # Si ES un rollo, contamos sus vecinos
        vecinos_ocupados = 0

        for df, dc in deltas:
            # Calculamos la coordenada del vecino
            vecino_f = f + df
            vecino_c = c + dc

            # --- AQUÍ ESTÁ LA MAGIA ---
            # Verificamos si esa coordenada es válida (está dentro del mapa)
            dentro_f = 0 <= vecino_f < filas_total
            dentro_c = 0 <= vecino_c < cols_total

            if dentro_f and dentro_c:
                # Solo si es válida, miramos qué hay dentro
                if tabla[vecino_f][vecino_c] == "@":
                    vecinos_ocupados += 1

        # --- 4. APLICAMOS LA REGLA ---
        # "Menos de 4 rollos vecinos" significa accesible
        if vecinos_ocupados < 4:
            result += 1
            # Opcional: Marcar en el mapa para verlo visualmente
            # tabla[f][c] = "X"

print("-" * 30)
print("Rollos accesibles encontrados:", result)

# Si quieres ver el mapa final
# for fila in tabla:
#     print("".join(fila))
