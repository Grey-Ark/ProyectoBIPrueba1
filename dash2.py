import dash
from dash import dcc, html, Input, Output
import pandas as pd
from sqlalchemy import create_engine
import plotly.express as px

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar las tablas desde la base de datos
cubo_olap = pd.read_sql("SELECT * FROM cubo_olap", engine)
cubo_regimen_genero_edad = pd.read_sql("SELECT * FROM cubo_regimen_genero_edad", engine)

# Validar que las columnas necesarias existen
required_columns = ["NombreRegimen", "RangoEdad", "Genero", "NumeroPacientes"]
missing_columns = [col for col in required_columns if col not in cubo_regimen_genero_edad.columns]

if missing_columns:
    raise ValueError(f"Faltan columnas necesarias en 'cubo_regimen_genero_edad': {missing_columns}")

# Inicializar la aplicación Dash
app = dash.Dash(__name__)

# Obtener los valores únicos de los rangos de edad y géneros
rangos_edad = cubo_regimen_genero_edad["RangoEdad"].unique()
generos = cubo_regimen_genero_edad["Genero"].unique()

# Diseño de la aplicación
app.layout = html.Div([
    html.H1("Análisis de Cumplimiento por Régimen", style={'textAlign': 'center'}),
    
    # Dropdown para seleccionar el rango de edad
    html.Div([
        html.Label("Selecciona un Rango de Edad:"),
        dcc.Dropdown(
            id="filtro-rango-edad",
            options=[{"label": rango, "value": rango} for rango in rangos_edad],
            value=rangos_edad[0]  # Valor inicial
        )
    ], style={'margin-bottom': '20px'}),
    
    # Dropdown para seleccionar el género
    html.Div([
        html.Label("Selecciona un Género:"),
        dcc.Dropdown(
            id="filtro-genero",
            options=[{"label": genero, "value": genero} for genero in generos],
            value=generos[0]  # Valor inicial
        )
    ], style={'margin-bottom': '20px'}),
    
    # Gráficos
    dcc.Graph(id="grafico-barras"),
    dcc.Graph(id="grafico-lineas")
])

# Callback para actualizar los gráficos con base en los filtros seleccionados
@app.callback(
    [Output("grafico-barras", "figure"),
     Output("grafico-lineas", "figure")],
    [Input("filtro-rango-edad", "value"),
     Input("filtro-genero", "value")]
)
def actualizar_graficos(rango_edad, genero):
    # Filtrar los datos según el rango de edad y el género seleccionados
    datos_filtrados = cubo_regimen_genero_edad[
        (cubo_regimen_genero_edad["RangoEdad"] == rango_edad) &
        (cubo_regimen_genero_edad["Genero"] == genero)
    ]

    if datos_filtrados.empty:
        return px.bar(title="No hay datos para el filtro seleccionado"), px.line(title="No hay datos para el filtro seleccionado")

    # Agrupar por NombreRegimen y calcular el total de pacientes
    pacientes_por_regimen = datos_filtrados.groupby("NombreRegimen").agg({
        "NumeroPacientes": "sum"
    }).reset_index()

    # Unir con el cubo_olap para obtener el cumplimiento de citas
    merged_df = cubo_olap.merge(
        pacientes_por_regimen,
        on="NombreRegimen",
        how="inner",
        suffixes=("_olap", "_genero_edad")
    )

    # Verificar que las columnas necesarias están presentes
    if "CumplimientoCitas" not in merged_df.columns:
        raise ValueError("La columna 'CumplimientoCitas' no está presente en 'cubo_olap'.")

    # Calcular el cumplimiento relativo
    merged_df["CumplimientoRelativo"] = (
        merged_df["CumplimientoCitas"] / merged_df["NumeroPacientes"]
    )

    # Gráfico de barras
    fig_barras = px.bar(
        merged_df,
        x="NombreRegimen",
        y="CumplimientoRelativo",
        color="NombreRegimen",
        title=f"Cumplimiento Relativo por Régimen ({rango_edad} - {genero})",
        labels={"CumplimientoRelativo": "Cumplimiento Relativo (%)", "NombreRegimen": "Régimen"},
        color_discrete_sequence=px.colors.qualitative.Set2,
        hover_data={"NumeroPacientes": True}
    )

    # Gráfico de líneas
    fig_lineas = px.line(
        merged_df,
        x="NombreRegimen",
        y="CumplimientoRelativo",
        markers=True,
        title=f"Cumplimiento Relativo por Régimen ({rango_edad} - {genero})",
        labels={"CumplimientoRelativo": "Cumplimiento Relativo (%)", "NombreRegimen": "Régimen"},
        line_shape="linear",
        color="NombreRegimen"
    )

    return fig_barras, fig_lineas


# Ejecutar la aplicación
if __name__ == "__main__":
    app.run_server(debug=True)
