import os

from simular_retos import generar_retos


# 1. Generar los datos sucios (se reutiliza la función, sin copiar código)

df = generar_retos()


# 2. Crear la carpeta de salida si no existe

os.makedirs("data/crudo", exist_ok=True)


# 3. Exportar a CSV, Excel y JSON

ruta_csv = "data/crudo/retos_sucio.csv"
ruta_xlsx = "data/crudo/retos_sucio.xlsx"
ruta_json = "data/crudo/retos_sucio.json"

df.to_csv(ruta_csv, index=False, encoding="utf-8")

df.to_excel(ruta_xlsx, index=False, sheet_name="retos")

df.to_json(
    ruta_json,
    orient="records",
    force_ascii=False,
    indent=2
)


# 4. Mostrar la ruta y el tamaño de cada archivo generado

for ruta in [ruta_csv, ruta_xlsx, ruta_json]:
    print(f"{ruta} -> {df.shape}")
