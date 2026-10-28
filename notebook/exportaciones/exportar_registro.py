# Rutina para generar archivos de REGISTROS en diferentes formatos (CSV, JSON, Excel)

import sys
from pathlib import Path

# 1. Configuracion general de las rutas

NOMBRE_ENTIDAD = "registro"
CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA_NOTEBOOK = CARPETA_PROYECTO / "notebook"

CARPETA_CRUDOS = CARPETA_PROYECTO / "datos" / "crudos"
CARPETA_LIMPIOS = CARPETA_PROYECTO / "datos" / "limpios"
CARPETA_REPORTES = CARPETA_PROYECTO / "datos" / "reportes"

# Para poder importar los modulos de las carpetas hermanas
sys.path.insert(0, str(CARPETA_NOTEBOOK / "simulaciones"))

from simular_registro import generar_registros, ensuciar, FILAS


# 2. Funciones genericas para crear los archivos

def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta


def exportar_csv(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, sep=";", index=False, encoding="utf-8-sig")
    return ruta


def exportar_json(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", indent=2,
                     date_format="iso", force_ascii=False)
    return ruta


def exportar_excel(datos_df, carpeta, nombre_archivo):
    ruta = preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, engine="openpyxl", index=False)
    return ruta


# 3. Llamar las funciones para generar los archivos

def exportar_registros_crudos(datos_df):
    return [
        exportar_csv(datos_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_json(datos_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_excel(datos_df, CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
    ]


def exportar_registros_limpios(datos_df):
    return [
        exportar_csv(datos_df, CARPETA_LIMPIOS, f"{NOMBRE_ENTIDAD}_limpio"),
        exportar_json(datos_df, CARPETA_LIMPIOS, f"{NOMBRE_ENTIDAD}_limpio"),
        exportar_excel(datos_df, CARPETA_LIMPIOS, f"{NOMBRE_ENTIDAD}_limpio"),
    ]


# 4. Ejecucion principal: simula, ensucia y exporta los CRUDOS

if __name__ == "__main__":
    df_sucio = ensuciar(generar_registros(n=FILAS), n=FILAS)

    print("Archivos crudos generados:")
    for ruta in exportar_registros_crudos(df_sucio):
        print(" -", ruta)
