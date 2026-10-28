import random
import uuid

import pandas as pd
from faker import Faker


# 1. Escoger el pais y lenguaje para simular datos

fake = Faker("es_CO")  # Faker para Colombia


# 2. Sembrar semillas
# Faker.seed(42) y random.seed(42) para que el archivo sea reproducible.

Faker.seed(42)
random.seed(42)


# 3. Definir el dato y su tipo a simular

# id (texto (UUID)),
# fecha_registro (fecha y hora),
# observacion (texto),
# estado (texto),************a tratar
# id_usuario (texto (UUID)),
# id_reto (texto (UUID)).


# 4. Definir el numero de datos simulados (DATASET)

FILAS = 800

# Cantidad de usuarios y retos que existiran en el sistema
# (los registros solo pueden apuntar a estos ids)
USUARIOS = 400
RETOS = 120

# Estados limpios (valores validos del negocio)
ESTADOS = ["inscrito", "en proceso", "finalizado"]


# 5. Construir funciones generadoras de datos

def _ids_falsos(cantidad):
    """Genera ids (UUID) falsos para usuarios y retos."""
    return [str(uuid.uuid4()) for _ in range(cantidad)]


# 5.1. Funcion que genera los 800 registros LIMPIOS

def generar_registros(n=FILAS):
    """Genera el dataset de registros LIMPIO (solo las n filas base).

    Devuelve el DataFrame (return df) para poder importarlo desde el
    script de exportacion o pasarlo a ensuciar().
    """

    # Ids falsos de usuarios y retos a los que pueden apuntar los registros
    ids_usuario = _ids_falsos(USUARIOS)
    ids_reto = _ids_falsos(RETOS)

    filas = []

    for _ in range(n):
        filas.append({
            "id": str(uuid.uuid4()),
            "fecha_registro": fake.date_time_between(start_date="-1y", end_date="now"),
            "observacion": fake.sentence(nb_words=10),
            "estado": random.choice(ESTADOS),
            "id_usuario": random.choice(ids_usuario),
            "id_reto": random.choice(ids_reto),
        })

    return pd.DataFrame(filas)


# 6. Ensuciar los datos

## 6.1 Generar una funcion que devuelva una muestra (los indices)

def generar_muestra(datos, porcentaje):
    return datos.sample(frac=porcentaje, random_state=random.randint(0, 9999)).index


## 6.2 Funcion que ensucia los datos.
##     Cada porcentaje se saca SOBRE LAS 800 FILAS BASE (n * porcentaje),
##     asi la tabla final se queda en 800 filas y cada % es exacto.

def ensuciar(datos_df, n=FILAS):
    datos_df = datos_df.copy()

    # --- Atributo fecha_registro -----------------------------
    # Se hace PRIMERO, porque las operaciones .str sobre 'estado' convierten
    # la columna a texto y rompen el acceso .dt sobre las fechas.

    ## 12% con formato latino (dd/mm/aaaa) en vez del formato ISO
    subconjunto_datos = generar_muestra(datos_df, 0.12)
    datos_df["fecha_registro"] = datos_df["fecha_registro"].astype(str)
    datos_df.loc[subconjunto_datos, "fecha_registro"] = (
        pd.to_datetime(datos_df.loc[subconjunto_datos, "fecha_registro"])
        .dt.strftime("%d/%m/%Y %H:%M")
        .astype(str)
    )

    # --- Atributo estado -------------------------------------

    ## 10% en MAYUSCULAS
    subconjunto_datos = generar_muestra(datos_df, 0.10)
    datos_df.loc[subconjunto_datos, "estado"] = (
        datos_df.loc[subconjunto_datos, "estado"].str.upper()
    )

    ## 8% con espacios sobrantes (ej: " inscrito ")
    subconjunto_datos = generar_muestra(datos_df, 0.08)
    datos_df.loc[subconjunto_datos, "estado"] = (
        " " + datos_df.loc[subconjunto_datos, "estado"] + " "
    )

    ## 5% con la primera letra en mayuscula (ej: "Inscrito")
    subconjunto_datos = generar_muestra(datos_df, 0.05)
    datos_df.loc[subconjunto_datos, "estado"] = (
        datos_df.loc[subconjunto_datos, "estado"].str.capitalize()
    )

    ## 4% vacios (None)
    subconjunto_datos = generar_muestra(datos_df, 0.04)
    datos_df.loc[subconjunto_datos, "estado"] = None

    # --- Atributo observacion --------------------------------

    ## 20% vacios (None)
    subconjunto_datos = generar_muestra(datos_df, 0.20)
    datos_df.loc[subconjunto_datos, "observacion"] = None

    # --- Duplicados y repetidos (sobre las 800) ---------------

    ## 10% con el par 'id_usuario' + 'id_reto' repetido
    ## (el mismo usuario inscrito dos veces en el mismo reto)
    total_pares_repetidos = int(n * 0.10)

    for _ in range(total_pares_repetidos):
        fila_origen = datos_df.sample(n=1).iloc[0]
        posicion = random.choice(datos_df.index)
        datos_df.loc[posicion, "id_usuario"] = fila_origen["id_usuario"]
        datos_df.loc[posicion, "id_reto"] = fila_origen["id_reto"]

    ## 5% de duplicados exactos (mismo id y todos los campos)
    total_duplicados = int(n * 0.05)

    for _ in range(total_duplicados):
        fila_origen = datos_df.sample(n=1).iloc[0]
        posicion = random.choice(datos_df.index)
        datos_df.loc[posicion] = fila_origen

    return datos_df


# 7. Ejecucion principal

if __name__ == "__main__":
    df = generar_registros(n=FILAS)
    print("df.shape (limpio):", df.shape)

    df = ensuciar(df, n=FILAS)
    print("df.shape (sucio):", df.shape)

    print("\ndf.head():")
    print(df.head())

    print("\ndf.isna().sum():")
    print(df.isna().sum())
