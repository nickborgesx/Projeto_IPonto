from flask import Blueprint, request, jsonify
import jwt
import datetime
from modules.users.controller import dao_users

auth_blueprint = Blueprint('auth', __name__)

SECRET_KEY = "secret"

@auth_blueprint.route("/api/vi/authentication/token/", methods=["POST"])
def get_token():
    data = request.get_json()
    username = data.get("name")
    password = data.get("password")

    if dao_users.verify_credentials(username, password):
        payload = {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1) #Estudar depois a questão do tempo no JWT
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Usuario invalidos ou nao existente."}), 400

@auth_blueprint.route("/api/vi/authentication/validation/", methods=["POST"])
def validate_token():
    data = request.get_json()
    token = data.get("token")

    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirado"}), 401
    except jwt.DecodeError:
        return jsonify({"error": "Token invalido ou nao autorizado"}), 401
