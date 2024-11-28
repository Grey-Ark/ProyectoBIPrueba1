import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar los datos
df_cubo1 = pd.read_sql("SELECT * FROM cubo_olap_1", engine)
cubo_olap = pd.read_sql("SELECT * FROM cubo_olap", engine)
cubo_regimen_genero_edad = pd.read_sql("SELECT * FROM cubo_regimen_genero_edad", engine)
cubo_mes_regimen = pd.read_sql("SELECT Mes, NombreRegimen, CumplimientoCitas, NumeroPacientes FROM cubo_mes_regimen", engine)

# Preparar datos adicionales
pacientes_por_regimen = cubo_regimen_genero_edad.groupby("NombreRegimen").agg({
    "NumeroPacientes": "sum"
}).reset_index()

merged_df = cubo_olap.merge(pacientes_por_regimen, on="NombreRegimen", suffixes=("_olap", "_genero"))
merged_df["CumplimientoRelativo"] = merged_df["CumplimientoCitas"] * merged_df["NumeroPacientes_olap"] / merged_df["NumeroPacientes_genero"]

cubo_mes_regimen['Mes'] = pd.to_datetime(cubo_mes_regimen['Mes'], format='%Y-%m')
cubo_mes_regimen['MesNombre'] = cubo_mes_regimen['Mes'].dt.strftime('%B')
cubo_mes_regimen = cubo_mes_regimen.sort_values('Mes')

# Inicializar la app Dash
app = Dash(__name__)

# Layout unificado
app.layout = html.Div([
    # Balanced Scorecard (BSC)
    html.Div([
        html.H1("Balanced Scorecard - Sistema de Gestión Nutricional", style={'textAlign': 'center', 'font-family': 'Candara'}),
        html.H3("Perspectivas Estratégicas", style={'textAlign': 'center', 'margin-top': '20px'}),
        html.Div([
            html.Div([
                html.H4("Perspectiva Financiera", style={'textAlign': 'center', 'font-family': 'Candara'}),
                html.Ul([
                    html.Li("Incrementar ingresos netos por servicios: Meta = $400 MXN/paciente"),
                    html.Li("Mantener el costo de regímenes en rangos adecuados: Meta = ≤ $100 MXN"),
                ]),
            ], style={'flex': '1', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
            html.Div([
                html.H4("Perspectiva del Cliente", style={'textAlign': 'center', 'font-family': 'Candara'}),
                html.Ul([
                    html.Li("Incrementar retención de pacientes: Meta = 95%"),
                    html.Li("Crecer en el número de pacientes: Meta = 10%"),
                    html.Li("Mejorar la satisfacción del paciente: Meta ≥ 4.5"),
                ]),
            ], style={'flex': '1', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
            html.Div([
                html.H4("Procesos Internos", style={'textAlign': 'center', 'font-family': 'Candara'}),
                html.Ul([
                    html.Li("Optimizar la personalización de regímenes: Meta ≤ 10% ajustes"),
                    html.Li("Monitorear adherencia a regímenes: Meta ≥ 90%"),
                ]),
            ], style={'flex': '1', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
            html.Div([
                html.H4("Aprendizaje y Crecimiento", style={'textAlign': 'center', 'font-family': 'Candara'}),
                html.Ul([
                    html.Li("Incrementar adopción de la herramienta: Meta ≥ 90%"),
                    html.Li("Mejorar predicción de resultados: Meta ≥ 85%"),
                ]),
            ], style={'flex': '1', 'padding': '10px', 'border': '1px solid #ddd', 'border-radius': '5px'}),
        ], style={'display': 'flex', 'gap': '20px', 'margin-top': '20px'}),
    ], style={'padding': '20px', 'margin-bottom': '40px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),

    # Dashboards
    html.H1("Dashboard Nutriológico", style={'textAlign': 'center', 'font-family': 'Candara', 'margin-bottom': '20px'}),
    html.Div([
        # Dashboard superior
        html.Div([
            html.H2("Análisis de Regímenes Nutricionales", style={'textAlign': 'center', 'font-family': 'Candara'}),
            dcc.Dropdown(
                id='metricas-dropdown',
                options=[{'label': col, 'value': col} for col in ["CostoRegimen", "CantidadPacientes", "SatisfaccionPromedio"]],
                value='CantidadPacientes',
                placeholder="Seleccione una métrica",
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='grafico-metricas')
        ], style={'padding': '20px', 'margin-bottom': '40px', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),
        
        # Dashboard inferior: Dos gráficos lado a lado
        html.Div([
            html.Div([
                html.H2("Relación entre Pacientes y Cumplimiento Relativo", style={'textAlign': 'center'}),
                dcc.Graph(
                    figure=px.scatter(
                        merged_df,
                        x="NumeroPacientes_olap",
                        y="CumplimientoRelativo",
                        color="NombreRegimen",
                        size="CumplimientoRelativo",
                        labels={"NumeroPacientes_olap": "Número de Pacientes", "CumplimientoRelativo": "Cumplimiento Relativo (%)"},
                        title="Relación entre Número de Pacientes y Cumplimiento Relativo",
                    ).update_layout(title_x=0.5)
                )
            ], style={'flex': '1', 'padding': '20px', 'margin-right': '20px'}),
            html.Div([
                html.H2("Inscripción por Régimen y Mes", style={'textAlign': 'center'}),
                dcc.Dropdown(
                    id='mes-dropdown',
                    options=[{'label': mes, 'value': mes} for mes in cubo_mes_regimen['MesNombre'].unique()],
                    value=cubo_mes_regimen['MesNombre'].iloc[0],
                    style={'width': '50%', 'margin': '0 auto'}
                ),
                dcc.Graph(id='regimen-pie-chart')
            ], style={'flex': '1', 'padding': '20px'}),
        ], style={'display': 'flex', 'gap': '20px'}),
    ])
], style={'max-width': '1200px', 'margin': '0 auto', 'padding': '20px'})

# Callbacks para Dash
@app.callback(
    Output('grafico-metricas', 'figure'),
    [Input('metricas-dropdown', 'value')]
)
def actualizar_grafico(metrica_seleccionada):
    fig = px.bar(
        df_cubo1, x='NombreRegimen', y=metrica_seleccionada,
        title=f'{metrica_seleccionada} por Régimen',
        color='NombreRegimen'
    )
    return fig

@app.callback(
    Output('regimen-pie-chart', 'figure'),
    [Input('mes-dropdown', 'value')]
)
def actualizar_pie_chart(mes):
    df_filtrado = cubo_mes_regimen[cubo_mes_regimen['MesNombre'] == mes]
    fig = px.pie(df_filtrado, names='NombreRegimen', values='NumeroPacientes', title=f"Inscripciones en {mes}")
    return fig

if __name__ == '__main__':
    app.run_server(debug=True)
