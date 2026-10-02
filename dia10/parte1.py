"""Advent of Code 2025 · Día 10: Factory · Parte 1

Mínimo de pulsaciones para encender el patrón de luces: prueba todas las combinaciones de botones.

Uso: python parte1.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os
import re
from itertools import product


def parse_machine(line):
    # 1. Extraer el patrón de luces: [.##.]
    match_lights = re.search(r"\[(.*?)\]", line)
    if not match_lights:
        return None

    pattern_str = match_lights.group(1)
    target_lights = [1 if c == "#" else 0 for c in pattern_str]

    # 2. Extraer los botones: (0,2) (1,3) ...
    # Usamos regex para encontrar todo lo que esté entre paréntesis
    buttons_str = re.findall(r"\((.*?)\)", line)

    buttons = []
    for b_str in buttons_str:
        if not b_str.strip():  # Botón vacío ()
            buttons.append([])
            continue
        # Convertir "0,2" -> [0, 2]
        indices = [int(x) for x in b_str.split(",")]
        buttons.append(indices)

    return target_lights, buttons


def solve_machine(target_lights, buttons):
    num_buttons = len(buttons)
    num_lights = len(target_lights)
    min_presses = float("inf")
    found_solution = False

    # Probar todas las combinaciones posibles de botones (2^N)
    # product([0, 1], repeat=N) genera (0,0,0), (0,0,1), etc.
    for press_combination in product([0, 1], repeat=num_buttons):

        # Optimización: Si el número de pulsaciones actual ya es mayor
        # o igual que el mínimo encontrado, no hace falta simular.
        current_presses = sum(press_combination)
        if current_presses >= min_presses:
            continue

        # Simular el estado de las luces
        # Empezamos con todas apagadas [0, 0, 0...]
        current_state = [0] * num_lights

        for i, press in enumerate(press_combination):
            if press == 1:  # Si apretamos este botón
                affected_indices = buttons[i]
                for idx in affected_indices:
                    # Toggle: XOR con 1 (o cambiar 0->1, 1->0)
                    if idx < num_lights:  # Seguridad por si el índice se sale
                        current_state[idx] ^= 1

        # Verificar si llegamos al objetivo
        if current_state == target_lights:
            if current_presses < min_presses:
                min_presses = current_presses
                found_solution = True

    return (
        min_presses if found_solution else 0
    )  # Si no hay solución (raro), devolvemos 0


def resolver_day10(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    total_presses = 0
    machines_processed = 0

    with open(nombre_archivo, "r") as f:
        for line in f:
            line = line.strip()
            if not line:
                continue

            data = parse_machine(line)
            if data:
                target, btns = data
                # Resolver esta máquina individualmente
                presses = solve_machine(target, btns)
                total_presses += presses
                machines_processed += 1

                # Feedback visual opcional
                # print(f"Máquina {machines_processed}: {presses} pulsaciones")

    print("-" * 40)
    print(f"Procesadas {machines_processed} máquinas.")
    print(f"Total mínimo de pulsaciones: {total_presses}")
    print("-" * 40)


if __name__ == "__main__":
    resolver_day10(ENTRADA)
