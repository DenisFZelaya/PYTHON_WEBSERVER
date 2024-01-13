from flask import Blueprint, jsonify

healt_bp = Blueprint('healt', __name__)

@healt_bp.route("/api/healt", methods=["GET"])
def test():
    return {"mensaje":"Healtcheck exitoso"}