from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request
from employees.modules.employees.dao import DAOEmployees
from employees.modules.employees.modelo import Employees
from employees.modules.roles.controller import dao_role

employees_controller = Blueprint('users_controller', __name__)
dao_employees = DAOEmployees()
module_name = 'employees'

@employees_controller.route(f'/api/v1/employees/', methods=['GET'])
@jwt_required()
def get_employeess():
    try:
        verify_jwt_in_request()
        current_user = get_jwt_identity()
        dao_employees = DAOEmployees()
        query = DAOEmployees._SELECT_ALL
        with dao_employees.connection.cursor() as cursor:
            cursor.execute(query)
            results = cursor.fetchall()
            cols = [desc[0] for desc in cursor.description]
            employeess = [Employees(**dict(zip(cols, i))) for i in results]
            for employee in employeess:
                roles = dao_role.get_by_id(employee.roles_id)
                if roles:
                    employee.roles_id = roles.__dict__
            results = [{"id": employee.id, "name": employee.name, "role": employee.roles_id} for employee in employeess]
            if results:
                response = jsonify(response=results)
                response.status_code = 200
            else:
                response = jsonify({'error': 'Nenhum funcionario encontrado.'})
                response.status_code = 400  # Mudança de status para 400 conforme especificado
            return response
    except Exception as e:
        return jsonify({'error': 'Token inválido'}), 400