import pandas as pd
import psycopg2
from psycopg2.extras import execute_batch
from psycopg2 import errors

# 1. Leer el Excel
archivo_excel = r"C:\Desarrollos\API_TasasCambio_USA\backend\data\tasas_de_cambio.xlsm"
df = pd.read_excel(archivo_excel, sheet_name="Hoja3", header=2)

# 2. Conexión a PostgreSQL (Render)
conn = psycopg2.connect(
    host="dpg-d4s5b77diees73dkljd0-a.ohio-postgres.render.com",
    database="db_api_usuarios",
    user="usuario_api",
    password="qLOEsZzJHzqjNBEQDuwEjGXL2dGU4Aq5",
    port=5432
)

cursor = conn.cursor()

# ==============================
# NORMALIZAR FECHA
# ==============================

df["Fecha"] = pd.to_datetime(
    df["Fecha"],
    format="%Y-%m-%d",
    errors="coerce"
)

# Convertir NaT a None (para PostgreSQL)
df["Fecha"] = df["Fecha"].where(df["Fecha"].notna(), None)

# 3. Insertar fila por fila
insert_sql = """
INSERT INTO tasas_de_cambio
(fecha, tipo_tasa, from_moneda, to_moneda, factor)
VALUES (%s, %s, %s, %s, %s)
"""

data = []

insertados = 0
duplicados = 0

for _, row in df.iterrows():
    try:
        cursor.execute(
            insert_sql,
            (
                row["Fecha"],          # date o None
                row["TipoTasa"],
                row["FromMoneda"],
                row["ToMoneda"],
                float(row["Factor"]),
            )
        )
        insertados += 1
    except psycopg2.errors.UniqueViolation:
        conn.rollback()
        duplicados += 1

conn.commit()

print(f"✅ Insertados: {insertados}")
print(f"⚠️ Duplicados ignorados: {duplicados}")


cursor.close()
conn.close()

print("✔ Proceso de cargue finalizado")
