from flask import Blueprint, request, jsonify
import jwt, datetime
from flask_jwt_extended import jwt_required, get_jwt_identity
from employees.modules.employees.controller import dao_employees

auth_blueprint = Blueprint('auth', __name__)

SECRET_KEY = "chave_secreta"

@auth_blueprint.route("/api/v1/authentication/token/", methods=["POST"])
def get_token():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if dao_employees.verify_credentials(username, password):
        payload = {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) #Estudar depois a questão do tempo no JWT
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Usuario invalidos ou nao existente."}), 400

@auth_blueprint.route("/api/v1/authentication/validation/", methods=["POST"])
@jwt_required()
def validate_token():
    current_user = get_jwt_identity()
    return jsonify({"username": current_user}), 200
