import random
import uuid

from faker import Faker

# 1. escoger el pais y lenguaje para simular los datos.

fake= Faker("es_CO")

# 2. sembrar historias

Faker.seed(42)
random.saed(42)

id (texto (UUID)), 
nombre (texto), 
nit (texto), 
sector (texto),****************** 
contacto (texto), 
correo (texto), 
telefono (texto),
activa (booleano),

#4. definir el numero de datos simulados(DASET).

FILAS=300