import random
import uuid

from faker import Faker

# 1. escoger el pais y lenguaje para simular los datos.

fake= Faker("es_CO")

# 2. sembrar historias

Faker.seed(42)
random.saed(42)

#3 definir el dato y su tipo a simular

id (texto (UUID)), 
#nombre (texto), 
#nit (texto), 
#correo (texto), 
#contrasena_hash (texto), 
#rol (texto), ****************
#activo (boleano),
#fecha_registro (fecha y hora),

#4. definir el numero de datos simulados(DASET).

FILAS=400

