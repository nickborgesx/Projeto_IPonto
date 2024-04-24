import requests
from flask import Blueprint, request, jsonify, make_response
from iponto.modules.company.dao import DAOCompany
from iponto.modules.company.modelo import Company
from iponto.modules.company.sql import SQLCompany

company_controller = Blueprint('company_controller', __name__)
dao_company = DAOCompany()
module_name = 'company'
SECRET_KEY = 'chave_secreta'
@company_controller.route('/api/v1/company/', methods=['POST'])
def create_company():
    token = request.headers.get('Authorization')
    auth_response = validate_token(token)

    if auth_response.status_code == 200:
        company_data = request.json
        errors = []

        for campo in SQLCompany._CAMPOS_OBRIGATORIOS:
            if campo not in company_data or not str(company_data.get(campo, '')).strip():
                errors.append(f'O campo {campo} é obrigatório!')

        if dao_company.get_by_cnpj(company_data.get('cnpj')):
            errors.append('Já existe uma empresa com esse CNPJ')

        if errors:
            response = jsonify({'error': errors})
            response.status_code = 400
            return response

        new_company = Company(
            name=company_data.get('name'),
            cnpj=company_data.get('cnpj'),
            lat=company_data.get('lat'),
            lng=company_data.get('lng')
        )

        saved_company = dao_company.salvar(new_company)
        return jsonify({'id': saved_company.id}), 201

    elif auth_response.status_code == 401:
        return jsonify({'error': 'Token de autenticação inválido'}), 401
    else:
        return make_response(auth_response.text, auth_response.status_code)

def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post('http://127.0.0.1:5000/api/v1/authentication/validation/', headers=headers)
    return response

