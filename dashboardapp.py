import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html
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

# Ajuste en el cálculo de Cumplimiento Relativo
merged_df = cubo_olap.merge(pacientes_por_regimen, on="NombreRegimen", suffixes=("_olap", "_genero"))
merged_df["CumplimientoRelativo"] = (
    merged_df["CumplimientoCitas"] / merged_df["NumeroPacientes_olap"] * 100
)

# Convertir y ordenar fechas
cubo_mes_regimen['Mes'] = pd.to_datetime(cubo_mes_regimen['Mes'], format='%Y-%m')
cubo_mes_regimen['MesNombre'] = cubo_mes_regimen['Mes'].dt.strftime('%B')
cubo_mes_regimen = cubo_mes_regimen.sort_values('Mes')

# Inicializar la app Dash
app = Dash(__name__)

# Layout
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
   
    html.H1("Dashboard Nutriológico", style={'textAlign': 'center'}),

    # Gráfico de Barras en la parte superior
    html.Div([
        html.H2("Análisis de Regímenes Nutricionales", style={'textAlign': 'center'}),
        dcc.Dropdown(
            id='metricas-dropdown',
            options=[{'label': col, 'value': col} for col in ["CostoRegimen", "CantidadPacientes", "SatisfaccionPromedio"]],
            value='CantidadPacientes',
            placeholder="Seleccione una métrica",
            style={'width': '50%', 'margin': '0 auto'}
        ),
        dcc.Graph(id='grafico-metricas')
    ], style={'margin-bottom': '50px'}),

    # Parte inferior: dispersión y pastel
    html.Div([
        # Gráfico de dispersión (izquierda)
        html.Div([
            html.H2("Relación entre Pacientes y Cumplimiento Relativo", style={'textAlign': 'center'}),
            html.Label("Seleccione Género:", style={'fontWeight': 'bold'}),
            dcc.Dropdown(
                id='filtro-genero',
                options=[{'label': genero, 'value': genero} for genero in cubo_regimen_genero_edad['Genero'].unique()],
                value=None,
                placeholder="Todos los géneros",
                style={'width': '80%', 'margin': '0 auto'}
            ),
            html.Label("Seleccione Rango de Edad:", style={'fontWeight': 'bold'}),
            dcc.Checklist(
                id='filtro-rango-edad',
                options=[{'label': rango, 'value': rango} for rango in cubo_regimen_genero_edad['RangoEdad'].unique()],
                value=cubo_regimen_genero_edad['RangoEdad'].unique().tolist(),
                inline=True,
                style={'margin-top': '10px'}
            ),
            dcc.Graph(id='grafico-dispersión')
        ], style={'flex': '1', 'padding': '20px'}),

        # Gráfico de pastel (derecha)
        html.Div([
            html.H2("Inscripción por Régimen y Mes", style={'textAlign': 'center'}),
            dcc.Dropdown(
                id='mes-dropdown',
                options=[{'label': mes, 'value': mes} for mes in cubo_mes_regimen['MesNombre'].unique()],
                value=cubo_mes_regimen['MesNombre'].iloc[0],
                style={'width': '50%', 'margin': '0 auto'}
            ),
            dcc.Graph(id='regimen-pie-chart')
        ], style={'flex': '1', 'padding': '20px'})
    ], style={'display': 'flex', 'gap': '20px'}),

        #Resumen
    html.Div([
    html.H4("Análisis del Registro de Pacientes y Potencial de Promoción", 
            style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
    html.Div([
        html.P("¿En qué fecha se registraron más pacientes para el régimen más aceptado?", 
               style={'font-weight': 'bold'}),
        html.P("En el año 2023, se registraron un total de 2,000 pacientes. Los meses con el mayor ingreso de pacientes fueron enero, febrero, marzo y abril, destacando enero como el mes con el mayor número de registros. Este dato sugiere que enero representa una excelente oportunidad para planificar y ejecutar una promoción efectiva, dado que la demanda es alta al inicio del año. Además, abril también experimentó un buen incremento en el registro de pacientes, lo cual podría estar relacionado con las promociones que se implementaron en ese mes. En consecuencia, sugerimos considerar el inicio de una promoción en enero, ya que es el mes con el mayor volumen de registros."),
        html.P("¿Qué tipo de régimen tienen más pacientes y cuántos se apegan a él? "),
        html.P("El regimen con mas pacientes y al que mejor se apegan a su cumplimiento es el Regimen Dieta Baja en Grasas con un total de 390 pacientes y un cumplimiento relativo del 20%. Podemos sugerir seguir implementando junto con algún tipo de promoción y mas publicidad del mismo."),
    ], style={'margin-bottom': '20px', 'color': '#34495e'}),
    
    html.Div([
        html.H4("Análisis de los Regímenes y el Apego de Pacientes", style={'font-family': 'Roboto, Arial, sans-serif'}),
        html.P("En cuanto a los regímenes, los datos muestran que existen dos regímenes que, debido a su costo, podrían estar limitando la decisión de muchos pacientes a optar por ellos. Estos regímenes son: Dieta de Ganancia Muscular y Dieta de Proteínas, los cuales presentan un número muy bajo de pacientes registrados, apenas alcanzando unos pocos."),
        html.P("Esta baja adherencia puede estar relacionada con el alto costo asociado a estos regímenes, lo que genera una brecha significativa en la cantidad de pacientes interesados. Se sugiere revisar y ajustar estos regímenes, considerando tanto su accesibilidad económica como las variaciones en el precio de los alimentos según la temporada y el abastecimiento disponible."),
    ], style={'margin-bottom': '20px', 'color': '#34495e'}),
    
    html.Div([
        html.H4("Cumplimiento con las Citas y Beneficios de la Promoción", style={'font-family': 'Roboto, Arial, sans-serif'}),
        html.P("En cuanto al cumplimiento de citas, se observa una tendencia de baja adherencia al régimen en el mes de diciembre, a pesar de que una buena parte de los pacientes se registró en abril. Esto sugiere que, aunque los pacientes se inscriben con la intención de seguir el régimen, la tasa de cumplimiento en términos de asistencia a citas es baja."),
        html.P("Este fenómeno podría explicarse por la falta de un seguimiento adecuado, por lo que se recomienda implementar un sistema de seguimiento más efectivo para los pacientes, con el fin de aumentar el nivel de cumplimiento y garantizar que se beneficien de las promociones que se ofrecen."),
        html.P("Finalmente, al evaluar el potencial de las promociones, se observa que enero es el mes con mayor número de registros de pacientes, lo que lo convierte en un mes clave para la implementación de promociones efectivas. Si bien abril también mostró un incremento de registros, la tendencia de enero sigue siendo la más sólida, lo que justifica la sugerencia de concentrar esfuerzos promocionales en ese mes.")
    ], style={'margin-bottom': '20px', 'color': '#34495e'}),
    
    html.Div([
        html.H4("Resumen", style={'font-family': 'Roboto, Arial, sans-serif'}),
        html.Ul([
            html.Li("Mes con más registros de pacientes: Enero."),
            html.Li("Mes con mayor potencial para promociones: Enero, debido al alto número de registros."),
            html.Li("Regímenes con menor apego: Dieta de Ganancia Muscular y Dieta de Proteínas, debido a su alto costo."),
            html.Li("Cumplimiento con citas en diciembre: Bajo, con la necesidad de un mejor seguimiento de pacientes."),
        ], style={'color': '#34495e'}),
    ], style={'padding': '10px', 'border-top': '1px solid #ecf0f1'}),
        
    ], style={
        'flex': '1', 
        'padding': '20px', 
        'border': '1px solid #ecf0f1', 
        'border-radius': '5px',
        'background-color': '#f9f9f9', 
        'margin': '10px'
    }),
    html.Div([
    # Reporte de Resultados y Recomendaciones
    html.Div([
        html.H4("Reporte de Resultados y Recomendaciones", 
                style={'textAlign': 'center', 'font-family': 'Roboto, Arial, sans-serif', 'color': '#2c3e50'}),
        html.Div([
            html.P("Se desarrolló un modelo predictivo utilizando el algoritmo Random Forest, entrenado con datos de los regímenes alimenticios. El modelo alcanzó un "
                   "accuracy de 1.0, lo que significa que clasifica correctamente si los pacientes cumplen o no con un régimen en función de variables clave como "
                   "costo, satisfacción y cumplimiento.", 
                   style={'margin-bottom': '10px', 'color': '#34495e'}),
            html.P("Con base en los resultados del modelo, se recomiendan las siguientes acciones para alcanzar las metas del Balance Score Card:", 
                   style={'margin-bottom': '10px', 'color': '#34495e'}),
            html.Ul([
                html.Li("Optimizar costos de regímenes alimenticios: Reducir el costo de la Dieta de Ganancia Muscular y Dieta de Proteínas para mejorar accesibilidad y adherencia."),
                html.Li("Aumentar la retención de pacientes: Personalizar regímenes con mayor flexibilidad en los menús y garantizar equivalencia nutricional para alcanzar una retención superior al 95%."),
                html.Li("Mejorar la satisfacción con el sistema de seguimiento: Fortalecer la herramienta móvil y garantizar un contacto más cercano mediante consultas periódicas, elevando la satisfacción promedio por encima de 4.5/5."),
                html.Li("Incrementar los ingresos netos: Concentrar promociones estratégicas en enero, el mes con mayor potencial de registros, enfocadas en regímenes accesibles y altamente valorados."),
            ], style={'color': '#34495e', 'font-family': 'Roboto, Arial, sans-serif'}),
        ], style={'margin-bottom': '20px'}),
    ], style={
        'padding': '20px', 
        'border': '1px solid #ecf0f1', 
        'border-radius': '5px',
        'background-color': '#f9f9f9', 
        'margin': '10px'
    }),
    ])  
])


# Callbacks

# Gráfico de barras
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
    Output('grafico-dispersión', 'figure'),
    [Input('filtro-genero', 'value'),
     Input('filtro-rango-edad', 'value')]
)
def actualizar_grafico_dispersión(genero, rangos_edad):
    # Filtrar datos según el género
    df_filtrado = cubo_regimen_genero_edad.copy()
    if genero:
        df_filtrado = df_filtrado[df_filtrado['Genero'] == genero]

    # Filtrar datos según los rangos de edad
    if rangos_edad:
        df_filtrado = df_filtrado[df_filtrado['RangoEdad'].isin(rangos_edad)]

    # Verificar si hay datos tras aplicar los filtros
    if df_filtrado.empty:
        return px.scatter(title="Sin datos para mostrar con los filtros seleccionados")

    # Agrupar datos por NombreRegimen
    df_agrupado = df_filtrado.groupby("NombreRegimen").agg({
        "NumeroPacientes": "sum"
    }).reset_index()

    # Calcular el cumplimiento relativo (como porcentaje del total de pacientes)
    total_pacientes = df_agrupado["NumeroPacientes"].sum()
    df_agrupado["CumplimientoRelativo"] = (df_agrupado["NumeroPacientes"] / total_pacientes) * 100

    # Crear gráfico de dispersión con color por 'NombreRegimen' y tamaño por 'NumeroPacientes'
    fig = px.scatter(
        df_agrupado,
        x="NombreRegimen",
        y="NumeroPacientes",
        size="NumeroPacientes",  # Tamaño basado en el número de pacientes
        color="CumplimientoRelativo",  # Color basado en el cumplimiento relativo
        color_continuous_scale='Viridis',  # Escala de color para cumplir con la variabilidad
        labels={
            "NombreRegimen": "Nombre del Régimen",
            "NumeroPacientes": "Número de Pacientes",
            "CumplimientoRelativo": "Cumplimiento Relativo (%)"
        },
        title="Distribución de Pacientes por Régimen y Cumplimiento Relativo"
    )
    return fig

# Gráfico de pastel
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
