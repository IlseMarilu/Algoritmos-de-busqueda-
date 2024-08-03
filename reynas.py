import random
import math


# Función para contar los conflictos en un tablero de ajedrez
def contar_conflictos(tablero):
    conflictos = 0
    n = len(tablero)
    for i in range(n):
        for j in range(i + 1, n):
            if tablero[i] == tablero[j] or abs(tablero[i] - tablero[j]) == abs(i - j):
                conflictos += 1
    return conflictos


# Función para generar una solución vecina
def vecino(tablero):
    n = len(tablero)
    nuevo_tablero = tablero[:]
    i = random.randint(0, n - 1)
    nuevo_tablero[i] = random.randint(0, n - 1)
    return nuevo_tablero


# Algoritmo de enfriamiento simulado
def enfriamiento_simulado(n, temperatura_inicial, tasa_enfriamiento, temperatura_final):
    solucion_actual = [random.randint(0, n - 1) for _ in range(n)]
    costo_actual = contar_conflictos(solucion_actual)
    temperatura = temperatura_inicial

    while temperatura > temperatura_final:
        solucion_candidata = vecino(solucion_actual)
        costo_candidata = contar_conflictos(solucion_candidata)
        delta_E = costo_candidata - costo_actual

        if delta_E < 0 or random.random() < math.exp(-delta_E / temperatura):
            solucion_actual = solucion_candidata
            costo_actual = costo_candidata

        temperatura *= tasa_enfriamiento

    return solucion_actual, costo_actual


# Parámetros del algoritmo
n = 8
temperatura_inicial = 1000
tasa_enfriamiento = 0.99
temperatura_final = 0.1

# Ejecución del algoritmo
solucion, costo = enfriamiento_simulado(n, temperatura_inicial, tasa_enfriamiento, temperatura_final)

print("Tablero final:")
for fila in range(n):
    linea = ['.'] * n
    linea[solucion[fila]] = 'Q'
    print(' '.join(linea))

print("\nNúmero de conflictos:", costo)
