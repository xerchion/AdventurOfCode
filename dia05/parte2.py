"""Advent of Code 2025 · Día 5: Cafeteria · Parte 2

Cuenta cuántos identificadores distintos cubren los rangos: ordena y fusiona los que se solapan.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

def resolver_parte_dos(fichero):
    rangos = []

    # --- 1. LECTURA ---
    # Solo nos interesan las líneas hasta el espacio en blanco
    with open(fichero, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()
            if not linea:
                break  # ¡Fin de la parte importante!

            # Convertimos "3-5" en tupla (3, 5)
            inicio, fin = map(int, linea.split("-"))
            rangos.append((inicio, fin))

    # --- 2. ORDENACIÓN (CRUCIAL) ---
    # Python ordena las tuplas por su primer elemento automáticamente.
    rangos.sort()

    # --- 3. FUSIÓN DE INTERVALOS ---
    if not rangos:
        return 0

    fusionados = []

    # Metemos el primero para empezar a comparar
    fusionados.append(rangos[0])

    # Recorremos el resto (desde el segundo hasta el final)
    for i in range(1, len(rangos)):
        actual_inicio, actual_fin = rangos[i]
        ultimo_inicio, ultimo_fin = fusionados[-1]

        # ¿Se solapan? (El inicio del actual es menor o igual al fin del último)
        # Nota: Usamos <= porque si uno acaba en 5 y otro empieza en 5, se tocan.
        # Incluso si uno acaba en 5 y el otro empieza en 6, podríamos fusionarlos,
        # pero para contar IDs únicos, basta con mirar solapamiento estricto.
        if actual_inicio <= ultimo_fin:  # Si hay solapamiento o están pegados
            # Nos quedamos con el final más lejano
            nuevo_fin = max(ultimo_fin, actual_fin)
            # Actualizamos el último rango de la lista
            fusionados[-1] = (ultimo_inicio, nuevo_fin)
        else:
            # No se tocan, añadimos el rango nuevo tal cual
            fusionados.append((actual_inicio, actual_fin))

    # --- 4. CÁLCULO FINAL ---
    # Sumamos el tamaño de cada rango fusionado
    total_ids = 0

    for inicio, fin in fusionados:
        # La cantidad de números es (fin - inicio + 1)
        # Ejemplo: 3-5 son 3, 4, 5 (5 - 3 + 1 = 3 números)
        cantidad = fin - inicio + 1
        total_ids += cantidad

    return total_ids


# --- EJECUCIÓN ---
archivo = ENTRADA
resultado = resolver_parte_dos(archivo)

print("-" * 30)
print("TOTAL IDs FRESCOS (PARTE 2):", resultado)
