"""Advent of Code 2025 · Día 3: Lobby · Parte 2

Igual que la parte 1, pero eligiendo 12 dígitos por fila: selección voraz con una pila.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

total_joltage = 0

print("--- Iniciando Cálculo ---")

with open(ENTRADA, "r", encoding="utf-8") as archivo:
    for linea in archivo:
        linea = linea.strip()  # Limpia espacios y saltos de linea
        if not linea:
            continue  # Saltamos lineas vacias

        # 1. Configuración del juego
        longitud_objetivo = 12
        # Calculamos cuántos números PODEMOS borrar
        vidas_para_borrar = len(linea) - longitud_objetivo

        pila = []

        # 2. Bucle principal (Greedy)
        for digito in linea:
            # Mientras:
            # a) Nos queden "vidas" para borrar (vidas_para_borrar > 0)
            # b) Tengamos algo en la pila (pila)
            # c) El número que tenemos en la mano (digito) sea MAYOR que el último de la pila
            while vidas_para_borrar > 0 and pila and pila[-1] < digito:
                pila.pop()  # ¡Fuera el pequeño!
                vidas_para_borrar -= 1  # Gastamos una vida

            pila.append(digito)

        # 3. Ajuste final
        # Si los números eran decrecientes (ej: 98765...), el while nunca saltó.
        # Nos habrán sobrado vidas y la pila será demasiado larga.
        # Cortamos por el final para quedarnos exactamente con 12.
        pila_final = pila[:longitud_objetivo]

        # 4. Convertir y Sumar
        numero_texto = "".join(pila_final)
        numero_valor = int(numero_texto)

        total_joltage += numero_valor

print("-" * 30)
print("RESULTADO FINAL TOTAL:", total_joltage)
