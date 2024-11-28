import random
import csv
from datetime import datetime, timedelta

def generar_nombre():
    nombres_m = [
        "Carlos", "Juan", "Luis", "Jorge", "Miguel", "David", "Javier", "Alejandro", 
        "Daniel", "Alberto", "Sergio", "Jose", "Manuel", "Antonio", "Francisco", 
        "Victor", "Pablo", "Ricardo", "Rafael", "Diego", "Eduardo", "Fernando", 
        "Adrian", "Julian", "Emilio", "Raul", "Cesar", "Hector", "Mario", "Enrique"
    ]

    nombres_f = [
        "Maria", "Ana", "Sofia", "Paula", "Diana", "Elena", "Isabel", "Laura", 
        "Marta", "Sara", "Lucia", "Irene", "Claudia", "Cristina", "Blanca", 
        "Carla", "Victoria", "Gabriela", "Camila", "Teresa", "Rosa", "Alejandra", 
        "Susana", "Silvia", "Beatriz", "Patricia", "Monica", "Veronica", "Andrea", "Noelia"
    ]

    apellidos = [
        "Gonzalez", "Martinez", "Lopez", "Hernandez", "Perez", "Sanchez", "Ramirez", 
        "Torres", "Flores", "Garcia", "Rodriguez", "Alonso", "Jimenez", "Ruiz", "Martin", 
        "Diaz", "Fernandez", "Morales", "Castillo", "Vargas", "Ortega", "Suarez", 
        "Guerrero", "Mendoza", "Cruz", "Rivera", "Navarro", "Dominguez", "Ramos", "Aguilar"
    ]

    nombre = random.choice(nombres_m + nombres_f)
    genero = "M" if nombre in nombres_m else "F"
    return f"{nombre} {random.choice(apellidos)} {random.choice(apellidos)}", genero

def generar_edad():
    edades = list(range(18, 31)) * 2 + list(range(31, 56))
    return random.choice(edades)

def generar_peso():
    pesos = list(range(60, 111))
    pesos_prob = [1 if 68 <= peso <= 76 else 0.5 for peso in pesos]
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
        "Perdida de peso": ["Dieta Mediterranea", "Dieta DASH", "Dieta Baja en Grasas", "Dieta Cetogenica", "Dieta Baja en Carbohidratos", "Dieta Vegetariana"],
        "Mantenimiento": ["Dieta Mediterranea", "Dieta DASH", "Dieta Baja en Grasas", "Dieta Vegetariana"],
        "Ganancia de peso": ["Dieta de Ganancia Muscular", "Dieta Hipercalorica", "Dieta de Proteinas"]
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

def generar_porciones(rango, probabilidad=None):
    if probabilidad:
        return random.choices(rango, weights=probabilidad, k=1)[0]
    return random.choice(rango)

def generar_ingesta_real(porciones, edad, objetivo):
    if edad < 30 and objetivo == "Perdida de peso":
        return porciones + (1 if random.random() < 0.7 else 0)
    return porciones

def calcular_peso_actual(peso_inicial, porciones, ingestas, imc, tiempo_meses, objetivo):
    if sum(ingestas) > sum(porciones):
        return peso_inicial + random.randint(2, 4)
    elif objetivo == "Perdida de peso" and imc > 24.9:
        return peso_inicial - round(0.5 * tiempo_meses, 1)
    return peso_inicial

def calcular_satisfaccion(peso_inicial, peso_actual):
    if peso_actual < peso_inicial:
        return random.choice(range(4, 6))
    elif peso_actual == peso_inicial:
        return random.choice(range(2, 4))
    return random.choice(range(0, 3))

def determinar_estado(satisfaccion):
    if satisfaccion < 3:
        return "Inactivo"
    return random.choices(["Activo", "Inactivo"], weights=[0.6, 0.4], k=1)[0]

def generar_citas(fecha_inicio, fecha_fin, satisfaccion):
    meses = (fecha_fin.year - fecha_inicio.year) * 12 + fecha_fin.month - fecha_inicio.month + 1
    citas_agendadas = meses
    citas_asistidas = citas_agendadas
    if satisfaccion < 3:
        citas_asistidas -= random.choice(range(1, 3))
    return citas_agendadas, citas_asistidas

def generar_registros(n):
    registros = []
    for i in range(1, n + 1):
        id_regimen = f"R{i:03d}"
        nombre, genero = generar_nombre()
        edad = generar_edad()
        peso_inicial = generar_peso()
        altura = generar_altura()
        imc = calcular_imc(peso_inicial, altura)
        objetivo = determinar_objetivo(imc)
        dieta = asignar_dieta(objetivo)
        costo, rango_costo = generar_costo(dieta)
        fecha_inicio = generar_fecha_inicio(objetivo, dieta)
        fecha_fin = generar_fecha_fin(fecha_inicio, dieta)
        
        porciones = {
            "Desayuno": generar_porciones(range(2, 5)),
            "Almuerzo": generar_porciones(range(2, 5)),
            "Cena": generar_porciones(range(2, 5)),
            "Colacion1": generar_porciones(range(0, 2)),
            "Colacion2": generar_porciones(range(0, 2))
        }
        
        ingestas = {
            k: generar_ingesta_real(v, edad, objetivo) for k, v in porciones.items()
        }
        
        tiempo_meses = (fecha_fin - fecha_inicio).days // 30
        peso_actual = calcular_peso_actual(peso_inicial, list(porciones.values()), list(ingestas.values()), imc, tiempo_meses, objetivo)
        satisfaccion = calcular_satisfaccion(peso_inicial, peso_actual)
        estado = determinar_estado(satisfaccion)
        citas_agendadas, citas_asistidas = generar_citas(fecha_inicio, fecha_fin, satisfaccion)

        registros.append({
            "IdPaciente": f"{i:03d}",
            "Nombre": nombre,
            "Edad": edad,
            "Genero": genero,
            "PesoInicial": peso_inicial,
            "Altura": altura,
            "IMC": imc,
            "Objetivo": objetivo,
            "IdRegimen": id_regimen,
            "NombreRegimen": dieta,
            "CostoRegimen": costo,
            "RangoCosto": rango_costo,
            "FechaInicioRegimen": fecha_inicio.strftime('%d/%m/%Y'),
            "FechaFinRegimen": fecha_fin.strftime('%d/%m/%Y'),
            "PorcionesDesayuno": porciones["Desayuno"],
            "PorcionesAlmuerzo": porciones["Almuerzo"],
            "PorcionesCena": porciones["Cena"],
            "PorcionesColacion1": porciones["Colacion1"],
            "PorcionesColacion2": porciones["Colacion2"],
            "IngestaRealDesayuno": ingestas["Desayuno"],
            "IngestaRealAlmuerzo": ingestas["Almuerzo"],
            "IngestaRealCena": ingestas["Cena"],
            "IngestaRealColacion1": ingestas["Colacion1"],
            "IngestaRealColacion2": ingestas["Colacion2"],
            "PesoActual": peso_actual,
            "SatisfaccionPaciente": satisfaccion,
            "EstadoPaciente": estado,
            "CitasAgendadas": citas_agendadas,
            "CitasAsistidas": citas_asistidas
        })
    return registros

def guardar_csv(nombre_archivo, registros):
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=registros[0].keys())
        escritor.writeheader()
        escritor.writerows(registros)

# Generar 100 registros y guardarlos en un archivo CSV
registros = generar_registros(2000)
guardar_csv('RegistrosNutriologo.csv', registros)
