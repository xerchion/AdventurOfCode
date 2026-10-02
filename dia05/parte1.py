"""Advent of Code 2025 · Día 5: Cafeteria · Parte 1

Cuenta cuántos identificadores caen dentro de alguno de los rangos.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

def procesar_archivo(fichero):
    rangos_frescos = []  # Guardaremos tuplas (inicio, fin)
    ids_a_comprobar = []

    leyendo_rangos = True  # Bandera para saber en qué parte del archivo estamos

    with open(fichero, "r", encoding="utf-8") as archivo:
        for linea in archivo:
            linea = linea.strip()

            # Si la línea está vacía, cambiamos de sección
            if not linea:
                leyendo_rangos = False
                continue

            if leyendo_rangos:
                # Parte 1: Guardamos las reglas (inicio, fin)
                # Ejemplo linea: "3-5"
                inicio, fin = map(int, linea.split("-"))
                rangos_frescos.append((inicio, fin))
            else:
                # Parte 2: Guardamos los IDs a verificar
                # Ejemplo linea: "10"
                ids_a_comprobar.append(int(linea))

    return rangos_frescos, ids_a_comprobar


def contar_frescos(rangos, candidatos):
    total_frescos = 0

    print(f"Verificando {len(candidatos)} ingredientes contra {len(rangos)} rangos...")

    for id_ingrediente in candidatos:
        es_fresco = False

        # Recorremos la lista de reglas
        for inicio, fin in rangos:
            # MAGIA MATEMÁTICA: Comprobación directa sin sets gigantes
            if inicio <= id_ingrediente <= fin:
                es_fresco = True
                break  # Si ya encontramos que es fresco, no hace falta mirar más rangos

        if es_fresco:
            total_frescos += 1

    return total_frescos


# --- EJECUCIÓN ---
archivo = ENTRADA

# 1. Carga y procesado en un solo paso eficiente
rangos, candidatos = procesar_archivo(archivo)

# 2. Conteo matemático
resultado = contar_frescos(rangos, candidatos)

print("-" * 30)
print("TOTAL INGREDIENTES FRESCOS:", resultado)
