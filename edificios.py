import numpy as np
import random
import math

# Parámetros del problema
NUM_EDIFICIOS = 10  # Número de edificios
NUM_GRUPOS_PERSONAS = 10  # Número de grupos de personas

# Matriz de distancias aleatorias (distancia entre grupos y ubicaciones fijas de sitios)
distancias = np.random.randint(1, 101, size=(NUM_GRUPOS_PERSONAS, NUM_EDIFICIOS))

# Vector que representa la cantidad de personas en cada grupo
frecuencia_personas = np.random.randint(1, 101, size=NUM_GRUPOS_PERSONAS)


# Función objetivo: minimiza la distancia total recorrida
def calcular_distancia_total(asignacion):
    total_distancia = 0
    for i in range(NUM_GRUPOS_PERSONAS):
        edificio_asignado = asignacion[i]
        total_distancia += distancias[i, edificio_asignado] * frecuencia_personas[i]
    return total_distancia


# Generar una solución inicial (asignación aleatoria de edificios a ubicaciones)
def generar_solucion_inicial():
    return random.sample(range(NUM_EDIFICIOS), NUM_EDIFICIOS)


# Función para generar una solución vecina (intercambio de dos edificios)
def generar_vecino(solucion_actual):
    vecino = solucion_actual[:]
    edificio1, edificio2 = random.sample(range(NUM_EDIFICIOS), 2)
    vecino[edificio1], vecino[edificio2] = vecino[edificio2], vecino[edificio1]
    return vecino


# Recocido simulado con temperatura dinámica
def recocido_simulado_dinamico(iteraciones, enfriamiento_lento=0.999, enfriamiento_rapido=0.95):
    # Inicializar una solución inicial
    solucion_actual = generar_solucion_inicial()
    mejor_solucion = solucion_actual[:]
    mejor_distancia = calcular_distancia_total(mejor_solucion)

    temperatura = 1000  # Temperatura inicial alta para permitir exploración
    estancamiento = 0  # Contador para medir cuántas iteraciones sin mejora

    for i in range(iteraciones):
        # Generar una solución vecina
        solucion_vecina = generar_vecino(solucion_actual)
        distancia_actual = calcular_distancia_total(solucion_actual)
        distancia_vecina = calcular_distancia_total(solucion_vecina)

        # Aceptar la solución vecina si es mejor o con probabilidad si es peor
        if distancia_vecina < distancia_actual:
            solucion_actual = solucion_vecina
            estancamiento = 0  # Resetea el contador si mejora
        else:
            probabilidad_aceptacion = math.exp((distancia_actual - distancia_vecina) / temperatura)
            if random.random() < probabilidad_aceptacion:
                solucion_actual = solucion_vecina
            estancamiento += 1  # Incrementa el contador si no mejora

        # Actualizar la mejor solución encontrada
        if calcular_distancia_total(solucion_actual) < mejor_distancia:
            mejor_solucion = solucion_actual[:]
            mejor_distancia = calcular_distancia_total(mejor_solucion)
            estancamiento = 0  # Resetea si encuentra una mejor solución

        # Ajuste dinámico de la temperatura
        if estancamiento > 100:  # Si no mejora después de 100 iteraciones, enfría lentamente
            temperatura *= enfriamiento_lento
        else:  # Si está mejorando, enfría rápidamente
            temperatura *= enfriamiento_rapido

        # Imprimir el progreso cada 100 iteraciones
        if i % 100 == 0:
            print(
                f"Iteración {i}: Mejor distancia = {mejor_distancia}, Temperatura = {temperatura:.5f}, Estancamiento = {estancamiento}")

    return mejor_solucion, mejor_distancia


# Parámetros del recocido simulado
iteraciones = 10000  # Número de iteraciones

# Ejecutar el recocido simulado dinámico
mejor_asignacion, mejor_distancia = recocido_simulado_dinamico(iteraciones)
print("\nMejor asignación de edificios a ubicaciones fijas:")
print(mejor_asignacion)
print("Distancia total mínima:", mejor_distancia)
