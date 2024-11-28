import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar las tablas necesarias
paciente_df = pd.read_sql("SELECT * FROM paciente", engine)
regimen_df = pd.read_sql("SELECT * FROM nombreregimen", engine)
citas_agendadas_df = pd.read_sql("SELECT * FROM citasagendadas", engine)
citas_asistidas_df = pd.read_sql("SELECT * FROM citasasistidas", engine)

# Unir las tablas con sufijos para evitar duplicados
df = paciente_df.merge(regimen_df, left_on='idNombreRegimen', right_on='id', 
                       how='left', suffixes=('', '_regimen')) \
                .merge(citas_agendadas_df, left_on='idCitasAgendadas', right_on='id', 
                       how='left', suffixes=('', '_citasagendadas')) \
                .merge(citas_asistidas_df, left_on='idCitasAsistidas', right_on='id', 
                       how='left', suffixes=('', '_citasasistidas'))

# Asegurar que 'FechaInicioRegimen' esté en formato datetime
df['FechaInicioRegimen'] = pd.to_datetime(df['FechaInicioRegimen'])

# Agregar una columna para agrupar por mes
df['Mes'] = df['FechaInicioRegimen'].dt.to_period('M').astype(str)

# Calcular cumplimiento de citas
df['CumplimientoCitas'] = (df['CitasAsistidas'] / df['CitasAgendadas']) * 100

# Agrupar por mes y régimen, calculando las métricas
cubo_mes_regimen = df.groupby(['Mes', 'NombreRegimen']).agg({
    'CumplimientoCitas': 'mean',  # Promedio del cumplimiento de citas
    'idPaciente': 'count'         # Conteo de pacientes
}).rename(columns={'idPaciente': 'NumeroPacientes'}).reset_index()

# Guardar el cubo como nueva tabla en la base de datos
tabla_nombre = "cubo_mes_regimen"
with engine.connect() as connection:
    cubo_mes_regimen.to_sql(tabla_nombre, connection, if_exists='replace', index=False)
    print(f"La tabla '{tabla_nombre}' se ha creado correctamente en la base de datos.")
