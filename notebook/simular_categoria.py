import random
import uuid
import pandas as pd
from faker import Faker

#1.escoger el pais  y lenguaje para simular datos
fake = Faker('es_co')

#2. sembrar semillas
Faker.seed(42)
random.seed(42)

#definir variables categorias y areas
CATEGORIAS = ["Electrónica", "Ropa", "Hogar", "Deportes"]
AREAS = ["Ventas", "Marketing", "IT", "Recursos Humanos"]

#3.definir el dato y su tipo a simular
#id (texto (UUID))
#nombre (texto)*
#descripcion (texto)
#area_responsable (texto)

#4.finir el numero de datos a simular (DATASET)
FILAS = 250

#construir funcion generadora de datos
def generar_datos_categoria(numero_registros = FILAS):
   filas=[]
   for _ in range(numero_registros):

        filas.append({
            "id": str(uuid.uuid4()),
            "nombre": random.choice(CATEGORIAS),
            "descripcion": fake.sentence(),
            "area_responsable": random.choice(AREAS)
        })
   return filas




#6. utilizaremos PANDAS para ordenar los datos simulados y crear un dataframe
tabla_ordenada_categoria = pd.DataFrame(generar_datos_categoria())

#7. ensuciar los datos simulados para probar la limpieza de datos
#7.1 generar una funcion que muestre los datos simulados
def generar_muestra():
    return datos.sample(fraccion=porcentaje, random_state=random.randint(0, 9999)).index    
#7.2 generar una funcion que ensucie los datos simulados
def ensuciar(datos_df):
    datos_df=datos_df.copy()

    #Se ensucia `nombre`: variantes del mismo nombre: 'Logistica', 'LOGISTICA', ' logistica ', 'logística'.
    subconjunto_datos = generar_muestra(datos_df, 0.1)
    datos_df.loc[subconjunto_datos, 'nombre'] = ""+datos_df.loc[subconjunto_datos, 'nombre']+" "

    #Se ensucia `descripcion`: 15% en None (nulos).
    subconjunto_datos = generar_muestra(datos_df, 0.15)
    datos_df.loc[subconjunto_datos, 'descripcion'] = None

    #Se ensucia `area_responsable`: 10% en none
    subconjunto_datos = generar_muestra(datos_df, 0.1)
    datos_df.loc[subconjunto_datos, 'area_responsable'] = None