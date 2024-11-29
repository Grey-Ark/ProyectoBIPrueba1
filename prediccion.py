import pandas as pd
import numpy as np
from sqlalchemy import create_engine
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import mean_absolute_error, r2_score
import matplotlib.pyplot as plt

# Conexión a la base de datos
engine = create_engine("mysql+pymysql://root:@localhost/nutriologo")

# Cargar los cubos de datos
df_cubo1 = pd.read_sql("SELECT * FROM cubo_olap_1", engine)
cubo_olap = pd.read_sql("SELECT * FROM cubo_olap", engine)
cubo_regimen_genero_edad = pd.read_sql("SELECT * FROM cubo_regimen_genero_edad", engine)
cubo_mes_regimen = pd.read_sql("SELECT Mes, NombreRegimen, CumplimientoCitas, NumeroPacientes FROM cubo_mes_regimen", engine)

# 1. Exploración de los datos
print(df_cubo1.head())
print(cubo_olap.head())
print(cubo_regimen_genero_edad.head())
print(cubo_mes_regimen.head())

# 2. Limpiar datos (eliminar nulos o registros inconsistentes)
df_cubo1.dropna(inplace=True)
cubo_olap.dropna(inplace=True)
cubo_regimen_genero_edad.dropna(inplace=True)
cubo_mes_regimen.dropna(inplace=True)

# 3. Análisis descriptivo básico
# Ver cómo se distribuyen los pacientes por régimen
regimen_counts = cubo_mes_regimen.groupby('NombreRegimen')['NumeroPacientes'].sum()
print(regimen_counts)

# Ver la relación entre el cumplimiento de citas y el número de pacientes
cumplimiento_vs_pacientes = cubo_mes_regimen.groupby('Mes')[['CumplimientoCitas', 'NumeroPacientes']].mean()
print(cumplimiento_vs_pacientes)

# 4. Preparación de los datos para el modelo predictivo
# Para predecir el cumplimiento de citas, vamos a utilizar las variables relevantes del cubo.
# Vamos a crear un dataframe con las variables de interés: 'Mes', 'NombreRegimen', 'NumeroPacientes' y 'CumplimientoCitas'.

# Variables de entrada (features) y variable objetivo (target)
X = cubo_mes_regimen[['NumeroPacientes', 'Mes']]
y = cubo_mes_regimen['CumplimientoCitas']

# Convertir las variables categóricas en numéricas (Mes y NombreRegimen)
X = pd.get_dummies(X, columns=['Mes'], drop_first=True)

# 5. Entrenamiento del modelo
# Dividir los datos en conjunto de entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# Usar un modelo de Random Forest para la predicción del cumplimiento de citas
model = RandomForestRegressor(n_estimators=100, random_state=42)
model.fit(X_train, y_train)

# 6. Evaluación del modelo
y_pred = model.predict(X_test)

# Métricas de desempeño del modelo
mae = mean_absolute_error(y_test, y_pred)
r2 = r2_score(y_test, y_pred)
print(f"Error absoluto medio (MAE): {mae}")
print(f"Coeficiente de determinación (R²): {r2}")

# 7. Predicción y recomendaciones
# Predicciones para el próximo mes o escenario específico
predicciones = model.predict(X)

# Agregar las predicciones a los datos originales
cubo_mes_regimen['PrediccionCumplimientoCitas'] = predicciones

# Filtrar las predicciones para encontrar los regímenes con mayor incumplimiento y sugerir acciones
incumplimiento_alto = cubo_mes_regimen[cubo_mes_regimen['PrediccionCumplimientoCitas'] < 0.8]

# Recomendaciones basadas en los resultados
acciones_recomendadas = []
for index, row in incumplimiento_alto.iterrows():
    regimen = row['NombreRegimen']
    if regimen == 'Dieta de Ganancia Muscular' or regimen == 'Dieta de Proteínas':
        acciones_recomendadas.append(f"Reducir el costo del régimen {regimen} o mejorar las promociones para incrementar la adherencia.")

# 8. Visualización de los resultados
# Graficar el cumplimiento de citas real vs. predicción
plt.figure(figsize=(10,6))
plt.scatter(y_test, y_pred, color='blue')
plt.plot([0, 1], [0, 1], color='red', linestyle='--')
plt.xlabel('Cumplimiento de Citas Real')
plt.ylabel('Cumplimiento de Citas Predicho')
plt.title('Cumplimiento de Citas Real vs. Predicción')
plt.show()

# Mostrar las recomendaciones generadas
for recomendacion in acciones_recomendadas:
    print(recomendacion)

