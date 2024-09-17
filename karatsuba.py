import random

def generar_numero_grande(num_digitos):
    # Generar un número de num_digitos dígitos, con cada dígito en el rango de 0-9
    return int(''.join(str(random.randint(0, 9)) for _ in range(num_digitos)))

def karatsuba(x, y):
    # Caso base: si los números son suficientemente pequeños, multiplicar directamente
    if x < 10 or y < 10:
        return x * y

    # Calcular el tamaño de los números
    n = max(len(str(x)), len(str(y)))
    m = n // 2

    # Dividir los números en partes altas y bajas
    parte_alta_x, parte_baja_x = divmod(x, 10**m)
    parte_alta_y, parte_baja_y = divmod(y, 10**m)

    # Calcular recursivamente los tres productos
    z0 = karatsuba(parte_baja_x, parte_baja_y)
    z2 = karatsuba(parte_alta_x, parte_alta_y)
    z1 = karatsuba((parte_baja_x + parte_alta_x), (parte_baja_y + parte_alta_y)) - z0 - z2

    # Combinar los resultados para obtener el producto final
    return z2 * 10**(2*m) + z1 * 10**m + z0

# Generar dos números de 1024 dígitos aleatorios
A = generar_numero_grande(1024)
B = generar_numero_grande(1024)

# Realizar la multiplicación usando Karatsuba
resultado = karatsuba(A, B)

# Mostrar el resultado
print(f"El resultado de multiplicar A y B usando Karatsuba es:\n{resultado}")
