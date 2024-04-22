from flask import Blueprint, request, jsonify
import datetime, jwt
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from msAuthentication.modules.user.dao import DAOUser

user_controller = Blueprint('user_controller', __name__)
dao_user = DAOUser()
module_name = 'user'

SECRET_KEY = 'chave_secreta'

@user_controller.route("/api/v1/authentication/token/", methods=["POST"])
def get_token():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")

    if dao_user.verify_credentials(username, password):
        payload = {
            "sub": username,
            "exp": datetime.datetime.utcnow() + datetime.timedelta(hours=1)
        }
        token = jwt.encode(payload, SECRET_KEY, algorithm="HS256")
        return jsonify({"token": token}), 200
    else:
        return jsonify({"error": "Credenciais invalidas."}), 400

@user_controller.route("/api/v1/authentication/validation/", methods=["POST"])
def validate_token():
    data = request.get_json()
    token = data.get("token")
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        return jsonify({"message": "Token válido"}), 200
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirada."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token invalida."}), 400

@user_controller.route("/api/v1/authentication/check/", methods=["GET"])
@jwt_required()
def check_token():
    verify_jwt_in_request()
    return jsonify({"message": "Token válido"}), 200
