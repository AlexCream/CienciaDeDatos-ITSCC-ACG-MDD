import numpy as np
from scipy import linalg
import os

def limpiar_pantalla():
    os.system('cls' if os.name == 'nt' else 'clear')

def pedir_entero(mensaje, minimo=None, maximo=None):
    while True:
        val = input(mensaje).strip()
        try:
            n = int(val)
            if minimo is not None and n < minimo:
                print(f"Ingrese un valor mayor o igual a {minimo}")
                input("Presione Enter para continuar...")
                continue
            if maximo is not None and n > maximo:
                print(f"Ingrese un valor menor o igual a {maximo}")
                input("Presione Enter para continuar...")
                continue
            return n
        except ValueError:
            print("Ingrese un valor numerico entero")
            input("Presione Enter para continuar...")

def CrearRenglonManual(cols, renglon_idx):
    RENGLON = []
    i = 0
    while i < cols:
        limpiar_pantalla()
        print(f"Renglon {renglon_idx + 1}: {RENGLON}")
        print(f"Posicion [{i}] (faltan {cols - i}): ", end="")
        val = input().strip()
        try:
            RENGLON.append(int(val))
            i += 1
        except ValueError:
            print("Ingrese un valor entero (puede ser negativo)")
            input("Presione Enter para continuar...")
    return RENGLON

def CrearMatriz(nombre="la Matriz", cuadrada=False, filas_fijas=None, cols_fijas=None):
    limpiar_pantalla()
    print(f"=== Creando {nombre} ===")

    if filas_fijas is not None:
        filas = filas_fijas
        print(f"Filas fijadas: {filas}")
    else:
        filas = pedir_entero("Numero de filas (min 1): ", minimo=1)

    if cols_fijas is not None:
        cols = cols_fijas
        print(f"Columnas fijadas: {cols}")
    elif cuadrada:
        cols = filas
        print(f"Columnas fijadas: {cols} (matriz cuadrada {filas}x{filas})")
    else:
        cols = pedir_entero("Numero de columnas (min 1): ", minimo=1)

    limpiar_pantalla()
    print(f"=== Creando {nombre} ({filas}x{cols}) ===")
    print("[1] Llenado automatico (valores aleatorios 1-9)")
    print("[2] Llenado manual")
    while True:
        modo = input("Seleccione modo: ").strip()
        if modo in ("1", "2"):
            break
        print("Seleccione 1 o 2")

    if modo == "1":
        matriz = np.random.randint(1, 10, size=(filas, cols))
    else:
        datos = []
        for i in range(filas):
            datos.append(CrearRenglonManual(cols, i))
        matriz = np.array(datos, dtype=int)

    limpiar_pantalla()
    print(f"{nombre} ({filas}x{cols}):")
    print(matriz)
    input("\nPresione Enter para continuar...")
    return matriz

def CrearVector(nombre="el Vector", longitud_fija=None):
    limpiar_pantalla()
    print(f"=== Creando {nombre} ===")

    if longitud_fija is not None:
        n = longitud_fija
        print(f"Longitud fijada: {n}")
    else:
        n = pedir_entero("Longitud del vector (min 1): ", minimo=1)

    limpiar_pantalla()
    print(f"=== Creando {nombre} (longitud {n}) ===")
    print("[1] Llenado automatico (valores aleatorios 1-9)")
    print("[2] Llenado manual")
    while True:
        modo = input("Seleccione modo: ").strip()
        if modo in ("1", "2"):
            break
        print("Seleccione 1 o 2")

    if modo == "1":
        vector = np.random.randint(1, 10, size=n)
    else:
        datos = []
        i = 0
        while i < n:
            limpiar_pantalla()
            print(f"Valores actuales: {datos}")
            print(f"Posicion [{i}] (faltan {n - i}): ", end="")
            val = input().strip()
            try:
                datos.append(int(val))
                i += 1
            except ValueError:
                print("Ingrese un valor entero")
                input("Presione Enter para continuar...")
        vector = np.array(datos, dtype=int)

    limpiar_pantalla()
    print(f"{nombre} (longitud {n}):")
    print(vector)
    input("\nPresione Enter para continuar...")
    return vector

def separador():
    print("\n" + "-" * 40 + "\n")

def MenuCalculadorEspecial():
    print("=" * 40)
    print("  CALCULADORA DE ALGEBRA LINEAL")
    print("=" * 40)
    print("[1] Suma de matrices")
    print("[2] Producto escalar")
    print("[3] Transpuesta de una matriz")
    print("[4] Producto punto vectorial")
    print("[5] Multiplicacion de matrices")
    print("[6] Producto matriz-vector")
    print("[7] Particion de matrices")
    print("[8] Inversa de matriz")
    print("[9] Determinante de matriz")
    print("[0] Salir")
    print("=" * 40)
    X = input("Seleccione: ").strip()
    try:
        return int(X)
    except ValueError:
        return -1

def Programa():
    while True:
        limpiar_pantalla()
        option = MenuCalculadorEspecial()

        match option:
            case 0:
                limpiar_pantalla()
                print("Hasta luego.")
                break

            case 1:  # Suma de matrices (mismo tamanio)
                limpiar_pantalla()
                print("=== SUMA DE MATRICES ===")
                print("Ambas matrices deben tener las mismas dimensiones.")
                input("Presione Enter para continuar...")
                A = CrearMatriz("Matriz A")
                filas, cols = A.shape
                print(f"\nMatriz B debe ser {filas}x{cols}")
                input("Presione Enter para continuar...")
                B = CrearMatriz("Matriz B", filas_fijas=filas, cols_fijas=cols)

                limpiar_pantalla()
                print("=== SUMA DE MATRICES ===")
                print("Matriz A:")
                print(A)
                separador()
                print("Matriz B:")
                print(B)
                separador()
                C = np.add(A, B)
                print("A + B =")
                print(C)
                input("\nPresione Enter para continuar...")

            case 2:  # Producto escalar
                limpiar_pantalla()
                print("=== PRODUCTO ESCALAR ===")
                input("Presione Enter para continuar...")
                A = CrearMatriz("la Matriz")
                escalar = pedir_entero("\nIngrese el valor escalar: ")

                limpiar_pantalla()
                print("=== PRODUCTO ESCALAR ===")
                print("Matriz:")
                print(A)
                separador()
                print(f"Escalar: {escalar}")
                separador()
                C = np.multiply(escalar, A)
                print(f"{escalar} * Matriz =")
                print(C)
                input("\nPresione Enter para continuar...")

            case 3:  # Transpuesta
                limpiar_pantalla()
                print("=== TRANSPUESTA DE MATRIZ ===")
                input("Presione Enter para continuar...")
                A = CrearMatriz("la Matriz")

                limpiar_pantalla()
                print("=== TRANSPUESTA DE MATRIZ ===")
                print("Matriz original:")
                print(A)
                separador()
                C = np.transpose(A)
                print("Transpuesta:")
                print(C)
                input("\nPresione Enter para continuar...")

            case 4:  # Producto punto vectorial
                limpiar_pantalla()
                print("=== PRODUCTO PUNTO VECTORIAL ===")
                print("Ambos vectores deben tener la misma longitud.")
                input("Presione Enter para continuar...")
                VA = CrearVector("Vector A")
                n = VA.shape[0]
                print(f"\nVector B debe tener longitud {n}")
                input("Presione Enter para continuar...")
                VB = CrearVector("Vector B", longitud_fija=n)

                limpiar_pantalla()
                print("=== PRODUCTO PUNTO VECTORIAL ===")
                print("Vector A:")
                print(VA)
                separador()
                print("Vector B:")
                print(VB)
                separador()
                resultado = np.dot(VA, VB)
                print("A . B =")
                print(resultado)
                input("\nPresione Enter para continuar...")

            case 5:  # Multiplicacion de matrices (cols A == filas B)
                limpiar_pantalla()
                print("=== MULTIPLICACION DE MATRICES ===")
                print("Las columnas de A deben ser iguales a las filas de B.")
                input("Presione Enter para continuar...")
                A = CrearMatriz("Matriz A")
                _, cols_a = A.shape
                print(f"\nMatriz B debe tener {cols_a} filas")
                input("Presione Enter para continuar...")
                B = CrearMatriz("Matriz B", filas_fijas=cols_a)

                limpiar_pantalla()
                print("=== MULTIPLICACION DE MATRICES ===")
                print("Matriz A:")
                print(A)
                separador()
                print("Matriz B:")
                print(B)
                separador()
                C = np.matmul(A, B)
                print("A x B =")
                print(C)
                input("\nPresione Enter para continuar...")

            case 6:  # Producto matriz-vector (cols A == longitud vector)
                limpiar_pantalla()
                print("=== PRODUCTO MATRIZ-VECTOR ===")
                print("Las columnas de la matriz deben ser iguales a la longitud del vector.")
                input("Presione Enter para continuar...")
                A = CrearMatriz("la Matriz")
                _, cols_a = A.shape
                print(f"\nEl vector debe tener longitud {cols_a}")
                input("Presione Enter para continuar...")
                V = CrearVector("el Vector", longitud_fija=cols_a)

                limpiar_pantalla()
                print("=== PRODUCTO MATRIZ-VECTOR ===")
                print("Matriz:")
                print(A)
                separador()
                print("Vector:")
                print(V)
                separador()
                C = np.dot(A, V)
                print("Matriz x Vector =")
                print(C)
                input("\nPresione Enter para continuar...")

            case 7:  # Particion de matrices (min 2x2)
                limpiar_pantalla()
                print("=== PARTICION DE MATRICES ===")
                print("La matriz debe ser de al menos 2x2.")
                input("Presione Enter para continuar...")
                A = CrearMatriz("la Matriz")
                filas, cols = A.shape

                if filas < 2 or cols < 2:
                    limpiar_pantalla()
                    print(f"La matriz {filas}x{cols} no se puede particionar.")
                    print("Se necesita al menos una matriz 2x2.")
                    input("Presione Enter para continuar...")
                    continue

                limpiar_pantalla()
                print("Matriz original:")
                print(A)
                print(f"\nDimensiones: {filas} filas x {cols} columnas")
                fila_corte = pedir_entero(
                    f"\nFila de corte (1 a {filas - 1}): ", minimo=1, maximo=filas - 1
                )
                col_corte = pedir_entero(
                    f"Columna de corte (1 a {cols - 1}): ", minimo=1, maximo=cols - 1
                )

                A11 = A[:fila_corte, :col_corte]
                A12 = A[:fila_corte, col_corte:]
                A21 = A[fila_corte:, :col_corte]
                A22 = A[fila_corte:, col_corte:]

                limpiar_pantalla()
                print("=== PARTICION DE MATRICES ===")
                print("Matriz original:")
                print(A)
                separador()
                print(f"A11 [filas 0:{fila_corte}, cols 0:{col_corte}]:")
                print(A11)
                print(f"\nA12 [filas 0:{fila_corte}, cols {col_corte}:{cols}]:")
                print(A12)
                print(f"\nA21 [filas {fila_corte}:{filas}, cols 0:{col_corte}]:")
                print(A21)
                print(f"\nA22 [filas {fila_corte}:{filas}, cols {col_corte}:{cols}]:")
                print(A22)
                input("\nPresione Enter para continuar...")

            case 8:  # Inversa (cuadrada)
                limpiar_pantalla()
                print("=== INVERSA DE MATRIZ ===")
                print("La matriz debe ser cuadrada (n x n).")
                input("Presione Enter para continuar...")
                A = CrearMatriz("la Matriz", cuadrada=True)

                limpiar_pantalla()
                print("=== INVERSA DE MATRIZ ===")
                print("Matriz original:")
                print(A)
                separador()
                try:
                    C = linalg.inv(A.astype(float))
                    print("Inversa:")
                    print(C)
                except linalg.LinAlgError:
                    print("Error: la matriz es singular (no tiene inversa).")
                input("\nPresione Enter para continuar...")

            case 9:  # Determinante (cuadrada)
                limpiar_pantalla()
                print("=== DETERMINANTE DE MATRIZ ===")
                print("La matriz debe ser cuadrada (n x n).")
                input("Presione Enter para continuar...")
                A = CrearMatriz("la Matriz", cuadrada=True)

                limpiar_pantalla()
                print("=== DETERMINANTE DE MATRIZ ===")
                print("Matriz:")
                print(A)
                separador()
                det = linalg.det(A.astype(float))
                print(f"det(A) = {det:.4f}")
                input("\nPresione Enter para continuar...")

            case _:
                print("Opcion no valida.")
                input("Presione Enter para continuar...")

if __name__ == "__main__":
    Programa()
