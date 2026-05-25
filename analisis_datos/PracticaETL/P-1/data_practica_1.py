# Actividad Individual:
# Una vez creado el ambiente virtual utilizamos Sqlite3, 
# y utilizamos el archivo “members.csv” para trabajar. 
import sqlite3
import pandas as pd

def load_csv_to_sqlite(csv_path: str, db_path: str = "members.db") -> sqlite3.Connection:
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("members", conn, if_exists="replace", index=False)
    print(f"{len(df)} registros cargados en '{db_path}' tabla 'members'")
    return conn

# 1)  Crear patrón RegEx para la columna Phone Number que encuentre todos los “+62”. 
def numeros_indonesia(df: pd.DataFrame, col: str = "phone_number") -> pd.DataFrame:
    # 1. Negativos corruptos → NULL
    df[col] = df[col].where(df[col].str.match(r"^\+62", na=False), other=None)
    print(f"Columna '{col}' formateada (sin +62)")
    return df

# 2)  Crear patrón RegEx que encuentre todos los patrones que comiencen con corchetes (abierto y cerrado) y un guion.
def limpiar_corchetes(df: pd.DataFrame, col: str = "phone_number") -> pd.DataFrame:
    # Elimina el bloque de área entre paréntesis y el guion/espacio que lo sigue: (036)- o (036)
    patron = r"\(\d+\)[-]?"
    df[col] = df[col].str.replace(patron, "", regex=True)
    print(f"Columna '{col}' limpiada (corchetes y guion eliminados)")
    return df

# 3)  Crear patrón RegEx que encuentre todos los espacios vacios.
def limpiar_espacios(df: pd.DataFrame, col: str = "phone_number") -> pd.DataFrame:
    # Elimina todos los espacios en blanco dentro del número
    patron = r"[\s-]+"
    df[col] = df[col].str.replace(patron, "", regex=True)
    print(f"Columna '{col}' limpiada (espacios eliminados)")
    return df

csv_path = "members.csv"
db_path = "members.db"
conn = load_csv_to_sqlite(csv_path, db_path)
df   = pd.read_sql("SELECT * FROM members", conn)

print(df[["participant_id", "first_name", "last_name", "phone_number"]])
# Aplicar transformaciones en cadena
dfa = numeros_indonesia(df, "phone_number")
dfa = dfa.dropna(subset=["phone_number"])
dfb = limpiar_corchetes(dfa, "phone_number")
dfc = limpiar_espacios(dfb, "phone_number")

print(dfc[["participant_id", "first_name", "last_name", "phone_number"]])
