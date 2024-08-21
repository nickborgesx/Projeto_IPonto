import requests
from datetime import datetime, timedelta
from flask import Blueprint, request, jsonify, make_response
from flask import request as flask_request
from iponto.modules.company.dao import DAOCompany
from iponto.modules.employees.dao import DAOEmployees
from iponto.modules.employees.modelo import Employees
from iponto.modules.employees.sql import SQLEmployees
from iponto.modules.roles.dao import DAORoles
from iponto.modules.scale.controller import dao_scale
from iponto.modules.scale.dao import DAOScale

employees_controller = Blueprint('employees_controller', __name__)
dao_employees = DAOEmployees()
dao_scale = DAOScale()
dao_roles = DAORoles()
dao_company = DAOCompany()
module_name = 'employees'
SECRET_KEY = 'chave_secreta'

def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post('http://127.0.0.1:5000/api/v1/authentication/validation/', headers=headers)
    return response

@employees_controller.route('/api/v1/employees/', methods=['GET'])
def get_employees():
    token = flask_request.headers.get('Authorization')
    auth_response = validate_token(token)

    if auth_response.status_code == 200:
        employees = dao_employees.get_all_employees()
        employees_data = []
        for employee in employees:
            employee_data = {
                "id": employee.id,
                "name": employee.name,
                "cpf": employee.cpf,
                "role": None,
                "company": None
            }

            company = dao_company.get_by_id(employee.company_id)
            if company:
                employee_data["company"] = {
                    "id": company.id,
                    "name": company.name
                }

            role = dao_roles.get_by_id(employee.roles_id)
            if role:
                employee_data["role"] = {
                    "id": role.id,
                    "title": role.title
                }

            employees_data.append(employee_data)
        return jsonify({"employees": employees_data}), 200
    elif auth_response.status_code == 401:
        return make_response(jsonify({'error': 'Token de autenticação inválido'}), 401)
    else:
        return make_response(auth_response.text, auth_response.status_code)

@employees_controller.route(f'/api/v1/employee/', methods=['POST'])
def create_employee():
    token = flask_request.headers.get('Authorization')
    auth_response = validate_token(token)
    if auth_response.status_code == 200:
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
        if not dao_roles.get_by_id(role_id):
            response = jsonify({'error': f'Não existe o cargo com ID {role_id} no sistema'})
            response.status_code = 400
            return response

        company_id = employee_data.get('company_id')
        if not dao_company.get_by_id(company_id):
            response = jsonify({'error': f'Não existe uma empresa com o ID {company_id} no sistema'})
            response.status_code = 400
            return response

        new_employee = Employees(
            name=employee_data.get('name'),
            cpf=employee_data.get('cpf'),
            roles_id=role_id,
            company_id=company_id
        )
        saved_employee = dao_employees.salvar(new_employee)
        response = jsonify({'id': saved_employee.id})
        response.status_code = 201
        return response

    elif auth_response.status_code == 401:
        return make_response(jsonify({'error': 'Token de autenticação inválido'}), 401)
    else:
        return make_response(auth_response.text, auth_response.status_code)

@employees_controller.route('/api/v1/employee/<int:id>/', methods=['PUT'])
def editar_funcionario(id):
    if not id:
        response = jsonify({"error": "ID errado ou não fornecido"})
        response.status_code = 400
        return response
    validar_id = dao_employees.get_by_id(id)
    if not validar_id:
        response = jsonify({"message": f"Funcionário com o ID {id} não encontrado"})
        return response

    global new_employee
    token = request.headers.get('Authorization')
    auth_response = validate_token(token)

    if auth_response.status_code == 200:
        data = request.json
        employee = Employees(
            name=data.get('name'),
            cpf=data.get('cpf'),
            roles_id=data.get('roles_id'),
            company_id=data.get('company_id')
        )
        required_fields = ['name', 'cpf']
        missing_fields = [field for field in required_fields if field not in data]
        if missing_fields:
            return jsonify({'error': f'Os campos {", ".join(missing_fields)} são obrigatórios'}), 400

        role_id = data.get('roles_id')
        if not dao_roles.get_by_id(role_id):
            response = jsonify({'error': f'Não existe o cargo com ID {role_id} no sistema'})
            response.status_code = 400
            return response

        company_id = data.get('company_id')
        if not dao_company.get_by_id(company_id):
            response = jsonify({'error': f'Não existe uma empresa com o ID {company_id} no sistema'})
            response.status_code = 400
            return response

        if employee.name == "":
            response = jsonify({'error': f'Nome não inserido'})
            response.status_code = 400
            return response


        if employee.cpf != "":
            old_employee = dao_employees.get_by_cpf(employee.cpf)
            if old_employee != None:
                id = dao_employees.get_id_by_cpf(employee.cpf)
                new_employee = Employees(employee.name, employee.cpf, employee.roles_id, employee.company_id, id)
                saved_employee = dao_employees.update_employees(new_employee)
                return jsonify({'id': saved_employee.id}), 201
            return jsonify({'error': 'Funcionário não encontrado'}), 400

    elif auth_response.status_code == 401:
        return jsonify({'error': 'Token de autenticação inválido'}), 401
    else:
        return make_response(auth_response.text, auth_response.status_code)

INTERVALO = True
@employees_controller.route('/api/v1/employee/<int:id>/point', methods=['POST'])
def bater_ponto(id):
    token = request.headers.get('Authorization')
    auth_response = validate_token(token)
    if auth_response.status_code == 200:
        employee_id = id
        # Captura automaticamente a data e hora local
        data_e_hora_atual = datetime.now()
        date_hoje = data_e_hora_atual.date().isoformat()
        hora_atual = data_e_hora_atual.strftime("%H:%M")

    # Verifica se há uma escala para o funcionário na data atual
        verificar_data = dao_scale.get_data_by_data_and_id(employee_id, date_hoje)
        input1 = verificar_data.get('input1')
        exit1 = verificar_data.get('exit1')
        input2 = verificar_data.get('input2')
        exit2 = verificar_data.get('exit2')
        if input1 and input2 and exit1 and exit2 != None :
            return make_response({'error': 'Limite do dia já atingido'}, 400)
        if verificar_data:
            if verificar_data.get('input1') == None:
                input1 = hora_atual
                check_in = dao_scale.update_input1(input1=input1, data=date_hoje, employee_id=employee_id)
                return jsonify(f'check-in = {check_in}'),200
            elif verificar_data.get('exit1') == None:
                input1 = verificar_data.get('input1')
                ultima_hora = datetime.strptime(input1, '%H:%M')
                atual_hora = datetime.strptime(hora_atual, '%H:%M')
                if atual_hora < (ultima_hora + timedelta(hours=1)):
                    return jsonify({"error": "Você não pode bater o ponto nesse momento, precisa de um intervalo de 1h entre os pontos"}), 400
                check_out = dao_scale.update_exit1(exit1=hora_atual, data=date_hoje, employee_id=employee_id)
                return jsonify(f'check-out = {check_out} '),200

            elif verificar_data.get('input2') == None:
                input2 = hora_atual
                check_in = dao_scale.update_input2(input2=input2, data=date_hoje, employee_id=employee_id)
                return jsonify(f'check-in = {check_in}'),200
            elif verificar_data.get('exit2') == None:
                input2 = verificar_data.get('input2')
                ultima_hora = datetime.strptime(input2, '%H:%M')
                atual_hora = datetime.strptime(hora_atual, '%H:%M')
                if atual_hora < (ultima_hora + timedelta(hours=1)):
                    return jsonify({"error": "Você não pode bater o ponto nesse momento, precisa de um intervalo de 1h entre os pontos"}), 400
                check_out = dao_scale.update_exit2(exit2=hora_atual, data=date_hoje, employee_id=employee_id)
                return jsonify(f'check-out = {check_out} '),200
        return jsonify({"error": f"Não existe escala definida para o dia {date_hoje} para o funcionário {id}"}), 400
    elif auth_response.status_code == 401:
        return jsonify({'error': 'Token de autenticação inválido'}), 401
    else:
        return make_response(auth_response.text, auth_response.status_code)


