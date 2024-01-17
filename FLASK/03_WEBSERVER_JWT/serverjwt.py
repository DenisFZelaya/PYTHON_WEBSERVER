from flask import Flask, jsonify, request, abort
from flask_jwt_extended import JWTManager, verify_jwt_in_request, create_access_token, jwt_required, get_jwt_identity, get_jwt
from base64 import b64decode
from datetime import timedelta
from flask_swagger_ui import get_swaggerui_blueprint
from flasgger import Swagger, swag_from

SWAGGER_URL="/swagger"
API_URL="/static/swagger.json"

swagger_ui_blueprint = get_swaggerui_blueprint(
    SWAGGER_URL,
    API_URL,
    config={
        'app_name': 'Access API'
    }
)

app = Flask(__name__)

app.config["JWT_SECRET_KEY"] = 'my_secret_key'
app.register_blueprint(swagger_ui_blueprint, url_prefix=SWAGGER_URL)
jwt = JWTManager(app)
swagger = Swagger(app)


def extract_credentials(authorization_header):
    # Decodificar el encabezado de autorización
    decoded_credentials = b64decode(authorization_header).decode('utf-8')

    # Separar el nombre de usuario y la contraseña
    username, password = decoded_credentials.split(':', 1)

    return username, password


def verificar_roles_requeridos(roles_requeridos, roles_usuario):
    if not roles_requeridos:
        return True
    return any(rol in roles_requeridos for rol in roles_usuario)

# Middleware
@app.before_request
def middleware_general():
    roles_necesarios = []
    roles_usuario = []

    print("ENDPOINT: ", request.endpoint)

    try:
        if request.endpoint != 'login' and request.endpoint != "swagger_ui.show" and request.endpoint != "static" :
        # if request.endpoint != 'login' and not request.path.startswith('/swagger'):
            print("ENTRA")
            verify_jwt_in_request()
            roles = get_jwt()["roles"]
            roles_usuario = roles
    except Exception as e:
        # Manejo genérico para otras excepciones
        roles_usuario = []
        print(f"Otro tipo de error: {e}")
        abort(403, description=(f"Excepcion: {e}"))

    # Especifica los roles permitidos para cada endpoint
    if request.endpoint == 'login':
        roles_necesarios = []

    if request.endpoint == 'protegido':
        roles_necesarios = ['ADM', 'SUPER']

    if request.endpoint == 'rrhh':
        roles_necesarios = ['RRHH']

    # Desencriptar y verificar roles
    if not verificar_roles_requeridos(roles_necesarios, roles_usuario):
        abort(403, description='No tienes permiso para acceder a esta ruta')

# En login se genera el login
@app.route("/api/login", methods=["POST"])
@swag_from('swagger_doc/login.yml')
def login():

    # Verificar la existencia del encabezado de autorización
    authorization_header = request.headers.get('Authorization')
    if authorization_header is None or not authorization_header.startswith('Basic '):
        return 'Authorization header missing or invalid', 401

    # Extraer las credenciales
    username, password = extract_credentials(
        authorization_header[len('Basic '):])
    
    if not isinstance(username, str) or not username.strip():
        return jsonify({"error": "El campo 'username' debe ser una cadena no vacía"}), 401

    # Validar el usuario y contraseña (deberías realizar la validación real aquí)
    if username and password:

        roles = []
        
        # Lógica para asignar roles según el username
        if username == 'DFZ':
            roles.extend(["ADM", "SUPER"])
        elif username == 'RRHH':
            roles.append("RRHH")
        
        # Crear token de acceso con información adicional (claims)
        user_info = {
            'nombre': username,
            'correo': 'usuario@example.com',
            "roles": roles
        }

        # Configurar la duración del token (en este caso, expira en 1 día)
        expires_in = timedelta(days=1, hours=2)

        access_token = create_access_token(
            identity=username, additional_claims=user_info, expires_delta=expires_in)
        return jsonify({
            "valid": True,
            "access_token": access_token
        }), 200
    else:
        return jsonify({"error": "Credenciales incorrectas"}), 401


@app.route('/api/protegido', methods=['GET'])
@jwt_required()
def protegido():
    """
    Ruta protegida que requiere un token JWT válido.

    ---
    tags:
      - "Auth"
    responses:
      200:
        description: "OK"
        schema:
          type: "object"
          properties:
            logged_in_as:
              type: "string"
            user_info:
              type: "object"
            roles:
              type: "array"
    """
    # Obtener la identidad del usuario y las claims adicionales del token JWT
    current_user = get_jwt_identity()
    additional_claims = get_jwt()
    roles = get_jwt()["roles"]

    return jsonify(logged_in_as=current_user, user_info=additional_claims, roles=roles), 200


@app.route('/api/rrhh', methods=['GET'])
@jwt_required()
def rrhh():
    # Obtener la identidad del usuario y las claims adicionales del token JWT
 
    return jsonify({"msj": "ERES DEL EQUIPO DE RRHH"}), 200


if __name__ == '__main__':
    puerto = 9000
    print("CORRIENDO EN PUERTO: ", puerto)
    app.run(port=puerto)
