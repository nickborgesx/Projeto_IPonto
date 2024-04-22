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

@employees_controller.route(f'/api/v1/employee/', methods=['POST'])
@jwt_required()
def create_employee():
    employee = request.json
    erros = []
    for data in employee:
        for campo in SQLEmployees._CAMPOS_OBRIGATORIOS:
            if campo not in data.keys() or not data.get(campo, '').strip():
                erros.append(f'O campo {campo} é pbrigatório!')
            if not data.get('cpf', '').strip():
                erros.append(f'O campo cpf é obrigatorio')
        if dao_employees.get_by_cpf(data.get('cpf')):
            erros.append(f'Já existe um funcionário com esse documento')
        if erros:
            response = jsonify({'error': erros})
            response.status_code = 400
            return response
        title = data.get('titulo')
        isTitle = DAORole.get_by_title(title)
        if not isTitle:
            response = jsonify({'error': 'Não existe esse cargo no sistema'})
            response.status_code = 400
            return response
        employee_dado = Employees(**data)
        id = dao_employees.salvar(employee_dado)
    response = jsonify({'id': id })
    response.status_code = 200
