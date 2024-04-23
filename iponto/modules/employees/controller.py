import requests
from flask import Blueprint, request, jsonify, make_response
from flask import request as flask_request
from iponto.modules.employees.dao import DAOEmployees
from iponto.modules.employees.modelo import Employees
from iponto.modules.employees.sql import SQLEmployees
from iponto.modules.roles.dao import DAORoles

employees_controller = Blueprint('employees_controller', __name__)
dao_employees = DAOEmployees()
dao_roles = DAORoles
module_name = 'employees'
SECRET_KEY = 'chave_secreta'
@employees_controller.route(f'/api/v1/employees/', methods=['GET'])
def get_employees():
    payload = {
        "authorization": flask_request.headers.get('authorization')
    }
    response = requests.post(url='http://localhost:5000/api/v1/authorization/validation/', data=payload)

    if response.status_code == 200:
        func = DAOEmployees().get_all_employees()
        return jsonify({"response": func})
    elif response.status_code == 401:
        return make_response(jsonify({'erro': 'Usuário não autorizado'}), 401)
    else:
        return make_response(response.json(), response.status_code)

@employees_controller.route(f'/api/v1/employee/', methods=['POST'])
def create_employee():
    employee_data = request.json
    errors = []

    for campo in SQLEmployees._CAMPOS_OBRIGATORIOS:
        if campo not in employee_data or not str(employee_data.get(campo, '')).strip():
            errors.append(f'O campo {campo} é obrigatório!')

    if not employee_data.get('cpf', '').strip():
        errors.append('O campo CPF é obrigatório')

    if dao_employees.get_by_cpf(employee_data.get('cpf')):
        errors.append('Já existe um funcionário com esse CPF')

    if errors:
        response = jsonify({'error': errors})
        response.status_code = 400
        return response

    role_id = employee_data.get('roles_id')
    if not dao_roles().get_by_id(role_id):
        response = jsonify({'error': f'Não existe o cargo com ID {role_id} no sistema'})
        response.status_code = 400
        return response

    employee = Employees(**employee_data)
    employee_id = dao_employees.salvar(employee)

    response_data = {'id': employee_id, 'name': employee_data['name']}
    response = jsonify(response_data)
    response.status_code = 200
    return response



