import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos (sin contraseña)
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar las tablas necesarias
paciente_df = pd.read_sql("SELECT * FROM paciente", engine)
regimen_df = pd.read_sql("SELECT * FROM nombreregimen", engine)
genero_df = pd.read_sql("SELECT * FROM genero", engine)

# Unir las tablas con sufijos para evitar duplicados
df = paciente_df.merge(regimen_df, left_on='idNombreRegimen', right_on='id', 
                       how='left', suffixes=('', '_regimen')) \
                .merge(genero_df, left_on='idGenero', right_on='id', 
                       how='left', suffixes=('', '_genero'))

# Crear rangos de edad
bins = [0, 18, 30, 45, 60, 100]  # Rango de edades
labels = ['0-18', '19-30', '31-45', '46-60', '60+']
df['RangoEdad'] = pd.cut(df['Edad'], bins=bins, labels=labels, right=False)

# Dimensiones y métricas
cubo = df.groupby(['NombreRegimen', 'Genero', 'RangoEdad']).agg({
    'idPaciente': 'count'  # Conteo de pacientes
}).rename(columns={'idPaciente': 'NumeroPacientes'}).reset_index()

# Guardar el cubo como nueva tabla en la base de datos
tabla_nombre = "cubo_regimen_genero_edad"
with engine.connect() as connection:
    cubo.to_sql(tabla_nombre, connection, if_exists='replace', index=False)
    print(f"La tabla '{tabla_nombre}' se ha creado correctamente en la base de datos.")
