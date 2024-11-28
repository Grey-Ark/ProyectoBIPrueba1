import pandas as pd
from sqlalchemy import create_engine
import dash
from dash import dcc, html
from dash.dependencies import Input, Output
import plotly.express as px

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar las tablas
cubo_mes_regimen = pd.read_sql("SELECT Mes, NombreRegimen, CumplimientoCitas, NumeroPacientes FROM cubo_mes_regimen", engine)

# Preparar los datos
cubo_mes_regimen['Mes'] = pd.to_datetime(cubo_mes_regimen['Mes'], format='%Y-%m')
cubo_mes_regimen['MesNombre'] = cubo_mes_regimen['Mes'].dt.strftime('%B')
cubo_mes_regimen = cubo_mes_regimen.sort_values('Mes')

# Crear la aplicación Dash
app = dash.Dash(__name__)

# Layout de la aplicación
app.layout = html.Div([
    html.H1("Dashboard: Inscripción por Régimen y Mes", style={'textAlign': 'center'}),
    
    # Dropdown para seleccionar el mes
    html.Div([
        html.Label("Selecciona un Mes:"),
        dcc.Dropdown(
            id='mes-dropdown',
            options=[{'label': mes, 'value': mes} for mes in cubo_mes_regimen['MesNombre'].unique()],
            value=cubo_mes_regimen['MesNombre'].iloc[0],
            style={'width': '50%'}
        )
    ], style={'textAlign': 'center', 'marginBottom': '20px'}),
    
    # Gráfico interactivo
    dcc.Graph(id='regimen-pie-chart')
])

# Callback para actualizar el gráfico basado en el mes seleccionado
@app.callback(
    Output('regimen-pie-chart', 'figure'),
    [Input('mes-dropdown', 'value')]
)
def update_pie_chart(selected_month):
    # Filtrar los datos para el mes seleccionado
    filtered_df = cubo_mes_regimen[cubo_mes_regimen['MesNombre'] == selected_month]
    
    # Crear gráfico de pastel
    fig = px.pie(
        filtered_df,
        values='NumeroPacientes',
        names='NombreRegimen',
        title=f"Distribución de Inscripciones en {selected_month}",
        color_discrete_sequence=px.colors.sequential.Viridis
    )
    fig.update_traces(textinfo='percent+label')  # Mostrar porcentaje y etiqueta
    return fig

# Ejecutar la aplicación
if __name__ == '__main__':
    app.run_server(debug=True)
