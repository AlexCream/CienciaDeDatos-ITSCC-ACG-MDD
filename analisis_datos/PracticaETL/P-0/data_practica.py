import sqlite3
import pandas as pd
import re
from datetime import datetime

# EXTRACCIÓN (Extract)
# Cargamos el CSV y lo insertamos en SQLite3
def load_csv_to_sqlite(csv_path: str, db_path: str = "members.db") -> sqlite3.Connection:
    df = pd.read_csv(csv_path)
    conn = sqlite3.connect(db_path)
    df.to_sql("members", conn, if_exists="replace", index=False)
    print(f"{len(df)} registros cargados en '{db_path}' tabla 'members'")
    return conn

# TRANSFORMACIÓN (Transform)
# Funciones ETL con Expresiones Regulares
# Extraer Código Postal
def extract_postal_code(df: pd.DataFrame, source_col: str = "address", dest_col: str  = "postal_code") -> pd.DataFrame:
    PATTERN = r"\b(\d{4,6})\b"
    df[dest_col] = df[source_col].str.extract(PATTERN)
    print(f"Columna '{dest_col}' creada desde '{source_col}'")
    return df

# Formatear Número Telefónico ────────────────────────
def clean_phone_number(df: pd.DataFrame, col: str = "phone_number") -> pd.DataFrame:
    # 1. Negativos corruptos → NULL
    df[col] = df[col].where(~df[col].str.match(r"^-\d+$", na=False), other=None)
 
    # 2. Quitar +, (, )
    df[col] = df[col].str.replace(r"[+()]", "", regex=True).str.strip()
 
    # 3. Guión interno como separador → espacio  (ej. 329-4756 → 329 4756)
    df[col] = df[col].str.replace(r"(?<=\d)-(?=\d)", " ", regex=True)
 
    # 4. Prefijo duplicado: '62 62 ' → '62 '  (ej. +62 (62) → 62 62 → 62)
    df[col] = df[col].str.replace(r"^62\s+62\s+", "62 ", regex=True)
 
    # 5. Cero redundante tras prefijo de país: '62 0xxx' → '62 xxx'
    df[col] = df[col].str.replace(r"^62\s+0", "62 ", regex=True)
 
    # 6. Espacios múltiples → uno solo
    df[col] = df[col].str.replace(r"\s{2,}", " ", regex=True).str.strip()
    print(f"Columna '{col}' formateada (sin +, (, ))")
    return df

# Formatear Fecha de Nacimiento → DD/MM/AAAA ─────────
def format_birth_date(df: pd.DataFrame, col: str = "birth_date") -> pd.DataFrame:
    MONTH_MAP = {
        "jan":"01","feb":"02","mar":"03","apr":"04",
        "may":"05","jun":"06","jul":"07","aug":"08",
        "sep":"09","oct":"10","nov":"11","dec":"12",
    }

    PATTERN = r"(\d{1,2})[-\s]([a-zA-Z]+)[-\s](\d{2,4})"

    def _convert(raw: str) -> str:
        m = re.match(PATTERN, str(raw).strip())
        if not m:
            return raw
        day, mon_str, year = m.group(1), m.group(2).lower(), m.group(3)
        month = MONTH_MAP.get(mon_str, "??")
        # Expandir año de 2 dígitos → 4 dígitos
        if len(year) == 2:
            year = "19" + year if int(year) > 25 else "20" + year
        return f"{int(day):02d}/{month}/{year}"

    df[col] = df[col].apply(_convert)
    print(f"Columna '{col}' formateada a DD/MM/AAAA")
    return df

# Calcular Edad desde register_time (Unix timestamp)
def calculate_age(df: pd.DataFrame, col: str = "register_time") -> pd.DataFrame:
    def _ts_to_age(ts) -> int:
        try:
            reg_date = datetime.fromtimestamp(int(ts))
            today    = datetime.today()
            years    = (today - reg_date).days
            return years
        except Exception:
            return None

    df["age_years"] = df[col].apply(_ts_to_age)
    print(f"Columna 'age_years' calculada desde '{col}'")
    return df


# CARGA (Load)
# Guardamos el DataFrame transformado de vuelta en SQLite3
def load_transformed_to_sqlite(df: pd.DataFrame, conn: sqlite3.Connection, table: str = "members_clean") -> None:
    df.to_sql(table, conn, if_exists="replace", index=False)
    print(f"Datos transformados guardados en tabla '{table}'")

# PIPELINE PRINCIPAL
def run_etl(csv_path: str = "members.csv", db_path:  str = "members.db") -> pd.DataFrame:
    input("\nPresiona Enter para iniciar la extraccion...")
    conn = load_csv_to_sqlite(csv_path, db_path)
    df   = pd.read_sql("SELECT * FROM members", conn)
    
    input("\nPresiona Enter para mostrar el csv original...")
    print(df[["first_name","address","phone_number","birth_date","register_time"]].to_string(index=False))
    
    input("\nPresiona Enter para continuar con las transformaciones...")
    print("\n─── Transformaciones ───")
    df = extract_postal_code(df, source_col="address",  dest_col="postal_code")
    df = clean_phone_number (df, col="phone_number")
    df = format_birth_date  (df, col="birth_date")
    df = calculate_age      (df, col="register_time")
    
    input("\n Transformacion terminada, presiona Enter para continuar con la carga...")
    print("\n Carga en SQLite3")
    load_transformed_to_sqlite(df, conn, table="members_clean")
    
    input("\n Carga terminada, presiona Enter para mostrar el resultado...")
    print(df[["first_name","postal_code","phone_number","birth_date","age_years"]].to_string(index=False))
    input("\n Enter para continuar...")

    conn.close()
    return df

# CONSULTAS DE EJEMPLO SOBRE SQLITE3
def query_examples(db_path: str = "members.db") -> None:
    conn = sqlite3.connect(db_path)
    print("\nConsulta: todos los campos limpios")
    df = pd.read_sql("""
        SELECT *
        FROM   members_clean
        ORDER  BY last_name
    """, conn)
    print(df.to_string(index=False))
    conn.close()

# ENTRADA
if __name__ == "__main__":
    df_result = run_etl(csv_path="members.csv", db_path="members.db")
    query_examples(db_path="members.db")
