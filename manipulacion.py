import pandas as pd
import numpy as np
import mysql.connector
import re
from datetime import datetime
import unicodedata

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



def mostrar_menu():
    print("Menú de opciones:")
    print("1. Importar Script de BD")
    print("2. Limpiar CSV")
    print("3. Insertar datos en las tablas de dimensiones")
    print("4. Insertar datos a la tabla de hechos")
    opcion = int(input("Selecciona una opción: "))
    
    if opcion == 1:
        importar_script_bd('C:/Users/juane/Documents/SeptimoSemestre/InteligenciaNegocios/ProyectoNutriologo/modeloNutriologo.sql', 'C:/Users/juane/Documents/SeptimoSemestre/InteligenciaNegocios/ProyectoNutriologo/modeloNutriologo_limpio.sql')
    if opcion == 2:
        preparar_archivo_csv('C:/Users/juane/Documents/SeptimoSemestre/InteligenciaNegocios/ProyectoNutriologo/RegistrosNutriologo.csv')
    if opcion == 3:
        insertar_datos_dimensiones('C:/Users/juane/Documents/SeptimoSemestre/InteligenciaNegocios/ProyectoNutriologo/RegistrosNutriologo_limpio.csv')
    if opcion == 4:
        insertar_datos_hechos('C:/Users/juane/Documents/SeptimoSemestre/InteligenciaNegocios/ProyectoNutriologo/RegistrosNutriologo_limpio.csv')
        insertar_dimensiones('C:/Users/juane/Documents/SeptimoSemestre/InteligenciaNegocios/ProyectoNutriologo/RegistrosNutriologo_limpio.csv')


mostrar_menu()
