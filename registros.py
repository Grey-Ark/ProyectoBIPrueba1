import random
import csv
from datetime import datetime, timedelta
import numpy as np

def generar_nombre():
    nombres = ["Carlos", "Juan", "Maria", "Ana", "Luis", "Sofia", "Jorge", "Paula", "Miguel", "Diana", "David", "Javier", "Alejandro", "Daniel", "Alberto", "Sergio", "Jose", "Manuel", "Antonio", "Francisco", "Elena", "Isabel", "Laura", "Marta", "Sara", "Lucia", "Irene", "Claudia", "Cristina", "Blanca"]
    apellidos = ["Gonzalez", "Martinez", "Lopez", "Hernandez", "Perez", "Sanchez", "Ramirez", "Torres", "Flores", "Garcia", "Rodriguez", "Alonso", "Jimenez", "Ruiz", "Martin", "Garcia", "Fernandez", "Lopez", "Gonzalez", "Sanchez", "Romero", "Moreno", "Alvarez", "Gutierrez", "Diaz", "Munoz", "Navarro", "Dominguez", "Vargas", "Castro"]
    return f"{random.choice(nombres)} {random.choice(apellidos)} {random.choice(apellidos)}"

def generar_edad():
    edades = list(range(18, 31)) * 2 + list(range(31, 56))  # Más probabilidades entre 18 y 30
    return random.choice(edades)

def generar_genero():
    return "F" if random.random() < 0.52 else "M"

def generar_peso():
    pesos = list(range(60, 111))
    pesos_prob = [1 if 68 <= peso <= 76 else 0.5 for peso in pesos]  # Mayor probabilidad entre 68 y 76
    return random.choices(pesos, weights=pesos_prob, k=1)[0]

def generar_altura():
    return round(random.uniform(1.60, 1.82), 2)

def calcular_imc(peso, altura):
    return round(peso / (altura ** 2), 2)

def determinar_objetivo(imc):
    if imc < 18.5:
        return "Ganancia de peso"
    elif 18.5 <= imc <= 24.9:
        return "Mantenimiento"
    else:
        return "Perdida de peso"

def asignar_dieta(objetivo):
    dietas = {
        "Perdida de peso": ["Dieta Mediterranea", "Dieta DASH", "Dieta Baja en Grasas", "Dieta Cetogenica"],
        "Mantenimiento": ["Dieta Mediterranea", "Dieta DASH", "Dieta Baja en Grasas"],
        "Ganancia de peso": ["Dieta de Ganancia Muscular"]
    }
    return random.choice(dietas[objetivo])

def generar_costo(dieta):
    costos = list(range(250, 851, 50))
    costos_prob = [1 if costo <= 400 else (2 if dieta in ["Dieta Cetogenica", "Dieta de Ganancia Muscular"] else 0.5) for costo in costos]
    costo = random.choices(costos, weights=costos_prob, k=1)[0]
    if costo <= 400:
        rango = "Economico"
    elif 450 <= costo <= 550:
        rango = "Medio"
    else:
        rango = "Alto"
    return costo, rango

def generar_fecha_inicio(objetivo, dieta):
    if objetivo == "Perdida de peso" and dieta == "Dieta Mediterranea":
        fechas_prob = [datetime(2023, 7, 1) + timedelta(days=i) for i in range(20)]
        fechas_prob.extend([datetime(2023, 1, 1) + timedelta(days=i) for i in range(365)])
        return random.choice(fechas_prob)
    return datetime(2023, 1, 1) + timedelta(days=random.randint(0, 484))

def generar_fecha_fin(fecha_inicio, dieta):
    meses_duracion = random.randint(1, 8)
    if dieta == "Dieta Cetogenica" and datetime(2023, 1, 1) <= fecha_inicio <= datetime(2023, 1, 30):
        meses_duracion = max(meses_duracion, 2)
    return fecha_inicio + timedelta(days=30 * meses_duracion)

def generar_registros(n):
    registros = []
    for _ in range(n):
        nombre = generar_nombre()
        edad = generar_edad()
        genero = generar_genero()
        peso = generar_peso()
        altura = generar_altura()
        imc = calcular_imc(peso, altura)
        objetivo = determinar_objetivo(imc)
        dieta = asignar_dieta(objetivo)
        costo, rango_costo = generar_costo(dieta)
        fecha_inicio = generar_fecha_inicio(objetivo, dieta)
        fecha_fin = generar_fecha_fin(fecha_inicio, dieta)
        registros.append({
            "Nombre": nombre,
            "Edad": edad,
            "Genero": genero,
            "PesoInicial": peso,
            "Altura": altura,
            "IMC": imc,
            "Objetivo": objetivo,
            "Nombre del Regimen": dieta,
            "CostoRegimen": costo,
            "RangoCosto": rango_costo,
            "FechaInicio": fecha_inicio.strftime('%d/%m/%Y'),
            "FechaFinRegimen": fecha_fin.strftime('%d/%m/%Y')
        })
    return registros

def guardar_csv(nombre_archivo, registros):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=registros[0].keys())
        escritor.writeheader()
        escritor.writerows(registros)

# Generar 100 registros y guardarlos en un archivo CSV
registros = generar_registros(100)
guardar_csv('registros_dietas.csv', registros)
