import pandas as pd
from sqlalchemy import create_engine
from dash import Dash, dcc, html, dash_table
from dash.dependencies import Input, Output
import plotly.express as px

# Conexión a la base de datos
engine = create_engine('mysql+mysqlconnector://root:@localhost/nutriologo')

# Cargar los datos del cubo OLAP
df_cubo1 = pd.read_sql('SELECT * FROM cubo_olap_1', engine)

# Inicializar la app de Dash
app = Dash(__name__)

# Layout del dashboard
app.layout = html.Div([
    html.Div([
        html.H1("Análisis de Regímenes Nutricionales", 
                style={
                    'text-align': 'center', 
                    'color': '#333333', 
                    'background-color': '#eaeaea', 
                    'padding': '15px', 
                    'border-radius': '8px', 
                    'font-family': 'Comic Sans MS, Verdana'
                }),
    ], style={'margin-bottom': '20px'}),
    
    html.Div([
        html.Div([
            html.H3("Análisis Gráfico de Regímenes", 
                    style={'color': '#444444', 'font-family': 'Comic Sans MS, Verdana'}),
            dcc.Dropdown(
                id='metricas-dropdown',
                options=[
                    {'label': 'Costo del Régimen', 'value': 'CostoRegimen'},
                    {'label': 'Cantidad de Pacientes', 'value': 'CantidadPacientes'},
                    {'label': 'Satisfacción Promedio', 'value': 'SatisfaccionPromedio'}
                ],
                value='CantidadPacientes',
                placeholder="Seleccione una métrica para graficar",
                style={
                    'width': '60%', 'margin': '0 auto 20px auto', 'padding': '10px',
                    'border-radius': '5px', 'border': '1px solid #444444', 'font-size': '16px',
                    'font-family': 'Comic Sans MS, Verdana'
                }
            ),
            dcc.Graph(id='grafico-metricas'),
        ], style={
            'background-color': '#f5f5f5', 
            'padding': '20px', 
            'border-radius': '10px', 
            'box-shadow': '0 2px 6px rgba(0, 0, 0, 0.1)'
        })
    ], style={
        'margin-bottom': '20px', 
        'width': '90%', 
        'margin-left': 'auto', 
        'margin-right': 'auto'
    }),
    
    html.Div([
        html.H3("Recomendación de Promociones", 
                style={'color': '#444444', 'font-family': 'Comic Sans MS, Verdana'}),
        html.P(
            "Regímenes con alta satisfacción y pocos pacientes podrían ser candidatos para promociones.", 
            style={'font-size': '16px', 'color': '#555555', 'font-family': 'Comic Sans MS, Verdana'}
        ),
        dash_table.DataTable(
            id='tabla-promociones',
            columns=[
                {'name': 'Nombre del Régimen', 'id': 'NombreRegimen'},
                {'name': 'Costo del Régimen', 'id': 'CostoRegimen'},
                {'name': 'Cantidad de Pacientes', 'id': 'CantidadPacientes'},
                {'name': 'Satisfacción Promedio', 'id': 'SatisfaccionPromedio'}
            ],
            data=[],
            style_table={'overflowX': 'auto', 'margin-top': '20px'},
            style_cell={
                'textAlign': 'center', 
                'font-family': 'Comic Sans MS, Verdana', 
                'padding': '10px', 
                'font-size': '14px'
            },
            style_header={
                'backgroundColor': '#dcdcdc', 
                'color': '#333333', 
                'fontWeight': 'bold', 
                'textAlign': 'center'
            },
            style_data={
                'backgroundColor': '#ffffff', 
                'border': '1px solid #cccccc'
            },
            page_size=5
        )
    ], style={
        'background-color': '#f5f5f5', 
        'padding': '20px', 
        'border-radius': '10px', 
        'box-shadow': '0 2px 6px rgba(0, 0, 0, 0.1)', 
        'width': '90%', 
        'margin-left': 'auto', 
        'margin-right': 'auto'
    })
])

# Callback para actualizar el gráfico según la métrica seleccionada
@app.callback(
    Output('grafico-metricas', 'figure'),
    [Input('metricas-dropdown', 'value')]
)
def actualizar_grafico(metrica_seleccionada):
    fig = px.bar(
        df_cubo1,
        x='NombreRegimen',
        y=metrica_seleccionada,
        title=f'{metrica_seleccionada} por Régimen',
        text=metrica_seleccionada,
        labels={metrica_seleccionada: metrica_seleccionada, 'NombreRegimen': 'Nombre del Régimen'},
        template='plotly_white'
    )
    fig.update_traces(
        texttemplate='%{text:.2s}', 
        textposition='outside', 
        marker_color='#777777'
    )
    fig.update_layout(
        yaxis=dict(title=metrica_seleccionada, showgrid=True, gridcolor='#e0e0e0'),
        xaxis=dict(title='Régimen', showgrid=False),
        title=dict(font=dict(size=20, family='Comic Sans MS, Verdana'), x=0.5),
        plot_bgcolor='#f9f9f9',
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig

# Callback para calcular y mostrar las recomendaciones de promociones
@app.callback(
    Output('tabla-promociones', 'data'),
    [Input('grafico-metricas', 'figure')]  # Escucha cambios en los datos graficados
)
def recomendar_promociones(_):
    # Filtrar regímenes con alta satisfacción y pocos pacientes (umbral ejemplo)
    df_recomendaciones = df_cubo1[
        (df_cubo1['SatisfaccionPromedio'] > 4.0) &  # Alta satisfacción
        (df_cubo1['CantidadPacientes'] < 20)       # Pocos pacientes
    ]
    return df_recomendaciones.to_dict('records')

# Ejecutar la app
if __name__ == '__main__':
    app.run_server(debug=True)
