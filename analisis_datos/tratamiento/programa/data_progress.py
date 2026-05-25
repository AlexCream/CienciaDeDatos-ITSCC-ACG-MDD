import pandas as pd
import os
from Limpieza import FuncionDeLimpiezaEspecifica

PATH_SUCIO = "pipol_datos_sucios.csv"
URL_SUCIO  = "https://raw.githubusercontent.com/AlexCream/CienciaDeDatos-ITSCC-ACG-MDD/main/pipol_datos.csv"


def MostrarInformacion(df, titulo=""):
    sep = "─" * 50
    print(f"\n{sep}")
    print(f"  {titulo}")
    print(sep)
    print(f"  Filas: {len(df)}  |  Columnas: {df.shape[1]}")

    print("\n  CAMPOS NULOS POR COLUMNA:")
    for col, n in df.isnull().sum().items():
        print(f"    {col:<12}: {n}")
    print(f"  Filas con algún nulo: {df.isnull().any(axis=1).sum()}")

    print("\n  EDUCACIÓN")
    print(df["education"].value_counts().to_string())
    print("\n  SEXO")
    print(df["sex"].value_counts().to_string())
    print("\n  CIUDADES")
    print(df["city"].value_counts().to_string())

    print("\n  ESTADÍSTICAS NUMÉRICAS")
    print(df[["age", "income", "height", "children"]].describe().round(2).to_string())


def comparar_nulos(df_antes, df_despues):
    print("\n" + "=" * 50)
    print("  COMPARATIVA DE NULOS: ANTES vs DESPUÉS")
    print("=" * 50)
    print(f"  {'Columna':<12} {'Antes':>8} {'Después':>9}")
    print("  " + "─" * 31)
    for col in df_antes.columns:
        antes   = int(df_antes[col].isnull().sum())
        despues = int(df_despues[col].isnull().sum()) if col in df_despues.columns else "-"
        print(f"  {col:<12} {antes:>8} {despues:>9}")


# ── Carga de datos sucios ─────────────────────────────────────
if not os.path.exists(PATH_SUCIO):
    print("Descargando datos de GitHub...")
    df_sucio = pd.read_csv(URL_SUCIO, index_col=[0])
    df_sucio.columns = ["age", "sex", "income", "height", "city", "education", "children"]
    df_sucio.to_csv(PATH_SUCIO)
else:
    df_sucio = pd.read_csv(PATH_SUCIO, index_col=[0])

# ── Limpieza ──────────────────────────────────────────────────
df_limpio = FuncionDeLimpiezaEspecifica(df_sucio, basura=3, exactitud=2)

# ── Reporte de progreso ───────────────────────────────────────
MostrarInformacion(df_sucio,  "ANTES DE LIMPIAR")
MostrarInformacion(df_limpio, "DESPUÉS DE LIMPIAR")
comparar_nulos(df_sucio, df_limpio)

df_limpio.to_csv("pipol_datos_limpio.csv")

print("\n" + "=" * 50)
print("  FIN DEL REPORTE DE PROGRESO")
print("=" * 50)
