from flask import Blueprint, request, jsonify
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
def get_employeess():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        dao_employees = DAOEmployees()
        query = f"{DAOEmployees._SELECT_ALL} WHERE {DAOEmployees._COL_USERNAME} = %s"
        params = (current_user,)
        with dao_employees.connection.cursor() as cursor:
            cursor.execute(query, params)
            results = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            employeess = [Employees(**dict(zip(cols, i))) for i in results]
            for employee in employeess:
                roles = DAORole().get_by_id(employee.roles_id)
                if roles:
                    employee.roles_id = roles.__dict__
            results = [{"id": employee.id, "name": employee.name, "role": employee.roles_id} for employee in employeess]
            if results:
                response = jsonify(response=results)
                response.status_code = 200
            else:
                response = jsonify({'error': 'Nenhum funcionário encontrado.'})
                response.status_code = 400
            return response
    except Exception as e:
        return jsonify({'error': 'Token inválido'}), 400

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
