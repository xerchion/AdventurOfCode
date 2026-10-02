"""Advent of Code 2025 · Día 4: Printing Department · Parte 2

Retira por rondas los rollos accesibles hasta que no quede ninguno, y cuenta los retirados.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

total_eliminados = 0
tabla = []

# --- 1. CARGA DE DATOS ---
with open(ENTRADA, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        tabla.append(list(linea.strip()))

filas_total = len(tabla)
cols_total = len(tabla[0])

# Direcciones (Deltas) para mirar vecinos
deltas = [(-1, -1), (-1, 0), (-1, 1), (0, -1), (0, 1), (1, -1), (1, 0), (1, 1)]

print(f"Mapa inicial: {filas_total}x{cols_total}")

# --- 2. BUCLE DE SIMULACIÓN (El cambio principal) ---
ronda = 1
hubo_cambios = True

while hubo_cambios:
    # Asumimos que no habrá cambios hasta que encontremos uno
    hubo_cambios = False
    para_borrar = []  # La "Lista de la Muerte" de esta ronda

    # A) ESCANEO: Buscamos candidatos SIN borrar nada todavía
    for f in range(filas_total):
        for c in range(cols_total):

            # Solo miramos rollos de papel vivos
            if tabla[f][c] == "@":
                vecinos = 0
                for df, dc in deltas:
                    vf, vc = f + df, c + dc

                    # Chequeo de bordes y si es vecino
                    if 0 <= vf < filas_total and 0 <= vc < cols_total:
                        if tabla[vf][vc] == "@":
                            vecinos += 1

                # Regla: Si tiene menos de 4 vecinos, A LA LISTA
                if vecinos < 4:
                    para_borrar.append((f, c))

    # B) ACTUALIZACIÓN: Ahora sí borramos todos de golpe
    cantidad = len(para_borrar)

    if cantidad > 0:
        print(f"Ronda {ronda}: Se eliminan {cantidad} rollos.")
        total_eliminados += cantidad
        hubo_cambios = True  # ¡Seguimos jugando!
        ronda += 1

        # Ejecutamos la eliminación
        for f, c in para_borrar:
            tabla[f][c] = "."  # Lo convertimos en aire/suelo
    else:
        print("Fin de la simulación. Ya no se puede acceder a más rollos.")

print("-" * 30)
print("TOTAL ROLLOS ELIMINADOS:", total_eliminados)
