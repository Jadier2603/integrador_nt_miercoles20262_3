##Tarea proxima semana, crear carpetas 
##Rutina para generar archivos en diferentes formatos con python 
##VAMos
from pathlib import Path

#1. Configuracion general de las rutas 

NOMBRE_ENTIDAD="usuario"
CARPETA_PROYECTO=Path(__file__).resolve().parents[2]

print(f"OEEEEEEE: {CARPETA_PROYECTO}")

CARPETA_CRUDOS = CARPETA_PROYECTO / "datos"/"crudos"

CARPETA_LIMPIOS = CARPETA_PROYECTO / "datos"/"limpios"

CARPETA_REPORTES = CARPETA_PROYECTO / "datos"/"reportes"

##2. Funciones Genericas paara ccrear los archivos 
def preparar_carpeta(carpeta):
    carpeta.mkdir(parents=True, exist_ok=True)
    return carpeta 

def exportar_csv(datos_df,carpeta,nombre_archivo):
    ruta=preparar_carpeta(carpeta) / f"{nombre_archivo}.csv"
    datos_df.to_csv(ruta, sep=";")
    return ruta


def exportar_json(datos_df,carpeta,nombre_archivo):
    ruta=preparar_carpeta(carpeta) / f"{nombre_archivo}.json"
    datos_df.to_json(ruta, orient="records", ident="2")
    return ruta


def exportar_excel(datos_df,carpeta,nombre_archivo):
    ruta=preparar_carpeta(carpeta) / f"{nombre_archivo}.xlsx"
    datos_df.to_excel(ruta, engine="openpyxl")
    return ruta


##3. Llamar las funciones para generar los archivoss


def exportar_usuarios_crudos(datos_df):
    return [

        exportar_csv(datos_df,CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_json(datos_df,CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo"),
        exportar_excel(datos_df,CARPETA_CRUDOS, f"{NOMBRE_ENTIDAD}_crudo")

    ]

    

##Tarea proxima semana, crear carpetas en mi proyecto INTEGRADOR









