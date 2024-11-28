import pandas as pd
import numpy as np
import mysql.connector
import re
import unicodedata
import random
import csv
from datetime import datetime, timedelta
from sqlalchemy import create_engine, text

def importar_script_bd(archivo_sql, archivo_sql_salida):
    print("Importando Script para la Base de Datos...")
    
    try:
        conexion = mysql.connector.connect(
            host = "localhost",
            user = "root",
            password = "",
            database = "nutriologo"
        )
        cursor = conexion.cursor()
        print("Conexion exitosa...")
    except mysql.connector.Error as err:
        print(f"Error de conexión: {err}")
        return
    
    try:
        with open(archivo_sql, 'r', encoding='utf-8') as file:
            contenido = file.read()
            
        contenido = contenido.replace('`', "'")
        contenido = re.sub(r'--.*\n', '', contenido)
        contenido = re.sub(r"'([^']*)'", r"`\1`", contenido)
        contenido = re.sub(r'\s+VISIBLE', '', contenido)
        contenido = '\n'.join([line.strip() for line in contenido.splitlines() if line.strip() != ''])
        
        consultas = []
        consulta_actual = ''
        for linea in contenido.splitlines():
            consulta_actual += ' ' + linea.strip()
            if consulta_actual.endswith(';'):
                consultas.append(consulta_actual)
                consulta_actual = ''
                
        if consulta_actual:
            consultas.append(consulta_actual)
        
        consultas_limpias = consultas
        
        with open(archivo_sql_salida, 'w', encoding='utf-8') as file_salida:
            for consulta in consultas_limpias:
                file_salida.write(consulta + '\n')
                
        print(f"Consultas limpias guardadas en: {archivo_sql_salida}")
        
        for consulta in consultas_limpias:
            try:
                cursor.execute(consulta)
                conexion.commit()
                print(f"Consulta ejecutada: {consulta}")
            except mysql.connector.Error as err:
                print(f"Error ejecutando consulta: {consulta}")
                print(f"Error: {err}")
                
    except FileNotFoundError:
        print(f"Archivo no encontrado: {archivo_sql}")
    except Exception as e:
        print(f"Error procesando el archivo SQL: {e}")
        
    cursor.close()
    conexion.close()
    input("Finalizar...")

def generar_registros_csv(nombre_archivo, num_registros):
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

    registros = []
    for i in range(1, num_registros + 1):
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
    
    with open(nombre_archivo, mode='w', newline='', encoding='utf-8') as archivo:
        escritor = csv.DictWriter(archivo, fieldnames=registros[0].keys())
        escritor.writeheader()
        escritor.writerows(registros)

def preparar_archivo_csv(ruta_csv):
    print("Preparando archivo CSV...")
    
    # Cargar el archivo CSV
    try:
        df = pd.read_csv(ruta_csv, low_memory=False, encoding='utf-8')
        print("Archivo CSV cargado correctamente con codificación UTF-8.")
    except UnicodeDecodeError:
        print("Error de codificación con UTF-8. Intentando con latin1...")
        try:
            df = pd.read_csv(ruta_csv, low_memory=False, encoding='latin1')
            print("Archivo CSV cargado correctamente con codificación latin1.")
        except FileNotFoundError:
            print(f"Archivo no encontrado: {ruta_csv}")
            return
        except Exception as e:
            print(f"Error cargando el archivo CSV: {e}")
            return
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        return
    except Exception as e:
        print(f"Error cargando el archivo CSV: {e}")
        return
    
    # Procesar datos
    try:
        # Quitar acentos de la columna 'Nombre'
        if 'Nombre' in df.columns:
            df['Nombre'] = df['Nombre'].apply(lambda x: unicodedata.normalize('NFKD', str(x)).encode('ascii', 'ignore').decode('utf-8') if pd.notna(x) else x)
            print("Acentos eliminados de la columna 'Nombre'.")
        else:
            print("Error: La columna 'Nombre' no existe en el archivo CSV.")
            return
        
        # Eliminar duplicados basados en la columna 'Nombre'
        df = df.drop_duplicates(subset='Nombre', keep='first')
        print("Registros duplicados eliminados basados en la columna 'Nombre'.")
        
        # Guardar el archivo limpio
        ruta_csv_salida = ruta_csv.replace('.csv', '_limpio.csv')
        df.to_csv(ruta_csv_salida, index=False, encoding='utf-8')
        print(f"Archivo CSV limpio guardado en: {ruta_csv_salida}")
    except KeyError:
        print("Error: La columna 'Nombre' no existe en el archivo CSV.")
    except Exception as e:
        print(f"Error procesando el archivo CSV: {e}")

    input("Presiona Enter para finalizar...")
    


def insertar_datos_dimensiones(ruta_csv):
    print("Insertando datos en tablas de dimensiones...")
    
    try:
        df = pd.read_csv(ruta_csv, low_memory=False, encoding='latin1')
        print("Archivo CSV cargado correctamente con codificación.")
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        return
    except Exception as e:
        print(f"Error cargando el archivo: {e}")
        return
    
    df_Genero = df[['Genero']].drop_duplicates()
    df_Objetivo = df[['Objetivo']].drop_duplicates()
    df_IdRegimen = df[['IdRegimen']].drop_duplicates()
    df_NombreRegimen = df[['NombreRegimen']].drop_duplicates()
    df_CostoRegimen = df[['CostoRegimen']].drop_duplicates()
    df_RangoCosto = df[['RangoCosto']].drop_duplicates()
    df_PorcionesDesayuno = df[['PorcionesDesayuno']].drop_duplicates()
    df_PorcionesAlmuerzo = df[['PorcionesAlmuerzo']].drop_duplicates()
    df_PorcionesCena = df[['PorcionesCena']].drop_duplicates()
    df_PorcionesColacion1 = df[['PorcionesColacion1']].drop_duplicates()
    df_PorcionesColacion2 = df[['PorcionesColacion2']].drop_duplicates()
    df_IngestaRealDesayuno = df[['IngestaRealDesayuno']].drop_duplicates()
    df_IngestaRealAlmuerzo = df[['IngestaRealAlmuerzo']].drop_duplicates()
    df_IngestaRealCena = df[['IngestaRealCena']].drop_duplicates()
    df_IngestaRealColacion1 = df[['IngestaRealColacion1']].drop_duplicates()
    df_IngestaRealColacion2 = df[['IngestaRealColacion2']].drop_duplicates()
    df_SatisfaccionPaciente = df[['SatisfaccionPaciente']].drop_duplicates()
    df_EstadoPaciente = df[['EstadoPaciente']].drop_duplicates()
    df_CitasAgendadas = df[['CitasAgendadas']].drop_duplicates()
    df_CitasAsistidas = df[['CitasAsistidas']].drop_duplicates()
    
    
    df_Genero = df_Genero.sort_values(by='Genero').reset_index(drop=True)
    df_Objetivo = df_Objetivo.sort_values(by='Objetivo').reset_index(drop=True)
    df_IdRegimen = df_IdRegimen.sort_values(by='IdRegimen').reset_index(drop=True)
    df_NombreRegimen = df_NombreRegimen.sort_values(by='NombreRegimen').reset_index(drop=True)
    df_CostoRegimen = df_CostoRegimen.sort_values(by='CostoRegimen').reset_index(drop=True)
    df_RangoCosto = df_RangoCosto.sort_values(by='RangoCosto').reset_index(drop=True)
    df_PorcionesDesayuno = df_PorcionesDesayuno.sort_values(by='PorcionesDesayuno').reset_index(drop=True)
    df_PorcionesAlmuerzo = df_PorcionesAlmuerzo.sort_values(by='PorcionesAlmuerzo').reset_index(drop=True)
    df_PorcionesCena = df_PorcionesCena.sort_values(by='PorcionesCena').reset_index(drop=True)
    df_PorcionesColacion1 = df_PorcionesColacion1.sort_values(by='PorcionesColacion1').reset_index(drop=True)
    df_PorcionesColacion2 = df_PorcionesColacion2.sort_values(by='PorcionesColacion2').reset_index(drop=True)
    df_IngestaRealDesayuno = df_IngestaRealDesayuno.sort_values(by='IngestaRealDesayuno').reset_index(drop=True)
    df_IngestaRealAlmuerzo = df_IngestaRealAlmuerzo.sort_values(by='IngestaRealAlmuerzo').reset_index(drop=True)
    df_IngestaRealCena = df_IngestaRealCena.sort_values(by='IngestaRealCena').reset_index(drop=True)
    df_IngestaRealColacion1 = df_IngestaRealColacion1.sort_values(by='IngestaRealColacion1').reset_index(drop=True)
    df_IngestaRealColacion2 = df_IngestaRealColacion2.sort_values(by='IngestaRealColacion2').reset_index(drop=True)
    df_SatisfaccionPaciente = df_SatisfaccionPaciente.sort_values(by='SatisfaccionPaciente').reset_index(drop=True)
    df_EstadoPaciente = df_EstadoPaciente.sort_values(by='EstadoPaciente').reset_index(drop=True)
    df_CitasAgendadas = df_CitasAgendadas.sort_values(by='CitasAgendadas').reset_index(drop=True)
    df_CitasAsistidas = df_CitasAsistidas.sort_values(by='CitasAsistidas').reset_index(drop=True)

    try:
        conn = mysql.connector.connect(
            host = 'localhost',
            user = 'root',
            password = '',
            database = 'nutriologo'
        )
        cursor = conn.cursor()
        print("Conexion a la base de datos establecida.")
    except mysql.connector.Error as err:
        print(f"Error al conectar a la base de datos: {err}")
        return
    
    def insert(df, tabla, columna):
        sql = f"INSERT IGNORE INTO {tabla} ({columna}) VALUES (%s)"
        
        for valor in df[columna]:
            if pd.notna(valor):
                print(f"Insertando valor: {valor}")
                cursor.execute(sql, (valor,))
                
        conn.commit()
        
    insert(df_Genero, 'Genero', 'Genero')
    insert(df_Objetivo, 'Objetivo', 'Objetivo')
    insert(df_IdRegimen, 'IdRegimen', 'IdRegimen')
    insert(df_NombreRegimen, 'NombreRegimen', 'NombreRegimen')
    insert(df_CostoRegimen, 'CostoRegimen', 'CostoRegimen')
    insert(df_RangoCosto, 'RangoCosto', 'RangoCosto')
    insert(df_PorcionesDesayuno, 'PorcionesDesayuno', 'PorcionesDesayuno')
    insert(df_PorcionesAlmuerzo, 'PorcionesAlmuerzo', 'PorcionesAlmuerzo')
    insert(df_PorcionesCena, 'PorcionesCena', 'PorcionesCena')
    insert(df_PorcionesColacion1, 'PorcionesColacion1', 'PorcionesColacion1')
    insert(df_PorcionesColacion2, 'PorcionesColacion2', 'PorcionesColacion2')
    insert(df_IngestaRealDesayuno, 'IngestaRealDesayuno', 'IngestaRealDesayuno')
    insert(df_IngestaRealAlmuerzo, 'IngestaRealAlmuerzo', 'IngestaRealAlmuerzo')
    insert(df_IngestaRealCena, 'IngestaRealCena', 'IngestaRealCena')
    insert(df_IngestaRealColacion1, 'IngestaRealColacion1', 'IngestaRealColacion1')
    insert(df_IngestaRealColacion2, 'IngestaRealColacion2', 'IngestaRealColacion2')
    insert(df_SatisfaccionPaciente, 'SatisfaccionPaciente', 'SatisfaccionPaciente')
    insert(df_EstadoPaciente, 'EstadoPaciente', 'EstadoPaciente')
    insert(df_CitasAgendadas, 'CitasAgendadas', 'CitasAgendadas')
    insert(df_CitasAsistidas, 'CitasAsistidas', 'CitasAsistidas')

    cursor.close()
    conn.close()
    print("Datos insertados correctamente en las tablas de dimensiones")
    input("Finalizar...")
    

def insertar_datos_hechos(ruta_csv):
    print("Insertando datos en la tabla de hechos...")
    
    # Cargar el CSV
    try:
        df = pd.read_csv(ruta_csv, low_memory=False, encoding='latin1')
        print("Archivo CSV cargado correctamente con codificación.")
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        return
    except Exception as e:
        print(f"Error cargando el archivo: {e}")
        return

    # Convertir las columnas de fecha al formato YYYY-MM-DD
    for col in ['FechaInicioRegimen', 'FechaFinRegimen']:
        if col in df.columns:
            try:
                # Convertir al formato de fecha y manejar errores
                df[col] = pd.to_datetime(df[col], format='%d/%m/%Y', dayfirst=True, errors='coerce')
                # Reemplazar valores NaT con una fecha por defecto
                df[col] = df[col].fillna(pd.Timestamp('1970-01-01')).dt.strftime('%Y-%m-%d')
            except Exception as e:
                print(f"Error al convertir la columna {col}: {e}")
                return
    
    # Conexión a la base de datos
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nutriologo'
        )
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos.")
    except mysql.connector.Error as err:
        print(f"Error al conectarse a la base de datos: {err}")
        return

    # Determinar las columnas
    columnas_especificas = ['Nombre', 'Edad', 'PesoInicial', 'Altura', 'IMC', 'FechaInicioRegimen', 'FechaFinRegimen', 'PesoActual']
    try:
        cursor.execute("DESCRIBE paciente")
        columnas_tabla = [col[0] for col in cursor.fetchall()]
        columnas_extras = [col for col in columnas_tabla if col not in columnas_especificas]
    except mysql.connector.Error as err:
        print(f"Error al describir la tabla: {err}")
        cursor.close()
        conn.close()
        return

    # Excluir la clave primaria de las columnas a actualizar
    columnas_actualizables = [col for col in columnas_especificas if col != 'IdPaciente']

    # Inserción de datos
    for idx, row in df.iterrows():
        datos_hechos = []
        for col in columnas_especificas:
            valor = row[col] if col in row else None
            datos_hechos.append(valor if pd.notna(valor) else None)
        
        datos_hechos += [0] * len(columnas_extras)
        
        # Construir el SQL dinámicamente
        sql_hechos = f"""
            INSERT INTO paciente ({', '.join(columnas_especificas + columnas_extras)})
            VALUES ({', '.join(['%s'] * (len(columnas_especificas) + len(columnas_extras)))} )
            ON DUPLICATE KEY UPDATE
            {', '.join([f"{col}=VALUES({col})" for col in columnas_actualizables])}
        """
        
        try:
            cursor.execute(sql_hechos, datos_hechos)
            conn.commit()
        except mysql.connector.Error as err:
            print(f"Error al insertar los datos (fila {idx}): {err}")
            break  # Salir del bucle si hay un error crítico

    # Cerrar conexiones
    cursor.close()
    conn.close()
    print("Datos insertados en la tabla de hechos correctamente")
    input("Finalizar...")


def insertar_dimensiones(ruta_csv):
    print("Cargando el archivo CSV...")
    try:
        df = pd.read_csv(ruta_csv, low_memory=False, encoding='latin1')
        df.columns = df.columns.str.strip()  # Limpia espacios extra en los nombres de columnas
        print("Archivo CSV cargado correctamente.")
    except FileNotFoundError:
        print(f"Archivo no encontrado: {ruta_csv}")
        return
    except Exception as e:
        print(f"Error cargando el archivo: {e}")
        return
    
    try:
        conn = mysql.connector.connect(
            host='localhost',
            user='root',
            password='',
            database='nutriologo'
        )
        cursor = conn.cursor()
        print("Conexión exitosa a la base de datos.")
    except mysql.connector.Error as err:
        print(f"Error al conectarse a la base de datos: {err}")
        return
    
    tablas_columnas = [
        ("Genero", "idGenero"),
        ("Objetivo", "idObjetivo"),
        ("IdRegimen", "idRegimen"),
        ("NombreRegimen", "idNombreRegimen"),
        ("CostoRegimen", "idCostoRegimen"),
        ("RangoCosto", "idRangoCosto"),
        ("PorcionesDesayuno", "idPorcionesDesayuno"),
        ("PorcionesAlmuerzo", "idPorcionesAlmuerzo"),
        ("PorcionesCena", "idPorcionesCena"),
        ("PorcionesColacion1", "idPorcionesColacion1"),
        ("PorcionesColacion2", "idPorcionesColacion2"),
        ("IngestaRealDesayuno", "idIngestaRealDesayuno"),
        ("IngestaRealAlmuerzo", "idIngestaRealAlmuerzo"),
        ("IngestaRealCena", "idIngestaRealCena"),
        ("IngestaRealColacion1", "idIngestaRealColacion1"),
        ("IngestaRealColacion2", "idIngestaRealColacion2"),
        ("SatisfaccionPaciente", "idSatisfaccionPaciente"),
        ("EstadoPaciente", "idEstadoPaciente"),
        ("CitasAgendadas", "idCitasAgendadas"),
        ("CitasAsistidas", "idCitasAsistidas")
    ]
    
    for tabla, columna_id in tablas_columnas:
        print(f"Procesando tabla: {tabla}")
        query = f"SELECT id, {tabla} FROM {tabla}"
        cursor.execute(query)
        resultados_tabla = cursor.fetchall()
        mapa_tabla = {fila[1]: fila[0] for fila in resultados_tabla}
        
        for idx, row in df.iterrows():
            valor_csv = row[tabla]
            if valor_csv in mapa_tabla:
                id_tabla = mapa_tabla[valor_csv]
                try:
                    update_query = f"UPDATE paciente SET {columna_id} = %s WHERE IdPaciente = %s"
                    cursor.execute(update_query, (id_tabla, row['IdPaciente']))
                except Exception as e:
                    print(f"Error actualizando fila {idx}: {e}")
    
    conn.commit()
    cursor.close()
    conn.close()
    print("Datos actualizados correctamente en la tabla paciente.")
    input("Finalizar...")

def generar_cubos_olap():
    # Conexión a la base de datos MySQL (usuario 'root' sin contraseña)
    engine = create_engine('mysql+pymysql://root:@localhost/nutriologo')
    
    # Verificación de la conexión
    try:
        with engine.connect() as connection:
            connection.execute(text("SELECT 1"))  # Usar `text` para ejecutar la consulta
            print("Conexión exitosa a la base de datos")
    except Exception as e:
        print(f"Error de conexión: {e}")
        return
    
    # Consulta para obtener los datos para el primer cubo OLAP
    query_1 = """
    SELECT 
        nr.NombreRegimen,
        cr.CostoRegimen,
        COUNT(p.idPaciente) AS CantidadPacientes,
        AVG(sp.SatisfaccionPaciente) AS SatisfaccionPromedio
    FROM paciente p
    JOIN NombreRegimen nr ON p.idNombreRegimen = nr.id
    JOIN CostoRegimen cr ON p.idCostoRegimen = cr.id
    JOIN SatisfaccionPaciente sp ON p.idSatisfaccionPaciente = sp.id
    GROUP BY nr.NombreRegimen, cr.CostoRegimen
    """
    df_cubo1 = pd.read_sql(query_1, engine)
    
    # Consulta para obtener los datos para el segundo cubo OLAP
    query_2 = """
    SELECT 
        nr.NombreRegimen,
        COUNT(p.idPaciente) AS CantidadPacientes,
        SUM(
            CASE 
                WHEN pd.PorcionesDesayuno = ir.IngestaRealDesayuno
                AND pa.PorcionesAlmuerzo = ir2.IngestaRealAlmuerzo
                AND pc.PorcionesCena = ir3.IngestaRealCena
                AND pcol1.PorcionesColacion1 = ir4.IngestaRealColacion1
                AND pcol2.PorcionesColacion2 = ir5.IngestaRealColacion2
                THEN 1 
                ELSE 0 
            END
        ) AS PacientesCumplenRegimen
    FROM paciente p
    JOIN NombreRegimen nr ON p.idNombreRegimen = nr.id
    LEFT JOIN PorcionesDesayuno pd ON p.idPorcionesDesayuno = pd.id
    LEFT JOIN PorcionesAlmuerzo pa ON p.idPorcionesAlmuerzo = pa.id
    LEFT JOIN PorcionesCena pc ON p.idPorcionesCena = pc.id
    LEFT JOIN PorcionesColacion1 pcol1 ON p.idPorcionesColacion1 = pcol1.id
    LEFT JOIN PorcionesColacion2 pcol2 ON p.idPorcionesColacion2 = pcol2.id
    LEFT JOIN IngestaRealDesayuno ir ON p.idIngestaRealDesayuno = ir.id
    LEFT JOIN IngestaRealAlmuerzo ir2 ON p.idIngestaRealAlmuerzo = ir2.id
    LEFT JOIN IngestaRealCena ir3 ON p.idIngestaRealCena = ir3.id
    LEFT JOIN IngestaRealColacion1 ir4 ON p.idIngestaRealColacion1 = ir4.id
    LEFT JOIN IngestaRealColacion2 ir5 ON p.idIngestaRealColacion2 = ir5.id
    GROUP BY nr.NombreRegimen
    """
    df_cubo2 = pd.read_sql(query_2, engine)
    
    # Crear cubos OLAP 1 y 2
    cubo1_olap = df_cubo1.pivot_table(
        index='NombreRegimen', 
        values=['CostoRegimen', 'CantidadPacientes', 'SatisfaccionPromedio'], 
        aggfunc={'CostoRegimen': 'first', 'CantidadPacientes': 'sum', 'SatisfaccionPromedio': 'mean'}
    )
    
    cubo2_olap = df_cubo2.pivot_table(
        index='NombreRegimen',
        values=['CantidadPacientes', 'PacientesCumplenRegimen'],
        aggfunc={'CantidadPacientes': 'sum', 'PacientesCumplenRegimen': 'sum'}
    )
    
    # Guardar los cubos OLAP en la base de datos
    try:
        cubo1_olap.reset_index().to_sql('cubo_olap_1', con=engine, if_exists='replace', index=False)
        print("Cubo OLAP 1 guardado exitosamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar el Cubo OLAP 1: {e}")
    
    try:
        cubo2_olap.reset_index().to_sql('cubo_olap_2', con=engine, if_exists='replace', index=False)
        print("Cubo OLAP 2 guardado exitosamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar el Cubo OLAP 2: {e}")
    
    # Cargar las tablas
    paciente_df = pd.read_sql("SELECT * FROM paciente", engine)
    satisfaccion_df = pd.read_sql("SELECT * FROM satisfaccionpaciente", engine)
    regimen_df = pd.read_sql("SELECT * FROM nombreregimen", engine)
    citas_agendadas_df = pd.read_sql("SELECT * FROM citasagendadas", engine)
    citas_asistidas_df = pd.read_sql("SELECT * FROM citasasistidas", engine)

    # Unir las tablas con sufijos para evitar duplicados
    df = paciente_df.merge(satisfaccion_df, left_on='idSatisfaccionPaciente', right_on='id', 
                        how='left', suffixes=('', '_satisfaccion')) \
                    .merge(regimen_df, left_on='idNombreRegimen', right_on='id', 
                        how='left', suffixes=('', '_regimen')) \
                    .merge(citas_agendadas_df, left_on='idCitasAgendadas', right_on='id', 
                        how='left', suffixes=('', '_citasagendadas')) \
                    .merge(citas_asistidas_df, left_on='idCitasAsistidas', right_on='id', 
                        how='left', suffixes=('', '_citasasistidas'))

    # Calcular cumplimiento de citas
    df['CumplimientoCitas'] = (df['CitasAsistidas'] / df['CitasAgendadas']) * 100

    # Dimensiones y métricas
    cubo = df.groupby(['NombreRegimen', 'SatisfaccionPaciente']).agg({
        'CumplimientoCitas': 'mean',
        'idPaciente': 'count'  # Conteo de pacientes
    }).rename(columns={'idPaciente': 'NumeroPacientes'}).reset_index()

    # Guardar el cubo como nueva tabla en la base de datos
    tabla_nombre = "cubo_olap"
    with engine.connect() as connection:
        cubo.to_sql(tabla_nombre, connection, if_exists='replace', index=False)
        print(f"La tabla '{tabla_nombre}' se ha creado correctamente en la base de datos.")

    
    # Cargar tablas para análisis de regimen, género y edad
    paciente_df = pd.read_sql("SELECT * FROM paciente", engine)
    regimen_df = pd.read_sql("SELECT * FROM nombreregimen", engine)
    genero_df = pd.read_sql("SELECT * FROM genero", engine)

    df = paciente_df.merge(regimen_df, left_on='idNombreRegimen', right_on='id', 
                           how='left', suffixes=('', '_regimen')) \
                    .merge(genero_df, left_on='idGenero', right_on='id', 
                           how='left', suffixes=('', '_genero'))

    # Crear rangos de edad
    bins = [0, 18, 30, 45, 60, 100]  # Rango de edades
    labels = ['0-18', '19-30', '31-45', '46-60', '60+']
    df['RangoEdad'] = pd.cut(df['Edad'], bins=bins, labels=labels, right=False)

    # Generar cubo por régimen, género y edad
    cubo_genero_edad = df.groupby(['NombreRegimen', 'Genero', 'RangoEdad']).agg({
        'idPaciente': 'count'  # Conteo de pacientes
    }).rename(columns={'idPaciente': 'NumeroPacientes'}).reset_index()

    try:
        cubo_genero_edad.to_sql('cubo_regimen_genero_edad', engine, if_exists='replace', index=False)
        print("Cubo Regimen, Genero, Edad guardado exitosamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar el cubo Regimen, Genero, Edad: {e}")

    # Cargar tablas para citas y generar cubo por mes y régimen
    citas_agendadas_df = pd.read_sql("SELECT * FROM citasagendadas", engine)
    citas_asistidas_df = pd.read_sql("SELECT * FROM citasasistidas", engine)

    df = paciente_df.merge(regimen_df, left_on='idNombreRegimen', right_on='id', 
                           how='left', suffixes=('', '_regimen')) \
                    .merge(citas_agendadas_df, left_on='idCitasAgendadas', right_on='id', 
                           how='left', suffixes=('', '_citasagendadas')) \
                    .merge(citas_asistidas_df, left_on='idCitasAsistidas', right_on='id', 
                           how='left', suffixes=('', '_citasasistidas'))

    # Asegurar que 'FechaInicioRegimen' esté en formato datetime
    df['FechaInicioRegimen'] = pd.to_datetime(df['FechaInicioRegimen'])

    # Agregar columna de mes
    df['Mes'] = df['FechaInicioRegimen'].dt.to_period('M').astype(str)

    # Calcular cumplimiento de citas
    df['CumplimientoCitas'] = (df['CitasAsistidas'] / df['CitasAgendadas']) * 100

    # Agrupar por mes y régimen
    cubo_mes_regimen = df.groupby(['Mes', 'NombreRegimen']).agg({
        'CumplimientoCitas': 'mean',  # Promedio del cumplimiento de citas
        'idPaciente': 'count'         # Conteo de pacientes
    }).rename(columns={'idPaciente': 'NumeroPacientes'}).reset_index()

    try:
        cubo_mes_regimen.to_sql('cubo_mes_regimen', engine, if_exists='replace', index=False)
        print("Cubo Mes Regimen guardado exitosamente en la base de datos.")
    except Exception as e:
        print(f"Error al guardar el cubo Mes Regimen: {e}")

def mostrar_menu():
    print("Menú de opciones:")
    print("1. Importar Script de BD")
    print("2. Generar registros")
    print("3. Limpiar CSV")
    print("4. Insertar datos en las tablas de dimensiones")
    print("5. Insertar datos a la tabla de hechos")
    print("6. Generar cubos OLAP")
    opcion = int(input("Selecciona una opción: "))
    
    if opcion == 1:
        importar_script_bd('modeloNutriologo.sql', 'modeloNutriologo_limpio.sql')
    if opcion == 2:
        generar_registros_csv('RegistrosNutriologo.csv',2000)
    if opcion == 3:
        preparar_archivo_csv('RegistrosNutriologo.csv')
    if opcion == 4:
        insertar_datos_dimensiones('RegistrosNutriologo_limpio.csv')
    if opcion == 5:
        insertar_datos_hechos('RegistrosNutriologo_limpio.csv')
        insertar_dimensiones('RegistrosNutriologo_limpio.csv')
    if opcion == 6:
        print("Generando cubos...")
        generar_cubos_olap()

mostrar_menu()
