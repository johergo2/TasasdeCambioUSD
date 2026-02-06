import pdfplumber
import re
import pandas as pd

ruta_pdf = r"C:/Users/USER/Downloads/Factura_TIGO_Feb_2025.pdf"
ruta_excel = r"C:/Users/USER/Downloads/Datos_Factura.xlsx"

datos = {
    "n_Contrato": None,
    "NombreClie": None,
    "NitClie": None
}

# Leer el PDF
with pdfplumber.open(ruta_pdf) as pdf:
    texto = ""
    for page in pdf.pages:
        texto += (page.extract_text() or "") + "\n"

# Expresiones regulares (ajustables según la factura)
contrato = re.search(r"Contrato\s*[:\-]?\s*(\d+)", texto, re.IGNORECASE)
nombre = re.search(r"Nombre\s*(del\s*cliente)?\s*[:\-]?\s*(.+)", texto, re.IGNORECASE)
nit = re.search(r"(NIT|CC)\s*[:\-]?\s*([\d\.]+)", texto, re.IGNORECASE)

if contrato:
    datos["n_Contrato"] = contrato.group(1)

if nombre:
    datos["NombreClie"] = nombre.group(2).strip()

if nit:
    datos["NitClie"] = nit.group(2)

# Crear DataFrame
df = pd.DataFrame([datos])

# Exportar a Excel (.xlsx)
df.to_excel(ruta_excel, index=False, engine="openpyxl")

print("✅ Archivo Excel generado correctamente:")
print(ruta_excel)

input("Presiona Enter para salir...")
