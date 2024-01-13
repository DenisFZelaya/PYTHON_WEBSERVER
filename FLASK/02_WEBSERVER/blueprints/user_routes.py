from flask import Blueprint, jsonify, request
from .user_functions import test2

user_bp = Blueprint('user', __name__)

@user_bp.route("/api/test-user", methods=["GET"])
def test():
    return {"mensaje":"Prueba blueprint user exitosa"}

@user_bp.route("/api/user", methods=["POST"])
def user():
    # Obtener datos del cuerpo (body) de la solicitud
    datos_body = request.get_json()

    # Obtener el token de autorización del encabezado
    auth_token = request.headers.get("Authorization")

    # Procesar los datos y el token
    resultado = procesar_datos(datos_body, auth_token)

    return jsonify(resultado)

def procesar_datos(datos_body, auth_token):
    # Lógica para procesar los datos y el token
    resultado = {"datos_body": datos_body, "auth_token": auth_token}
    return resultado

@user_bp.route("/api/test-user2", methods=["GET"])
def test_route2():
    return test2()