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

# Layout mejorado con mayor margen, centrado y tipografía refinada
app.layout = html.Div([
    html.Div(style={
        'width': '100%', 
        'height': '35px', 
        'background-color': '#0077b6', 
        'position': 'fixed', 
        'top': '0', 
        'left': '0', 
        'z-index': '1000'
    }),
    # Balanced Scorecard (BSC)
    html.Div([
        html.H1("Balanced Scorecard - Sistema de Gestión Nutricional", 
                style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50',
                       'margin-bottom': '20px'}),
        html.H3("Perspectivas Estratégicas", 
                style={'textAlign': 'center', 'margin-top': '20px', 'color': '#34495e'}),
        html.Div([
            # Perspectivas originales
            html.Div([
                html.H4("Perspectiva Financiera", 
                        style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
                html.Ul([
                    html.Li("Optimizar el costo de los regímenes alimenticios, manteniendo la eficiencia en el servicio para los pacientes. Meta: Mantener los costos dentro de los rangos establecidos ($300 - $750 MXN semanales), con una desviación estándar $100."),
                    html.Li("Incrementar los ingresos netos por consultas y servicios de seguimiento, manteniendo un crecimiento sostenible en la cantidad de pacientes atendidos. Meta: Incrementar la cantidad de pacientes en un 10% mensual."),
                    html.Li("Asegurar que las promociones y ajustes en el costo de los servicios mantengan la rentabilidad para el sistema sin comprometer la calidad de atención. Meta: Controlar el costo de las consultas y servicios dentro de un rango económico y accesible."),
                ], style={'color': '#34495e'}),
            ], style={'flex': '1', 'padding': '20px', 'border': '1px solid #ecf0f1', 'border-radius': '5px',
                    'background-color': '#f9f9f9', 'margin': '10px'}),

            html.Div([
                html.H4("Perspectiva del Cliente", 
                        style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
                html.Ul([
                    html.Li("Aumentar la retención de pacientes mediante la personalización de los regímenes alimenticios, permitiendo cambios dentro de un mismo grupo alimenticio sin perder la equivalencia nutricional. Meta: Mantener una retención de pacientes mayor a 95%."),
                    html.Li("Mejorar la satisfacción del paciente con el sistema de seguimiento mediante la herramienta móvil y consultas periódicas. Meta: Obtener una calificación de satisfacción mayor a 4.5 de calificacion de un total de 5, en encuestas de pacientes."),
                    html.Li("Proveer un servicio de calidad que garantice que los pacientes se sientan apoyados en su proceso de cambio de hábitos alimenticios, con resultados tangibles en su salud y bienestar."),
                ], style={'color': '#34495e'}),
            ], style={'flex': '1', 'padding': '20px', 'border': '1px solid #ecf0f1', 'border-radius': '5px',
                    'background-color': '#f9f9f9', 'margin': '10px'}),
               
            html.Div([
                html.H4("Procesos Internos", 
                        style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
                html.Ul([
                    html.Li("Optimizar el proceso de personalización de regímenes alimenticios de acuerdo a los criterios del sistema mexicano de alimentos equivalentes, permitiendo ajustes flexibles pero controlados para cada paciente."),
                    html.Li("Monitorear el seguimiento de los pacientes a sus regímenes alimenticios mediante el uso efectivo de la herramienta móvil y la generación de reportes automáticos para los nutriólogos. Meta: Asegurar un seguimiento mayor al 90%."),
                    html.Li("Automatizar la gestión de cambios en los regímenes alimenticios para facilitar la toma de decisiones rápidas, asegurando que los pacientes reciban el régimen adecuado a tiempo."),
                ], style={'color': '#34495e'}),
            ], style={'flex': '1', 'padding': '20px', 'border': '1px solid #ecf0f1', 'border-radius': '5px',
                    'background-color': '#f9f9f9', 'margin': '10px'}),

            html.Div([
                html.H4("Aprendizaje y Crecimiento", 
                        style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
                html.Ul([
                    html.Li("Incrementar la adopción y uso efectivo de la herramienta móvil para el seguimiento nutricional, tanto por pacientes como por nutriólogos, asegurando que un mayor numero de los pacientes utilicen la aplicación de manera constante."),
                    html.Li("Mejorar las capacidades predictivas del sistema para anticipar resultados de los regímenes alimenticios, utilizando inteligencia de negocios para generar recomendaciones más precisas y personalizadas. Meta: Aumentar la precisión de las predicciones mayor a 85%."),
                    html.Li("Fomentar la capacitación continua del personal en el uso de las herramientas tecnológicas y la aplicación de la inteligencia de negocios en la toma de decisiones estratégicas."),
                ], style={'color': '#34495e'}),
            ], style={'flex': '1', 'padding': '20px', 'border': '1px solid #ecf0f1', 'border-radius': '5px',
                    'background-color': '#f9f9f9', 'margin': '10px'}),

        ], style={'display': 'flex', 'gap': '20px', 'margin-top': '20px', 'justify-content': 'center'}),
        
        
        # Nueva sección: Desarrollo del BSC
        html.Div([
            html.H3("Desarrollo y Proceso de Construcción del Balanced Scorecard", 
                    style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'margin-top': '40px',
                           'color': '#2c3e50'}),
            html.P("""
                El Balanced Scorecard fue desarrollado siguiendo una metodología sistemática que incluye:
                la identificación de objetivos estratégicos clave, la definición de indicadores de desempeño, 
                y el establecimiento de metas específicas para cada perspectiva. Se pensaron y plantearon
                propuestas para garantizar que las metas financieras, de cliente, de procesos internos 
                y de aprendizaje estuvieran alineadas con los valores y objetivos.
                 """, style={'textAlign': 'justify', 'font-family': 'Roboto, Arial, sans-serif', 'line-height': '1.6',
                        'color': '#34495e', 'padding': '20px'}),                                
                ], style={'padding': '20px', 'margin-top': '20px', 'border-radius': '10px', 
                        'background-color': '#f9f9f9', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),

        # Información sobre el diseño de la base de datos y cubos OLAP
        html.Div([
            html.H4("Diseño de Base de Datos y Cubos OLAP para Análisis de Datos", 
                    style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'margin-top': '40px',
                        'color': '#2c3e50'}),
            html.P("""
                El diseño de la base de datos fue creado con el fin de recopilar y gestionar la información 
                relevante para el seguimiento de los pacientes en su régimen alimenticio. Los campos claves 
                incluyen datos del paciente, detalles del régimen alimenticio, seguimiento de la ingesta, 
                y la satisfacción del paciente, entre otros. La base de datos permite un análisis profundo 
                sobre el comportamiento de los pacientes en relación con su régimen alimenticio.
            """, style={'textAlign': 'justify', 'font-family': 'Roboto, Arial, sans-serif', 'line-height': '1.6',
                        'color': '#34495e', 'padding': '20px'}),

            html.P("""
                Para mejorar la gestión y la toma de decisiones, se crearon cubos OLAP que permiten responder 
                preguntas clave sobre el rendimiento del sistema. Algunas de las preguntas más relevantes incluyen:
            """, style={'textAlign': 'justify', 'font-family': 'Roboto, Arial, sans-serif', 'line-height': '1.6',
                        'color': '#34495e', 'padding': '20px'}),

            html.Ul([
                html.Li("¿En qué fecha se registraron más pacientes para el régimen más aceptado?"),
                html.Li("¿Qué tipo de régimen tienen más pacientes y cuántos se apegan a él?"),
                html.Li("¿Cuántos pacientes cumplieron con sus citas y se beneficiaron de la promoción en tal mes?"),
                html.Li("¿Cuál es el mes con mayor potencial para una promoción efectiva? (Ej. Julio, mes con mayor número de registros)"),
            ], style={'color': '#34495e', 'padding-left': '20px'}),

            html.P("""
                Estos cubos OLAP permiten realizar un análisis multidimensional de los datos y ofrecer 
                información valiosa para la toma de decisiones, como la predicción de regímenes exitosos, 
                el ajuste de precios y la optimización de las promociones.
            """, style={'textAlign': 'justify', 'font-family': 'Roboto, Arial, sans-serif', 'line-height': '1.6',
                        'color': '#34495e', 'padding': '20px'}),

        ], style={'padding': '20px', 'margin-top': '20px', 'border-radius': '10px', 
                'background-color': '#f9f9f9', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),     
    ], style={'padding': '40px', 'margin': '40px auto', 'max-width': '1200px',
              'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'background-color': '#ffffff'}),                
    
    # Dashboards
    html.H1("Dashboard Nutriológico", 
            style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'margin-bottom': '20px',
                   'color': '#2c3e50'}),
    html.Div([
        # Dashboard superior
        html.Div([
            html.H2("Análisis de Regímenes Nutricionales", 
                    style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
            dcc.Dropdown(
                id='metricas-dropdown',
                options=[{'label': col, 'value': col} for col in ["CostoRegimen", "CantidadPacientes", "SatisfaccionPromedio"]],
                value='CantidadPacientes',
                placeholder="Seleccione una métrica",
                style={'width': '50%', 'margin': '0 auto', 'font-family': 'Roboto, Arial, sans-serif'}
            ),
            dcc.Graph(id='grafico-metricas')
        ], style={'padding': '20px', 'margin-bottom': '40px', 'border-radius': '10px', 
                  'box-shadow': '0 4px 8px rgba(0,0,0,0.1)', 'background-color': '#ffffff'}),
        
        # Dashboard inferior: Dos gráficos lado a lado
        html.Div([
            html.Div([
                html.H2("Relación entre Pacientes y Cumplimiento Relativo", style={'textAlign': 'center', 'color': '#2c3e50'}),
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
            ], style={'flex': '1', 'padding': '20px', 'margin-right': '20px', 
                      'background-color': '#ffffff', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),
            html.Div([
                html.H2("Inscripción por Régimen y Mes", style={'textAlign': 'center', 'color': '#2c3e50'}),
                dcc.Dropdown(
                    id='mes-dropdown',
                    options=[{'label': mes, 'value': mes} for mes in cubo_mes_regimen['MesNombre'].unique()],
                    value=cubo_mes_regimen['MesNombre'].iloc[0],
                    style={'width': '50%', 'margin': '0 auto'}
                ),
                dcc.Graph(id='regimen-pie-chart')
            ], style={'flex': '1', 'padding': '20px', 
                      'background-color': '#ffffff', 'border-radius': '10px', 'box-shadow': '0 4px 8px rgba(0,0,0,0.1)'}),
        ], style={'display': 'flex', 'gap': '20px'}),
    ], style={'max-width': '1200px', 'margin': '0 auto'}),
])


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
