import pandas as pd
from sqlalchemy import create_engine

# 1. Conexión a la base de datos MySQL (usuario 'root' sin contraseña)
engine = create_engine('mysql+mysqlconnector://root:@localhost/nutriologo')

# 2. Verificación de conexión
try:
    with engine.connect() as connection:
        result = connection.execute("SELECT 1")  # Comprobación simple
        print("Conexión exitosa a la base de datos")
except Exception as e:
    print(f"Error de conexión: {e}")

# 3. Consulta para obtener los datos para el primer cubo OLAP
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

# Cargar los datos en un DataFrame
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

# Cargar los datos en un DataFrame
df_cubo2 = pd.read_sql(query_2, engine)

# Mostrar los primeros registros de cada cubo (opcional)
print("Cubo 1:")
print(df_cubo1.head())

print("\nCubo 2:")
print(df_cubo2.head())

# 5. Creación del cubo OLAP 1
cubo1_olap = df_cubo1.pivot_table(
    index='NombreRegimen', 
    values=['CostoRegimen', 'CantidadPacientes', 'SatisfaccionPromedio'], 
    aggfunc={'CostoRegimen': 'first', 'CantidadPacientes': 'sum', 'SatisfaccionPromedio': 'mean'}
)

print("\nCubo OLAP 1:")
print(cubo1_olap)

# 6. Creación del cubo OLAP 2
cubo2_olap = df_cubo2.pivot_table(
    index='NombreRegimen',
    values=['CantidadPacientes', 'PacientesCumplenRegimen'],
    aggfunc={'CantidadPacientes': 'sum', 'PacientesCumplenRegimen': 'sum'}
)

print("\nCubo OLAP 2:")
print(cubo2_olap)

# Guardar el cubo OLAP 1 en la base de datos
try:
    cubo1_olap.reset_index().to_sql('cubo_olap_1', con=engine, if_exists='replace', index=False)
    print("Cubo OLAP 1 guardado exitosamente en la base de datos.")
except Exception as e:
    print(f"Error al guardar el Cubo OLAP 1: {e}")

# Guardar el cubo OLAP 2 en la base de datos
try:
    cubo2_olap.reset_index().to_sql('cubo_olap_2', con=engine, if_exists='replace', index=False)
    print("Cubo OLAP 2 guardado exitosamente en la base de datos.")
except Exception as e:
    print(f"Error al guardar el Cubo OLAP 2: {e}")