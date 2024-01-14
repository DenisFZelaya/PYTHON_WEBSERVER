from flask import Blueprint, jsonify, request

verbos_bp = Blueprint("verbos", __name__)

@verbos_bp.route("/api/verbos/get", methods=["GET"])
def get():
    data = {"mensaje":"Verbo get exitoso"}
    return jsonify(data)

@verbos_bp.route("/api/verbos/post", methods=["POST"])
def post():
    data = {"mensaje":"Verbo post exitoso"}
    return jsonify(data)

@verbos_bp.route("/api/verbos/put", methods=["PUT"])
def put():
    data = {"mensaje":"Verbo PUT exitoso"}
    return jsonify(data)

@verbos_bp.route("/api/verbos/delete", methods=["DELETE"])
def delete():
    data = {"mensaje":"Verbo DELETE exitoso"}
    return jsonify(data)

# Verbos con parametros
@verbos_bp.route("/api/verbos/post/data", methods=["POST"])
def POST_BODY_PARAMS():
    return jsonify({"data":  request.get_json()})

@verbos_bp.route("/api/verbos/post/header-params", methods=["POST"])
def POST_HEADER_PARAMS():
    return jsonify({"token":  request.headers.get("Authorization")
})