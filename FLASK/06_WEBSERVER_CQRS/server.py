from flask import Flask
from flask_restful import Api, Resource, reqparse
from webargs import fields, validate
from webargs.flaskparser import use_args

app = Flask(__name__)
api = Api(app)

# Base de datos simulada para almacenar datos
database = {'usuarios': {}}

# Command: Crear Usuario
class CrearUsuarioCommand(Resource):
    @use_args({
        'id': fields.Int(required=True),
        'nombre': fields.Str(required=True),
        'edad': fields.Int(required=True)
    })
    def post(self, args):
        try:
            usuario_id = args['id']
            usuario = {'nombre': args['nombre'], 'edad': args['edad']}
            database['usuarios'][usuario_id] = usuario
            return {'mensaje': f'Usuario {usuario_id} creado correctamente'}, 201
        except Exception as err:
            # Manejar errores de validación
            return {'error': err.messages}, 400

# Query: Obtener Usuario
class ObtenerUsuarioQuery(Resource):
    def get(self, usuario_id):
        usuario = database['usuarios'].get(usuario_id)
        if usuario:
            return {'usuario': usuario}
        else:
            return {'error': f'Usuario {usuario_id} no encontrado'}, 404

# Configurar los recursos en la API
api.add_resource(CrearUsuarioCommand, '/usuarios')
api.add_resource(ObtenerUsuarioQuery, '/usuarios/<int:usuario_id>')

if __name__ == '__main__':
    app.run(debug=True)
