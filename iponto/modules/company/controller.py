import requests
from flask import Blueprint, request, jsonify, make_response
from iponto.modules.company.dao import DAOCompany
from iponto.modules.company.modelo import Company
from iponto.modules.company.sql import SQLCompany
from iponto.modules.employees.dao import DAOEmployees
from iponto.modules.employees.modelo import Employees

company_controller = Blueprint('company_controller', __name__)
dao_company = DAOCompany()
dao_employees = DAOEmployees()
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

@company_controller.route('/api/v1/employee/<int:id>/', methods=['PUT'])
def editar_funcionario(id):
    token = request.headers.get('Authorization')
    auth_response = validate_token(token)

    if auth_response.status_code == 200:

        data = request.json
        employee = Employees(
            name=data.get('name'),
            cpf=data.get('cpf'),
            roles_id=data.get('role_id'),
            company_id=data.get('company_id')
        )
        if not employee.name:
            return jsonify({'error': 'O campo name é obrigatório'}), 400
        if not employee.company_id != "":
            return jsonify({'error': 'O campo company é obrigatório'}), 400
        if employee.cpf != "":
            ald_employee = dao_employees.get_by_cpf(employee.cpf)
            if ald_employee != None:
                return jsonify({'error': 'Funcionário não encontrado'}), 400
            id = dao_employees.get_id_by_cpf(employee.cpf)
            new_employee = Employees(employee.name, employee.cpf, employee.roles_id, employee.company_id, id)
        return jsonify({'id': new_employee.id}), 201

    elif auth_response.status_code == 401:
        return jsonify({'error': 'Token de autenticação inválido'}), 401
    else:
        return make_response(auth_response.text, auth_response.status_code)


def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post('http://127.0.0.1:5000/api/v1/authentication/validation/', headers=headers)
    return response

