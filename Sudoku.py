import random
import math

# Función para calcular el número de conflictos en el Sudoku
def contar_conflictos(sudoku):
    conflictos = 0
    n = len(sudoku)

    # Contar conflictos en filas
    for fila in sudoku:
        conflictos += n - len(set(fila))

    # Contar conflictos en columnas
    for columna in range(n):
        col = [sudoku[fila][columna] for fila in range(n)]
        conflictos += n - len(set(col))

    # Contar conflictos en subcuadrículas de 3x3
    for fila_base in range(0, n, 3):
        for columna_base in range(0, n, 3):
            bloque = []
            for fila in range(3):
                for columna in range(3):
                    bloque.append(sudoku[fila_base + fila][columna_base + columna])
            conflictos += n - len(set(bloque))

    return conflictos

# Función para generar una solución vecina del Sudoku
def vecino(sudoku, fijo):
    n = len(sudoku)
    nuevo_sudoku = [fila[:] for fila in sudoku]

    # Selecciona aleatoriamente un bloque 3x3
    fila_bloque = random.randint(0, 2) * 3
    columna_bloque = random.randint(0, 2) * 3

    # Encuentra dos celdas intercambiables dentro del bloque que no sean fijas
    celda1 = None
    celda2 = None

    while celda1 is None or celda2 is None:
        fila1 = fila_bloque + random.randint(0, 2)
        columna1 = columna_bloque + random.randint(0, 2)
        fila2 = fila_bloque + random.randint(0, 2)
        columna2 = columna_bloque + random.randint(0, 2)

        if not fijo[fila1][columna1]:
            celda1 = (fila1, columna1)
        if not fijo[fila2][columna2] and (fila1, columna1) != (fila2, columna2):
            celda2 = (fila2, columna2)

    # Intercambia las celdas
    nuevo_sudoku[celda1[0]][celda1[1]], nuevo_sudoku[celda2[0]][celda2[1]] = \
        nuevo_sudoku[celda2[0]][celda2[1]], nuevo_sudoku[celda1[0]][celda1[1]]

    return nuevo_sudoku

# Algoritmo de enfriamiento simulado para resolver Sudoku
def enfriamiento_simulado_sudoku(sudoku):
    n = len(sudoku)
    temperatura_inicial = 5000
    temperatura_final = 0.1
    tasa_enfriamiento = 0.999

    # Crear matriz de celdas fijas
    fijo = [[sudoku[fila][columna] != 0 for columna in range(n)] for fila in range(n)]

    # Inicializar el Sudoku llenando filas de forma aleatoria sin cambiar las celdas fijas
    solucion_actual = []
    for fila in range(n):
        numeros = set(range(1, n + 1))
        fila_solucion = []
        for columna in range(n):
            if fijo[fila][columna]:
                fila_solucion.append(sudoku[fila][columna])
                if sudoku[fila][columna] in numeros:
                    numeros.remove(sudoku[fila][columna])
            else:
                fila_solucion.append(0)

        # Rellenar las celdas no fijas con los números restantes de forma aleatoria
        posiciones_libres = [i for i in range(n) if not fijo[fila][i]]
        random.shuffle(posiciones_libres)
        for i, num in zip(posiciones_libres, numeros):
            fila_solucion[i] = num

        solucion_actual.append(fila_solucion)

    costo_actual = contar_conflictos(solucion_actual)
    temperatura = temperatura_inicial
    # Guardar el número de conflictos en cada paso
    historial_conflictos = [costo_actual]

    while temperatura > temperatura_final and costo_actual > 0:
        solucion_candidata = vecino(solucion_actual, fijo)
        costo_candidato = contar_conflictos(solucion_candidata)
        delta_E = costo_candidato - costo_actual

        if delta_E < 0 or random.random() < math.exp(-delta_E / temperatura):
            solucion_actual = solucion_candidata
            costo_actual = costo_candidato

        temperatura *= tasa_enfriamiento
        historial_conflictos.append(costo_actual)

    return solucion_actual, costo_actual, historial_conflictos

# Función para inicializar el Sudoku con 16 valores aleatorios
def inicializar_sudoku_aleatorio():
    n = 9
    sudoku = [[0] * n for _ in range(n)]
    posiciones = [(fila, columna) for fila in range(n) for columna in range(n)]
    random.shuffle(posiciones)

    # Insertar 16 valores aleatorios en posiciones aleatorias
    for _ in range(16):
        fila, columna = posiciones.pop()
        valor = random.randint(1, n)
        sudoku[fila][columna] = valor

    return sudoku

# Inicializar un Sudoku aleatorio con 16 valores
sudoku_inicial = inicializar_sudoku_aleatorio()

# Resolver el Sudoku
solucion, costo, historial_conflictos = enfriamiento_simulado_sudoku(sudoku_inicial)

# Imprimir la solución encontrada
print("Sudoku Inicial:")
for fila in sudoku_inicial:
    print(fila)

print("\nSudoku Resuelto:")
for fila in solucion:
    print(fila)

print("\nNúmero de conflictos:", costo)
print("\nHistorial de conflictos:", historial_conflictos)
