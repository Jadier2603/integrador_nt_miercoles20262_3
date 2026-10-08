import random
import pandas as pd
import uuid

from faker import Faker

# 1. escoger el pais y lenguaje para simular los datos.

fake= Faker("es_CO")

# 2. sembrar historias

Faker.seed(42)
random.seed(42)

#id (texto (UUID)), 
#nombre (texto), 
#nit (texto), 
#sector (texto),****************** 
#contacto (texto), 
#correo (texto), 
#telefono (texto),
#activa (booleano),

#4. definir el numero de datos simulados(DASET).

FILAS=300

SECTORES=["Tecnología", "Salud", "Educación", "Finanzas", "Manufactura", "Construccion"]

# 5 construir funcion generadora de datos

def generar_datos_empresas(numero_registros=FILAS):
    filas=[]

    for _ in range(numero_registros):
        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": fake.company(),
            "nit": fake.numerify("#########-#"),
            "sector": random.choice(SECTORES),
            "contacto": fake.name(),
            "correo": fake.company_email(),
            "telefono": fake.numerify("3#########"),
            "activa": random.choice([True,False]),          
    })

    return filas

#6. Generar una muestra de índices para modificar
def  generar_muestra(datos,porcentaje):
    return datos.sample(frac=porcentaje,random_state=random.randint(0,9999)).index

#7. Ensuciar los datos
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    # Nombre: 10% con espacios sobrantes y 15% en mayúsculas.
    subconjunto_datos=generar_muestra(datos_df,0.1)
    datos_df.loc[subconjunto_datos,"nombre"]=" "+datos_df.loc[subconjunto_datos,"nombre"]+" "

    subconjunto_datos=generar_muestra(datos_df,0.15)
    datos_df.loc[subconjunto_datos,"nombre"]=datos_df.loc[subconjunto_datos,"nombre"].str.upper()

    # NIT: variar mayúsculas no aplica a este dato; se conserva el formato textual.
    subconjunto_datos=generar_muestra(datos_df,0.08)

    # Sector: introducir variantes de espacios y mayúsculas.
    subconjunto_datos=generar_muestra(datos_df,0.30)
    for i in subconjunto_datos:
        s = datos_df.loc[i,"sector"]
        datos_df.loc[i,"sector"] = random.choice([s.upper(), f" {s.lower()} ", s.lower()])

    # Contacto: 8% nulos.
    subconjunto_datos=generar_muestra(datos_df,0.08)
    datos_df.loc[subconjunto_datos,"contacto"]=None

    # Correo: 6% sin arroba.
    subconjunto_datos=generar_muestra(datos_df,0.06)
    datos_df.loc[subconjunto_datos,"correo"]=datos_df.loc[subconjunto_datos,"correo"].str.replace("@","", regex=False)

    # Teléfono: mezclar tres formatos.
    for i in datos_df.index:
        t = datos_df.loc[i,"telefono"]
        datos_df.loc[i,"telefono"] = random.choice([
            t,
            f"{t[:3]} {t[3:6]} {t[6:]}",
            f"+57 {t[:3]}-{t[3:6]}-{t[6:]}",
        ])

    # Activa: representar algunos booleanos como texto.
    datos_df["activa"] = datos_df["activa"].astype(object)
    subconjunto_datos=generar_muestra(datos_df,0.25)
    for i in subconjunto_datos:
        valor = datos_df.loc[i,"activa"]
        datos_df.loc[i,"activa"] = random.choice(["SI", "1"] if valor else ["No", "0"])

    # Repetir algunos NIT entre registros distintos.
    if len(datos_df) > 1:
        subconjunto_datos=generar_muestra(datos_df,0.03)
        for i in subconjunto_datos:
            otro = random.choice(datos_df.index[datos_df.index != i].tolist())
            datos_df.loc[i,"nit"] = datos_df.loc[otro,"nit"]

        # Duplicar filas exactas sin cambiar el número de registros.
        subconjunto_datos=generar_muestra(datos_df,0.05)
        for i in subconjunto_datos:
            otro = random.choice(datos_df.index[datos_df.index != i].tolist())
            datos_df.loc[i] = datos_df.loc[otro].copy()

    return datos_df

if __name__ == "__main__":
    df = ensuciar(pd.DataFrame(generar_datos_empresas()))
    print(df.shape)
    print(df.head())
    print(df.isna().sum())






   
