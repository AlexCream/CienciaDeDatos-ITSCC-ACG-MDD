# Reporte Técnico — Práctica ETL 1

## Descripción general

El código implementa un mini pipeline **ETL (Extract, Transform, Load)** sobre un archivo CSV de miembros. Se carga la información a una base de datos SQLite, se consultan los datos y se aplican tres transformaciones de limpieza sobre la columna de números telefónicos usando expresiones regulares.

---

## Conceptos clave

| Concepto | Descripción |
|---|---|
| **ETL** | Proceso de Extracción, Transformación y Carga de datos. |
| **SQLite** | Motor de base de datos relacional embebido, sin servidor. |
| **Pandas DataFrame** | Estructura tabular en memoria para manipular datos con Python. |
| **Expresiones regulares (RegEx)** | Patrones que describen cadenas de texto para buscar, filtrar o reemplazar. |

---

## Funciones y técnicas aplicadas

### 1. `load_csv_to_sqlite` — Carga (Load)
- Lee el CSV con `pd.read_csv`.
- Crea/reemplaza la tabla `members` en una base SQLite con `df.to_sql`.
- Devuelve la conexión activa para consultas posteriores.

### 2. `numeros_indonesia` — Filtro por patrón RegEx
- **Patrón:** `^\+62` — verifica que el número comience con el prefijo telefónico de Indonesia.
- Usa `str.match` para evaluar cada valor; los que **no** coinciden se convierten en `NULL` (None).
- Luego se eliminan las filas nulas con `dropna`, conservando solo números indonesios válidos.

### 3. `limpiar_corchetes` — Eliminación de códigos de área
- **Patrón:** `\(\d+\)[-]?` — detecta bloques del tipo `(036)-` o `(021)`.
- Usa `str.replace` para eliminarlos, dejando únicamente los dígitos del número local.

### 4. `limpiar_espacios` — Normalización de formato
- **Patrón:** `[\s-]+` — detecta uno o más espacios en blanco o guiones consecutivos.
- Los elimina por completo, produciendo números compactos sin separadores.

---

## Flujo del pipeline

```
members.csv
    │
    ▼
load_csv_to_sqlite()      ← Extracción + Carga en SQLite
    │
    ▼
SELECT * FROM members     ← Consulta inicial (datos crudos)
    │
    ▼
numeros_indonesia()       ← Filtro: solo +62, resto → NULL → eliminados
    │
    ▼
limpiar_corchetes()       ← Elimina códigos de área (036)- etc.
    │
    ▼
limpiar_espacios()        ← Elimina espacios y guiones internos
    │
    ▼
Consulta final (datos limpios)
```

---

## Diferencia entre la consulta inicial y la consulta final

| Aspecto | Consulta inicial | Consulta final |
|---|---|---|
| **Filas** | Todos los registros del CSV | Solo registros con número indonesio (`+62`) |
| **Formato del número** | Heterogéneo: `+62 (036)-123 456`, `+1-800-555-0199`, etc. | Compacto y uniforme: `+6236123456` |
| **Valores nulos** | Pueden existir o no | Eliminados (`dropna`) |
| **Calidad** | Datos crudos sin limpiar | Datos normalizados y filtrados |

**Ejemplo ilustrativo:**

| Estado | phone_number |
|---|---|
| Antes | `+62 (036)-812 345 678` |
| Después | `+62036812345678` |

---

## Herramienta de IA utilizada

Se utilizó **Claude (Anthropic)** como apoyo para revisar la lógica de las expresiones regulares, validar el flujo ETL y estructurar este reporte técnico.
