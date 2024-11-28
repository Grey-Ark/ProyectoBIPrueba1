import pandas as pd
from sqlalchemy import create_engine

# Conexión a la base de datos (sin contraseña)
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

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
