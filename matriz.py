import random
import math

def crear_solucion_inicial(n):
    # Crear una lista de números del 1 al n^2
    numeros = list(range(1, n * n + 1))
    # Formar la matriz
    random.shuffle(numeros)
    matriz = [numeros[i * n:(i + 1) * n] for i in range(n)]
    return matriz

def calcular_constante_magica(n):
    # Calcula la constante mágica
    return n * (n ** 2 + 1) // 2

def calcular_costo(matriz, constante_magica):
    n = len(matriz)
    costo = 0

    # Calcular la diferencia con respecto a la suma mágica
    for i in range(n):
        costo += abs(constante_magica - sum(matriz[i]))  # Filas
        costo += abs(constante_magica - sum(matriz[j][i] for j in range(n)))  # Columnas

    # Calcular la diferencia con respecto a las diagonales
    costo += abs(constante_magica - sum(matriz[i][i] for i in range(n)))  # Diagonal principal
    costo += abs(constante_magica - sum(matriz[i][n - i - 1] for i in range(n)))  # Diagonal secundaria

    return costo

def generar_vecino(matriz):
    n = len(matriz)
    nueva_matriz = [fila[:] for fila in matriz]  # Copia de la matriz actual

    # Seleccionar dos posiciones aleatorias para intercambiar
    i, j = random.randint(0, n - 1), random.randint(0, n - 1)
    x, y = random.randint(0, n - 1), random.randint(0, n - 1)

    # Intercambiar los elementos en las posiciones seleccionadas
    nueva_matriz[i][j], nueva_matriz[x][y] = nueva_matriz[x][y], nueva_matriz[i][j]

    return nueva_matriz

def enfriamiento_simulado(n, max_iteraciones=10000, temp_inicial=100, tasa_enfriamiento=0.995):
    solucion_actual = crear_solucion_inicial(n)
    costo_actual = calcular_costo(solucion_actual, calcular_constante_magica(n))
    temperatura = temp_inicial

    mejor_solucion = solucion_actual
    mejor_costo = costo_actual

    iteracion = 0
    while iteracion < max_iteraciones and costo_actual != 0:
        # Generar una solución vecina
        nueva_solucion = generar_vecino(solucion_actual)
        nuevo_costo = calcular_costo(nueva_solucion, calcular_constante_magica(n))

        # Calcular la probabilidad de aceptar la nueva solución
        if nuevo_costo < costo_actual or random.random() < math.exp((costo_actual - nuevo_costo) / temperatura):
            solucion_actual = nueva_solucion
            costo_actual = nuevo_costo

            if nuevo_costo < mejor_costo:
                mejor_solucion = nueva_solucion
                mejor_costo = nuevo_costo

        # Enfriar la temperatura
        temperatura *= tasa_enfriamiento
        iteracion += 1

    return mejor_solucion, mejor_costo

def imprimir_matriz(matriz):
    n = len(matriz)
    constante_magica = calcular_constante_magica(n)
    print("Matriz:")
    for fila in matriz:
        print(" ".join(f"{num:2d}" for num in fila))

    # Imprimir las sumas de las filas
    print("\nSuma de las filas:")
    for fila in matriz:
        print(sum(fila), end=' ')
    print()

    # Imprimir las sumas de las columnas
    print("\nSuma de las columnas:")
    for j in range(n):
        print(sum(matriz[i][j] for i in range(n)), end=' ')
    print()

    # Imprimir las sumas de las diagonales
    print("\nSuma de la diagonal principal:")
    print(sum(matriz[i][i] for i in range(n)))

    print("\nSuma de la diagonal secundaria:")
    print(sum(matriz[i][n - i - 1] for i in range(n)))

# Pedir al usuario el tamaño de la matriz
while True:
    try:
        n = int(input("Introduce el tamaño de la matriz (2-10): "))
        if 2 <= n <= 10:
            break
        else:
            print("Por favor, introduce un número entre 2 y 10.")
    except ValueError:
        print("Entrada inválida. Por favor, introduce un número entre 2 y 10.")

# Ejecutar el algoritmo
solucion, costo = enfriamiento_simulado(n)

print("Cuadrado mágico encontrado:" if costo == 0 else "No se encontró la matriz:")
imprimir_matriz(solucion)

