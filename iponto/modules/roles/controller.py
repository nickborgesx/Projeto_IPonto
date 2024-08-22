import requests
from flask import request, Blueprint, jsonify, make_response
from iponto.modules.roles.dao import DAORoles
from iponto.modules.roles.modelo import Roles
from iponto.modules.roles.sql import SQLRoles

roles_controller = Blueprint('role_controller', __name__)
dao_roles = DAORoles()
module_name = 'roles'
SECRET_KEY = 'chave_secreta'



@roles_controller.route('/api/v1/role/', methods=['POST'])
def create_role():
    token = request.headers.get('Authorization')
    auth_response = validate_token(token)

    if auth_response.status_code == 200:
        roles_data = request.json
        errors = []
        for data in roles_data:
            for campo in SQLRoles._CAMPOS_OBRIGATORIOS:
                if campo not in data or not str(data.get(campo, '')).strip():
                    errors.append(f'O campo {campo} é obrigatório!')

            if dao_roles.get_by_title(**data):
                errors.append('Já existe esta função')

            if errors:
                response = jsonify({'error': errors})
                response.status_code = 400
                return response

            role = Roles(**data)
            dao_roles.create_role(role)
        return jsonify('sucesso'), 201

    elif auth_response.status_code == 401:
        return jsonify({'error': 'Token de autenticação inválido'}), 401
    else:
        return make_response(auth_response.text, auth_response.status_code)

def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post('http://127.0.0.1:5000/api/v1/authentication/validation/', headers=headers)
    return response