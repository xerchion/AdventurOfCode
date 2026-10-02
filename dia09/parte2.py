"""Advent of Code 2025 · Día 9: Movie Theater · Parte 2

Igual, pero el rectángulo debe quedar dentro del polígono que forman los puntos.

Uso: python parte2.py [fichero]
Sin argumento lee entrada.txt, en la misma carpeta que este script.
"""

import sys
from pathlib import Path

ENTRADA = Path(sys.argv[1]) if len(sys.argv) > 1 else Path(__file__).with_name("entrada.txt")

import os

def resolver_day9_vectorial(nombre_archivo):
    if not os.path.exists(nombre_archivo):
        print(f"ERROR: No se encuentra '{nombre_archivo}'.")
        return

    # 1. Leer coordenadas
    puntos = []
    with open(nombre_archivo, 'r') as f:
        for line in f:
            line = line.strip()
            if not line: continue
            try:
                parts = list(map(int, line.split(',')))
                if len(parts) == 2:
                    puntos.append(tuple(parts))
            except ValueError:
                continue

    n = len(puntos)
    if n < 4: # Se necesitan al menos 4 puntos para cerrar un bucle con área
        print("Pocos puntos para formar un polígono.")
        return

    print(f"Puntos leídos: {n}. Procesando geométricamente...")

    # 2. Pre-calcular los segmentos (paredes) del polígono
    # Guardamos tuplas: (tipo, valor_fijo, inicio_variable, fin_variable)
    # Tipo 'V'ertical: (x, y1, y2). Tipo 'H'orizontal: (y, x1, x2)
    segmentos_v = []
    segmentos_h = []

    for i in range(n):
        p1 = puntos[i]
        p2 = puntos[(i + 1) % n] # Conectar con el siguiente (y el último con el primero)

        if p1[0] == p2[0]: # Vertical
            y_min, y_max = min(p1[1], p2[1]), max(p1[1], p2[1])
            segmentos_v.append((p1[0], y_min, y_max))
        else: # Horizontal
            x_min, x_max = min(p1[0], p2[0]), max(p1[0], p2[0])
            segmentos_h.append((p1[1], x_min, x_max))

    max_area = 0

    # 3. Probar parejas de puntos
    # Ordenamos las iteraciones para intentar encontrar áreas grandes pronto (opcional, pero ayuda)
    # Sin embargo, el doble bucle simple es suficiente si N < 2000.

    for i in range(n):
        for j in range(i + 1, n):
            p1 = puntos[i]
            p2 = puntos[j]

            # Calcular dimensiones
            # Recordar: Área = (|x1-x2| + 1) * (|y1-y2| + 1) según el problema
            # PERO primero verifiquemos si vale la pena procesarlo
            w = abs(p1[0] - p2[0]) + 1
            h = abs(p1[1] - p2[1]) + 1
            area = w * h

            if area <= max_area:
                continue

            # Definir los límites del rectángulo candidato (exclusivos para el interior)
            rx_min, rx_max = min(p1[0], p2[0]), max(p1[0], p2[0])
            ry_min, ry_max = min(p1[1], p2[1]), max(p1[1], p2[1])

            # --- CHEQUEO 1: ¿Alguna pared cruza el INTERIOR del rectángulo? ---
            # Si una pared pasa por dentro, el rectángulo "atrapa" espacio vacío -> Inválido.
            # (Las paredes pueden tocar los bordes del rectángulo, eso está permitido)

            pared_intrusiva = False

            # Revisar paredes verticales que estén DENTRO del rango X del rectángulo
            for vx, vy1, vy2 in segmentos_v:
                if rx_min < vx < rx_max: # La pared está en medio horizontalmente
                    # Verificar si se solapa verticalmente
                    if max(ry_min, vy1) < min(ry_max, vy2):
                        pared_intrusiva = True
                        break

            if pared_intrusiva: continue

            # Revisar paredes horizontales que estén DENTRO del rango Y
            for hy, hx1, hx2 in segmentos_h:
                if ry_min < hy < ry_max: # La pared está en medio verticalmente
                    # Verificar si se solapa horizontalmente
                    if max(rx_min, hx1) < min(rx_max, hx2):
                        pared_intrusiva = True
                        break

            if pared_intrusiva: continue

            # --- CHEQUEO 2: ¿El rectángulo está DENTRO o FUERA del polígono? ---
            # Si no hay paredes cruzando, el rectángulo está totalmente dentro o totalmente fuera.
            # Probamos el punto central.
            mid_x = (rx_min + rx_max) / 2
            mid_y = (ry_min + ry_max) / 2

            # Algoritmo Ray Casting (Lanzar rayo a la derecha)
            cruces = 0
            for vx, vy1, vy2 in segmentos_v:
                # El segmento vertical debe estar a la derecha del punto (vx > mid_x)
                # Y el punto debe estar en el rango vertical del segmento (vy1 <= mid_y < vy2)
                if vx > mid_x and vy1 <= mid_y < vy2:
                    cruces += 1

            # Si cruza un número IMPAR de paredes, está DENTRO.
            if cruces % 2 == 1:
                max_area = area

    print("-" * 40)
    print(f"Cálculo finalizado.")
    print(f"El área del rectángulo válido más grande es: {max_area}")
    print("-" * 40)

if __name__ == "__main__":
    resolver_day9_vectorial(ENTRADA)
