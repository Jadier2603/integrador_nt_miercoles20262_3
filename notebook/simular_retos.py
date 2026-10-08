import random
import pandas as pd
import uuid

from datetime import timedelta
from faker import Faker


# 1. Escoger el país y lenguaje para simular los datos

fake = Faker("es_CO")


# 2. Sembrar historias

Faker.seed(42)
random.seed(42)


# 3. Definir las constantes

ESTADOS = [
    "pendiente",
    "en_curso",
    "completado",
    "cerrado"
]

IDS_EMPRESA = [
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4())
]

IDS_CATEGORIA = [
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4())
]

IDS_PRIORIDAD = [
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4()),
    str(uuid.uuid4())
]


# 4. Definir el número de datos simulados (DATASET)

FILAS = 500


# 5. Construir función generadora de datos

def generar_retos(n=FILAS):

    filas = []

    # Generamos el 95% de las filas originales.
    # El otro 5% serán duplicados exactos.

    filas_originales = n - int(n * 0.05)

    for _ in range(filas_originales):

        # Fecha inicial del reto

        fecha_inicio = fake.date_between(
            start_date="-1y",
            end_date="+3m"
        )

        # Fecha final entre 15 y 180 días después

        fecha_fin = fecha_inicio + timedelta(
            days=random.randint(15, 180)
        )

        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.sentence(
                nb_words=6
            ).rstrip("."),
            "descripcion": fake.sentence(
                nb_words=12
            ),
            "fecha_inicio": fecha_inicio,
            "fecha_fin": fecha_fin,
            "estado": random.choice(ESTADOS),
            "id_empresa": random.choice(IDS_EMPRESA),
            "id_categoria": random.choice(IDS_CATEGORIA),
            "id_prioridad": random.choice(IDS_PRIORIDAD)
        })

    datos_df = pd.DataFrame(filas)

    # 5% de duplicados exactos.
    # Como n = 500, serán 25 duplicados.

    cantidad_duplicados = int(n * 0.05)

    duplicados = datos_df.sample(
        n=cantidad_duplicados,
        random_state=42
    ).copy()

    datos_df = pd.concat(
        [
            datos_df,
            duplicados
        ],
        ignore_index=True
    )

    # Mezclar las filas para que los duplicados
    # no queden todos al final.

    datos_df = datos_df.sample(
        frac=1,
        random_state=42
    ).reset_index(drop=True)

    return datos_df


# 6. Generar una muestra de índices para modificar

def generar_muestra(datos, porcentaje):

    return datos.sample(
        frac=porcentaje,
        random_state=random.randint(0, 9999)
    ).index


# 7. Ensuciar los datos

def ensuciar(datos_df):

    datos_df = datos_df.copy()


    # --------------------------------------------------------
    # Nombre:
    # 10% con espacios sobrantes
    # --------------------------------------------------------

    subconjunto_datos = generar_muestra(
        datos_df,
        0.10
    )

    datos_df.loc[
        subconjunto_datos,
        "nombre"
    ] = (
        " "
        + datos_df.loc[subconjunto_datos, "nombre"]
        + " "
    )


    # --------------------------------------------------------
    # Descripción:
    # 12% en None
    # --------------------------------------------------------

    subconjunto_datos = generar_muestra(
        datos_df,
        0.12
    )

    datos_df.loc[
        subconjunto_datos,
        "descripcion"
    ] = None


    # --------------------------------------------------------
    # Fecha inicio:
    # Mezclar formatos:
    # 2026-03-02
    # 02/03/2026
    # --------------------------------------------------------

    for i in datos_df.index:

        fecha = datos_df.loc[
            i,
            "fecha_inicio"
        ]

        datos_df.loc[
            i,
            "fecha_inicio"
        ] = random.choice([
            fecha.strftime("%Y-%m-%d"),
            fecha.strftime("%d/%m/%Y")
        ])


    # --------------------------------------------------------
    # Fecha fin:
    # 8% en None
    # --------------------------------------------------------

    subconjunto_datos = generar_muestra(
        datos_df,
        0.08
    )

    datos_df.loc[
        subconjunto_datos,
        "fecha_fin"
    ] = None


    # --------------------------------------------------------
    # Fecha fin:
    # 5% anterior a fecha_inicio
    # --------------------------------------------------------

    subconjunto_datos = generar_muestra(
        datos_df,
        0.05
    )

    for i in subconjunto_datos:

        fecha_inicio = datos_df.loc[
            i,
            "fecha_inicio"
        ]

        if "/" in fecha_inicio:

            fecha_inicio = pd.to_datetime(
                fecha_inicio,
                format="%d/%m/%Y"
            )

        else:

            fecha_inicio = pd.to_datetime(
                fecha_inicio,
                format="%Y-%m-%d"
            )

        fecha_invalida = (
            fecha_inicio
            - timedelta(
                days=random.randint(1, 30)
            )
        )

        datos_df.loc[
            i,
            "fecha_fin"
        ] = fecha_invalida.strftime(
            "%Y-%m-%d"
        )


    # --------------------------------------------------------
    # Estado:
    # Variantes:
    # en_curso
    # EN CURSO
    # Cerrado
    # --------------------------------------------------------

    subconjunto_datos = generar_muestra(
        datos_df,
        0.15
    )

    for i in subconjunto_datos:

        datos_df.loc[
            i,
            "estado"
        ] = random.choice([
            "en_curso",
            "EN CURSO",
            " Cerrado "
        ])


    return datos_df


# 8. Ejecutar el programa

if __name__ == "__main__":

    df = generar_retos()

    df = ensuciar(df)

    print(df.shape)

    print(df.head())

    print(df.isna().sum())