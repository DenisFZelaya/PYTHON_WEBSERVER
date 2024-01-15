from flask import Blueprint, jsonify, request, abort

roles_bp =Blueprint("roles", __name__)

def verificar_roles_requeridos(roles_requeridos, roles_usuario):
    # Si roles_requeridos está vacío, retorna True
    if not roles_requeridos:
        return True
    
    # Retorna True si al menos uno de los roles requeridos está presente en los roles del usuario
    # return any(rol in roles_usuario for rol in roles_requeridos)
    return any(rol in roles_requeridos for rol in roles_usuario)

# Middleware
@roles_bp.before_request
def middleware_blueprint_before_request():
    roles_necesarios = []
    roles_usuario = []

    print("ENDPOINT: ", request.endpoint)

    try:
        roles_usuario = request.get_json().get('roles') if request.get_json() and 'roles' in request.get_json() else []
    except Exception as e:
        # Manejo genérico para otras excepciones
        roles_usuario = []
        print(f"Otro tipo de error: {e}")

    # Especifica los roles permitidos para cada endpoint
    if request.endpoint == 'roles.Roles':
        roles_necesarios = []
    
    if request.endpoint == 'roles.ADM':
        print("ADM INVOKE: ")
        roles_necesarios = ['ADM', 'SUPER']

    # Desencriptar y verificar roles
    if not verificar_roles_requeridos(roles_necesarios, roles_usuario):
        abort(403, description='No tienes permiso para acceder a esta ruta')
 
@roles_bp.route("/api/roles", methods=["GET"])
def Roles():
    return jsonify({
        "roles": ["ADM","RRHH", "OFICIAL", "SUPER"]
})

@roles_bp.route("/api/adm", methods=["GET"])
def ADM():
    return jsonify({
        "msj": "EXITO ADM"
})