"""Advent of Code 2025 · Día 2: Gift Shop · Parte 2

Suma los identificadores formados por un patrón repetido dos o más veces.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

result = 0
suma = 0
todos = []

# --- PARTE 1: LECTURA DEL ARCHIVO (Igual que tenías) ---
with open(ENTRADA, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        elementos = linea.strip().split(",")
        for elemento in elementos:
            if elemento != "":
                todos.append(elemento)

# --- PARTE 2: PROCESAMIENTO ---
print("Procesando rangos...")

for elemento in todos:
    # Limpieza y separación
    partes = elemento.strip().split("-")
    if not partes or partes == ['']: continue # Saltamos vacíos

    initial = int(partes[0])
    end = int(partes[1])

    # Recorremos cada número del rango
    for num in range(initial, end + 1):
        alfa = str(num)
        size = len(alfa)
        sumalo = False # Bandera para saber si encontramos patrón

        # Probamos longitudes de patrón posibles.
        # Un patrón debe medir al menos 1, y como mucho la mitad del string total.
        # (Porque tiene que repetirse al menos 2 veces).
        for longitud_patron in range(1, (size // 2) + 1):

            # 1. Optimización: Si el tamaño total no es divisible por el patrón,
            #    es imposible que se repita perfectamente. Saltamos.
            if size % longitud_patron != 0:
                continue

            # 2. Extraemos el candidato a patrón (el trocito inicial)
            patron = alfa[0:longitud_patron]

            # 3. Calculamos cuántas veces debería repetirse
            veces = size // longitud_patron

            # 4. TRUCO DE PYTHON: Multiplicamos el string y comparamos
            #    Ej: Si patron es "12" y veces es 3 -> "12" * 3 crea "121212"
            reconstruido = patron * veces

            if reconstruido == alfa:
                sumalo = True
                break # ¡Encontrado! No hace falta buscar más patrones en este número

        if sumalo:
            suma += num
            result += 1
            # print(f"Encontrado: {num}") # Descomenta si quieres verlos

print("-" * 30)
print("RESULTADO FINAL")
print("Cantidad encontrados:", result)
print("Suma total:", suma)
