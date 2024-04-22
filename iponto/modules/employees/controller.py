import requests
from flask import Blueprint, request, jsonify, make_response
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from iponto.modules.employees.dao import DAOEmployees
from iponto.modules.employees.modelo import Employees
from iponto.modules.employees.sql import SQLEmployees
from iponto.modules.roles.dao import DAORole

employees_controller = Blueprint('employees_controller', __name__)
dao_employees = DAOEmployees()
module_name = 'employees'

@employees_controller.route(f'/api/v1/employees/', methods=['GET'])
@jwt_required()
def employees():
    token = request.headers.get('Authorization')
    payload = {
        "token": token
    }
    response = requests.post(url='http://localhost:5000/api/v1/authentication/validation/', json=payload)
    if response.status_code == 200:
        employees = DAOEmployees.get_all_employees()
        return jsonify({"response": employees})
    elif response.status_code == 401:
        return make_response(jsonify({'error': 'Usuário não autorizado'}), 401)
    else:
        return make_response(response.json(), response.status_code)

@employees_controller.route('/api/v1/employee/', methods=['POST'])
def create_employee():
    data = request.json
    errors = []
    required_fields = ['nome', 'cpf', 'roles_id']
    for field in required_fields:
        if field not in data or not data[field].strip():
            errors.append(f'O campo {field} é obrigatório!')
    if dao_employees.get_by_cpf(data.get('cpf')):
        errors.append('Já existe um funcionário com esse documento!')
    title = data.get('roles_id')
    if not DAORole.get_by_title(title): #Erro acontece exatamente nessa parte
        errors.append('Não existe esse cargo no sistema!')
    if errors:
        response = jsonify({'errors': errors})
        response.status_code = 400
        return response
    employee_data = Employees(**data)
    employee_id = dao_employees.salvar(employee_data)
    response = jsonify({'id': employee_id})
    response.status_code = 200
    return response


