import pymysql
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score

# Conexión a la base de datos
connection = pymysql.connect(
    host='localhost',       # Cambia por tu host de la base de datos
    user='root',            # Cambia por tu usuario
    password='',    # Cambia por tu contraseña
    database='nutriologo'   # Nombre de la base de datos
)

# Consultar las tablas
query_cubo_mes_regimen = "SELECT * FROM cubo_mes_regimen;"
query_cubo_olap = "SELECT * FROM cubo_olap;"
query_cubo_olap_1 = "SELECT * FROM cubo_olap_1;"
query_cubo_olap_2 = "SELECT * FROM cubo_olap_2;"
query_cubo_regimen_genero_edad = "SELECT * FROM cubo_regimen_genero_edad;"

# Cargar los datos en DataFrames
cubo_mes_regimen = pd.read_sql(query_cubo_mes_regimen, connection)
cubo_olap = pd.read_sql(query_cubo_olap, connection)
cubo_olap_1 = pd.read_sql(query_cubo_olap_1, connection)
cubo_olap_2 = pd.read_sql(query_cubo_olap_2, connection)
cubo_regimen_genero_edad = pd.read_sql(query_cubo_regimen_genero_edad, connection)

# Cerrar la conexión
connection.close()

# Consolidar los datos
cubo_olap_2 = cubo_olap_2.rename(columns={"CantidadPacientes": "TotalPacientes"})
merged_data = cubo_olap.merge(cubo_olap_1, on="NombreRegimen").merge(cubo_olap_2, on="NombreRegimen")
merged_data["CumplimientoRegimen"] = merged_data["PacientesCumplenRegimen"] / merged_data["TotalPacientes"] * 100

# Preparar los datos para el modelo predictivo
X = merged_data[["CostoRegimen", "SatisfaccionPromedio", "SatisfaccionPaciente", "TotalPacientes"]]
y = (merged_data["CumplimientoRegimen"] > 50).astype(int)

# Dividir los datos en entrenamiento y prueba
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

# Construir el modelo Random Forest
model = RandomForestClassifier(random_state=42)
model.fit(X_train, y_train)

# Predicciones y evaluación
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
report = classification_report(y_test, y_pred)

# Imprimir resultados
print("Accuracy:", accuracy)
print("\nClassification Report:\n", report)
