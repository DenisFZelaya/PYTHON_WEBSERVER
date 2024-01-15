from flask import Blueprint, jsonify, request, abort

middleware_bp = Blueprint("middleware", __name__)

# Middleware específico para el blueprint antes de la solicitud principal
@middleware_bp.before_request
def middleware_blueprint_before_request():

    auth_header = request.headers.get('Authorization')
    print("auth_header: ", auth_header)
    print("Middleware específico para el blueprint antes de la solicitud principal")

    if auth_header == None:
        # Puedes realizar acciones como abortar la solicitud si el parámetro no está presente
        abort(401, description='Falta el parámetro en el encabezado de autorización')

# Middleware específico para el blueprint después de la solicitud principal
@middleware_bp.after_request
def middleware_blueprint_after_request(response):
    print("Middleware específico para el blueprint después de la solicitud principal")
    return response

@middleware_bp.route("/middleware/1", methods=["GET"])
def Func1():
    auth_header = request.headers.get('Authorization')
    return jsonify({"msj": "Middleware: " + auth_header})
