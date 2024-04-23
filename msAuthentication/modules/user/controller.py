from flask import Blueprint, request, jsonify, make_response
import requests, jwt
from msAuthentication.modules.user.dao import DAOUser
from msAuthentication.modules.user.modelo import User

user_controller = Blueprint('user_controller', __name__)
dao_user = DAOUser()
module_name = 'user'

SECRET_KEY = 'chave_secreta'

@user_controller.route("/api/v1/authentication/token/", methods=["POST"])
def get_token():
    username = request.json.get('username')
    password = request.json.get('password')

    if not username or not password:
        return make_response(jsonify({'Erro': 'Nome de usuário e senha são obrigatórios'}), 400)

    user = DAOUser().verify_credentials(username, password)

    if user is not None:
        payload = {'username': username}
        token = jwt.encode(payload, SECRET_KEY, algorithm='HS256')
        return jsonify({'token': token}), 200
    else:
        return make_response(jsonify({'Erro': 'Nome de usuário ou senha inválidos'}), 401)

@user_controller.route("/api/v1/authentication/validation/", methods=["POST"])
def validate_token():
    try:
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Token não fornecido."}), 401
        token = token.replace('Bearer ', '')
        decoded_token = jwt.decode(token, SECRET_KEY, algorithms=['HS256'])
        username = decoded_token.get('username')
        if not username:
            return jsonify({"error": "Nome de usuário ausente no token."}), 400
        user = DAOUser().user_name(username)
        if user is not None:
            return jsonify({"message": "Token válido"}), 200
        else:
            return jsonify({"error": "Usuário associado ao token não encontrado."}), 401
    except jwt.ExpiredSignatureError:
        return jsonify({"error": "Token expirada."}), 401
    except jwt.InvalidTokenError:
        return jsonify({"error": "Token inválido."}), 400


