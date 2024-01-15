from flask import Flask
from blueprints.user_routes import user_bp
from blueprints.healt_routes import healt_bp
from blueprints.verbos_routes import verbos_bp
from blueprints.middleware_routes import middleware_bp
from blueprints.roles_routes import roles_bp

# Crear instancia
app = Flask(__name__)

# Registrar los blueprints
app.register_blueprint(user_bp)
app.register_blueprint(healt_bp)
app.register_blueprint(verbos_bp)
app.register_blueprint(middleware_bp)
app.register_blueprint(roles_bp)

if __name__ == '__main__':
    puerto = 9000
    print("CORRIENDO EN PUERTO: ", puerto)
    app.run(port=puerto)