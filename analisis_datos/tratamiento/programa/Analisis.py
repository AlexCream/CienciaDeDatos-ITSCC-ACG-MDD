import pandas as pd
import os

# Verificar campos nulos
def ListarCampo(vector, start=0, end=200, salto=10):
    for inicio in range(start, end, salto):
        fin = inicio + salto
        if fin == end:
            count = vector[(vector >= inicio) & (vector <= fin)].shape[0]
        else:
                count = vector[(vector >= inicio) & (vector < fin)].shape[0]
        print(f"Valores entre {inicio}-{fin}: {count}")

def MostrarInformacion(df):
    print("CAMPOS NULOS POR COLUMNA:")
    print(df.isnull().sum())
    print(f"\nTotal de filas con algún valor nulo: {df.isnull().any(axis=1).sum()}")

    print("LISTADO DE EDADES")
    ListarCampo(df["age"], int(df["age"].min()), int(df["age"].max()), 5)
    print("\nLISTADO DE INGRESOS")
    ListarCampo(df["income"], int(df["income"].min()), int(df["income"].max()), 5000)
    print("\nLISTADO DE ALTURAS")
    ListarCampo(df["height"]*100, int(df["height"].min()*100), int(df["height"].max()*100), 5)
    print("\nLISTADO DE HIJOS")
    ListarCampo(df["children"], int(df["children"].min()), int(df["children"].max()), 1)
    print("\nLISTADO DE CIUDADES")
    print(df["city"].value_counts())
    print("\nLISTADO DE EDUCACIÓN")
    print(df["education"].value_counts())
    print("\nLISTADO DE SEXOS")
    print(df["sex"].value_counts())

    print("\n")
    print(df)

path_limpio = "pipol_datos_limpio.csv"
path_sucio = "pipol_datos_sucios.csv"
url_sucio = "https://raw.githubusercontent.com/AlexCream/CienciaDeDatos-ITSCC-ACG-MDD/main/pipol_datos.csv"

# Descargar datos sucios solo si no existen localmente
if not os.path.exists(path_sucio):
    print("Descargando datos sucios de GitHub...")
    df_sucio = pd.read_csv(url_sucio, index_col=[0])
    df_sucio.columns = ["age", "sex", "income", "height", "city", "education", "children"]
    df_sucio.to_csv(path_sucio)
    print(f"Datos sucios guardados en {path_sucio}")
else:
    print("Cargando datos sucios desde archivo local...")
    df_sucio = pd.read_csv(path_sucio, index_col=[0])

df_limpio = pd.read_csv(path_limpio, index_col=[0])

print("INFORMACIÓN DE LOS DATOS SUCIOS")
MostrarInformacion(df_sucio)
print("INFORMACIÓN DE LOS DATOS LIMPIOS")
MostrarInformacion(df_limpio)