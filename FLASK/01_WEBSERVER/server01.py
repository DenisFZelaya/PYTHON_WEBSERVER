from flask import Flask, jsonify, request

# Crear una instancia de la app
app = Flask(__name__)

print("NAME: ", __name__)

# Definicion de rutas de la API

@app.route("/api/ejemplo", methods=["GET"])

def obtener_ejemplo():
    print("Invoke Obtener Ejemplo")
    # Retornar un json
    datos = {"mensaje": "API Response"}
    return jsonify(datos)

@app.route("/api/healt", methods=["GET"])
def healtcheck():
    print("Invoke HealtCheck")
    response = {"success": True, "msj": "Server is up!"}
    return response


@app.route("/api/optional/params")
def optionalParams():
    print("Invoke Optional Params")
    nombre = request.args.get("nombre")

    datos = {"mensaje": "API Response", "nombre": nombre }
    return datos

@app.route("/api/usuario/<int:id>/edad/<int:edad>", methods=["GET"])
def obtener_usuario(id, edad):
    print("Obtener usuario segun el ID")

    datos = { "id": id, "edad": edad, "response": "Obtener el usuario por el id proporcionado"}
    return datos

# Iniciar el servidor 
if __name__ == '__main__':
    # Configurar el puerto de salida
    puerto = 9000
    print("CORRIENDO EN PUERTO: ", puerto)
    app.run(port=puerto)
    