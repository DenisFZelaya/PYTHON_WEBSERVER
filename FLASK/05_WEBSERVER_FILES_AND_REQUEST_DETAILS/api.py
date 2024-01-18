from flask import Flask, jsonify, request, render_template
import json
from datetime import datetime

# Crear una instancia de la app
app = Flask(__name__)

# Definicion de rutas de la API
@app.route("/", methods=["GET"])
def index():
    print("Invoke Obtener Ejemplo")
    # Retornar un json
    
    # Ruta del archivo JSON
    ruta_archivo = 'logs.json'
    fecha_actual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    
    datos = {
        "date": fecha_actual,
        "user_agent": request.user_agent.string,
        "remote_addr": request.remote_addr,
        "remote_user": request.remote_user,
        "access_route": request.access_route,
        "url": request.url,
        "scheme": request.scheme,
        "referrer": request.referrer,
        "path": request.path,
        "host": request.host,
        "host_url": request.host_url,
        "endpoint": request.endpoint,
    }
    
    try:
        # Abrir el archivo en modo anexar ('a')
        with open(ruta_archivo, 'a') as archivo: 
            json.dump(datos, archivo)
            archivo.write(',\n')

        # Mensaje de éxito
        mensaje = "Log guardado correctamente."

    except Exception as e:
        # Mensaje de error en caso de problemas
        mensaje = f"Error al guardar el log: {str(e)}"
        
    print(mensaje)
    return jsonify(datos)


# Iniciar el servidor
if __name__ == '__main__':
    # Configurar el puerto de salida
    puerto = 5000
    print("CORRIENDO EN PUERTO: ", puerto)
    # manager.run()
    app.run(port=puerto)
