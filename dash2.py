import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px
from dash import Dash, dcc, html

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar las tablas desde la base de datos
cubo_olap = pd.read_sql("SELECT * FROM cubo_olap", engine)
cubo_regimen_genero_edad = pd.read_sql("SELECT * FROM cubo_regimen_genero_edad", engine)

# Normalizar el número de pacientes entre ambas tablas
# Agrupar por NombreRegimen para sumar pacientes de todas las edades y géneros
pacientes_por_regimen = cubo_regimen_genero_edad.groupby("NombreRegimen").agg({
    "NumeroPacientes": "sum"
}).reset_index()

# Unir con cubo_olap para obtener cumplimiento
merged_df = cubo_olap.merge(pacientes_por_regimen, on="NombreRegimen", suffixes=("_olap", "_genero"))

# Calcular porcentaje de cumplimiento relativo (CumplimientoCitas ponderado por NúmeroPacientes)
merged_df["CumplimientoRelativo"] = merged_df["CumplimientoCitas"] * merged_df["NumeroPacientes_olap"] / merged_df["NumeroPacientes_genero"]

# Crear el gráfico de dispersión usando Plotly Express
fig = px.scatter(
    merged_df,
    x="NumeroPacientes_olap",
    y="CumplimientoRelativo",
    color="NombreRegimen",
    size="CumplimientoRelativo",
    title="Relación entre Número de Pacientes y Cumplimiento Relativo",
    labels={"NumeroPacientes_olap": "Número de Pacientes", "CumplimientoRelativo": "Cumplimiento Relativo (%)"}
)

# Crear la aplicación Dash
app = Dash(__name__)

# Definir el layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard: Análisis de Cumplimiento Relativo"),
    dcc.Graph(figure=fig)  # Insertar el gráfico en el layout
])

# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
