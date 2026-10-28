# Limpieza de los datos de REGISTROS (lee los crudos y exporta los limpios)

import sys
from pathlib import Path

import pandas as pd

# 1. Configuracion general de las rutas

CARPETA_PROYECTO = Path(__file__).resolve().parents[2]
CARPETA_NOTEBOOK = CARPETA_PROYECTO / "notebook"

# Para poder importar los modulos de las carpetas hermanas
sys.path.insert(0, str(CARPETA_NOTEBOOK / "simulaciones"))
sys.path.insert(0, str(CARPETA_NOTEBOOK / "exportaciones"))

from simular_registro import ESTADOS
from exportar_registro import CARPETA_CRUDOS, exportar_registros_limpios

RUTA_CRUDO = CARPETA_CRUDOS / "registro_crudo.csv"

ESTADO_VACIO = "sin_estado"
OBSERVACION_VACIA = "sin observacion"


# 2. Funciones de limpieza (una por problema)

def limpiar_fechas(datos_df):
    """Unifica los dos formatos (ISO y dd/mm/aaaa) a datetime."""
    texto = datos_df["fecha_registro"].astype(str).str.strip()
    iso = pd.to_datetime(texto, format="%Y-%m-%d %H:%M:%S", errors="coerce")
    latino = pd.to_datetime(texto, format="%d/%m/%Y %H:%M", errors="coerce")
    datos_df["fecha_registro"] = iso.fillna(latino)
    return datos_df


def limpiar_estado(datos_df):
    """Quita espacios, pasa a minuscula y valida contra ESTADOS."""
    estado = datos_df["estado"].str.strip().str.lower()
    estado = estado.where(estado.isin(ESTADOS))      # lo invalido queda vacio
    datos_df["estado"] = estado.fillna(ESTADO_VACIO)
    return datos_df


def limpiar_observacion(datos_df):
    datos_df["observacion"] = datos_df["observacion"].fillna(OBSERVACION_VACIA)
    return datos_df


def eliminar_duplicados_exactos(datos_df):
    return datos_df.drop_duplicates()


def eliminar_pares_repetidos(datos_df):
    """Deja una sola inscripcion por usuario y reto (la mas antigua)."""
    datos_df = datos_df.sort_values("fecha_registro")
    return datos_df.drop_duplicates(subset=["id_usuario", "id_reto"], keep="first")


def limpiar_registros(datos_df):
    """Aplica todas las limpiezas en orden y devuelve el DataFrame limpio."""
    datos_df = datos_df.copy()
    datos_df = limpiar_fechas(datos_df)
    datos_df = limpiar_estado(datos_df)
    datos_df = limpiar_observacion(datos_df)

    antes = len(datos_df)
    datos_df = eliminar_duplicados_exactos(datos_df)
    print(f"Duplicados exactos eliminados: {antes - len(datos_df)}")

    antes = len(datos_df)
    datos_df = eliminar_pares_repetidos(datos_df)
    print(f"Pares usuario+reto repetidos eliminados: {antes - len(datos_df)}")

    return datos_df.reset_index(drop=True)


# 3. Ejecucion principal: lee crudos -> limpia -> exporta limpios

if __name__ == "__main__":
    if not RUTA_CRUDO.exists():
        raise SystemExit(
            f"No existe {RUTA_CRUDO}. Ejecuta primero exportar_registro.py"
        )

    df_crudo = pd.read_csv(RUTA_CRUDO, sep=";", encoding="utf-8-sig")
    print("df.shape (crudo):", df_crudo.shape)

    df_limpio = limpiar_registros(df_crudo)
    print("df.shape (limpio):", df_limpio.shape)

    print("\nValores de estado:")
    print(df_limpio["estado"].value_counts())

    print("\nArchivos limpios generados:")
    for ruta in exportar_registros_limpios(df_limpio):
        print(" -", ruta)
