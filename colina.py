import numpy as np
import matplotlib.pyplot as plt


# Función para implementar el algoritmo de Hill Climbing
def escalada_colina_multiple(func, tam_paso, max_iter, num_inicios, rango, direccion='max'):
    mejores_puntos = []
    for _ in range(num_inicios):
        x = np.random.uniform(rango[0], rango[1])
        for _ in range(max_iter):
            x_nuevo = x + tam_paso if direccion == 'max' else x - tam_paso
            if func(x_nuevo) > func(x) and direccion == 'max':
                x = x_nuevo
            elif func(x_nuevo) < func(x) and direccion == 'min':
                x = x_nuevo
            else:
                break
        mejores_puntos.append(x)
    return mejores_puntos


# Función para obtener los máximos y mínimos globales
def obtener_extremos(func, puntos, num_extremos=3, tipo='max'):
    if tipo == 'max':
        puntos = sorted(puntos, key=lambda x: func(x), reverse=True)
    elif tipo == 'min':
        puntos = sorted(puntos, key=lambda x: func(x))

    # Eliminar duplicados cercanos
    puntos_unicos = []
    for punto in puntos:
        if all(abs(punto - p) > 0.1 for p in puntos_unicos):  # Ajustar la tolerancia según sea necesario
            puntos_unicos.append(punto)
        if len(puntos_unicos) == num_extremos:
            break

    return puntos_unicos


# Función para graficar la función con los puntos máximos y mínimos
def graficar_funcion_con_puntos(func, rango_x, puntos_max, puntos_min):
    x = np.linspace(rango_x[0], rango_x[1], 1000)
    y = func(x)

    plt.plot(x, y, label='F(x)')
    for punto in puntos_max:
        plt.scatter(punto, func(punto), color='red', label='Máximo' if punto == puntos_max[0] else "")
        plt.text(punto, func(punto), f'({punto:.2f}, {func(punto):.2f})', color='red')
    for punto in puntos_min:
        plt.scatter(punto, func(punto), color='blue', label='Mínimo' if punto == puntos_min[0] else "")
        plt.text(punto, func(punto), f'({punto:.2f}, {func(punto):.2f})', color='blue')
    plt.legend()
    plt.xlabel('x')
    plt.ylabel('F(x)')
    plt.title('Escalada de Colina en F(x)')
    plt.grid(True)
    plt.show()


# Definir la función
def funcion(x):
    return np.cos(2 * x + 1) + 2 * np.cos(3 * x + 2) + 3 * np.cos(4 * x + 3) + 4 * np.cos(5 * x + 4) + 5 * np.cos(
        6 * x + 5)


# Parámetros del algoritmo
tam_paso = 0.01
max_iter = 1000
num_inicios = 500  # Aumentar el número de inicios aleatorios
rango = (-10, 10)

# Encontrar máximos y mínimos
puntos_max = escalada_colina_multiple(funcion, tam_paso, max_iter, num_inicios, rango, direccion='max')
puntos_min = escalada_colina_multiple(funcion, tam_paso, max_iter, num_inicios, rango, direccion='min')

# Filtrar los puntos únicos para evitar duplicados
puntos_max = list(set(puntos_max))
puntos_min = list(set(puntos_min))

# Obtener los tres máximos y mínimos globales
puntos_max_globales = obtener_extremos(funcion, puntos_max, num_extremos=3, tipo='max')
puntos_min_globales = obtener_extremos(funcion, puntos_min, num_extremos=3, tipo='min')

# Graficar la función con los puntos máximos y mínimos
graficar_funcion_con_puntos(funcion, rango, puntos_max_globales, puntos_min_globales)
