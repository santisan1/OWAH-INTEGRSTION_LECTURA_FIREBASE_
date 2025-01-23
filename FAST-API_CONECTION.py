from fastapi import FastAPI
from firebase_admin import credentials, firestore, initialize_app
from fastapi.middleware.cors import CORSMiddleware

# Inicializar la aplicación FastAPI
app = FastAPI()

# Configurar CORS para permitir solicitudes desde tu frontend
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://127.0.0.1:5500"],  # Permitir solicitudes desde el origen de tu frontend
    allow_credentials=True,
    allow_methods=["*"],  # Permitir todos los métodos HTTP (GET, POST, etc.)
    allow_headers=["*"],  # Permitir todos los encabezados
)

# Configurar Firebase
cred = credentials.Certificate("firebase_config.json")
initialize_app(cred)
db = firestore.client()

# Ruta de prueba para obtener datos de Firebase
@app.get("/get-data/{sensor_name}")
async def get_data(sensor_name: str):
    try:
        # Verificar que la ruta y el nombre del documento sean correctos
        print(f"Buscando datos para el sensor: {sensor_name}")
        
        # Accedemos al documento "sensor_data" de la colección "sensores_TTE"
        doc_ref = db.collection("sensores_TTE").document("sensor_data")
        doc = doc_ref.get()

        if doc.exists:
            data = doc.to_dict()
            print(f"Datos obtenidos del documento: {data}")  # Muestra los datos del documento

            # Verificar si el sensor solicitado está presente en los datos
            if sensor_name in data:
                print(f"Datos deel sensor {sensor_name}: {data[sensor_name]}")  # Muestra los datos del sensor específico
                return {"status": "success", "data": {sensor_name: data[sensor_name]}}
            else:
                print(f"Sensor {sensor_name} no encontrado en el documento")
                return {"status": "error", "message": f"Sensor {sensor_name} no encontrado"}
        else:
            print("Documento 'sensor_data' no encontrado")
            return {"status": "error", "message": "Documento 'sensor_data' no encontrado"}

    except Exception as e:
        print(f"Error: {e}")  # Para capturar errores más específicos
        return {"status": "error", "message": str(e)}
