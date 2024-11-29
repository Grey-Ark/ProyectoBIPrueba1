import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar la tabla cubo_regimen_genero_edad
cubo_regimen_genero_edad = pd.read_sql("SELECT * FROM cubo_regimen_genero_edad", engine)

# Agrupar los datos por 'NombreRegimen' y 'Genero', y sumar 'NumeroPacientes' para cada combinación
regimen_genero_data = cubo_regimen_genero_edad.groupby(["NombreRegimen", "Genero"])['NumeroPacientes'].sum().reset_index()

# Crear la app de Dash
app = Dash(__name__)

# Layout del Dashboard
app.layout = html.Div([
    html.H2("Tipo de Régimen, Género y Número de Pacientes que se Apegan", style={'textAlign': 'center', 'color': '#2c3e50'}),
    
    # Gráfico de barras
    dcc.Graph(
        id='regimen-genero-bar-chart',
        figure=px.bar(
            regimen_genero_data,
            x='NombreRegimen',
            y='NumeroPacientes',
            color='Genero',  # Color según género
            title="Número de Pacientes por Tipo de Régimen y Género",
            labels={'NombreRegimen': 'Tipo de Régimen', 'NumeroPacientes': 'Número de Pacientes', 'Genero': 'Género'},
            color_discrete_map={'M': 'blue', 'F': 'pink'},  # Mapear colores para los géneros
        ).update_layout(title_x=0.5)
    ),
])

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)
