from flask import Blueprint, request, jsonify
from employees.modules.employees.dao import DAOEmployees
from employees.modules.employees.modelo import Employees
from employees.modules.roles.controller import dao_role

employees_controller = Blueprint('users_controller', __name__)
dao_employees = DAOEmployees()
module_name = 'employees'

@employees_controller.route(f'/api/v1/employees/', methods=['GET']) #Arrumar para POST dps
def get_employeess():
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
        results = [{"id": employee.id, "name": employee.name, "roles": employee.roles_id} for employee in employeess]
        if results:
            response = jsonify(results)
            response.status_code = 200
        else:
            response = jsonify('Nenhum funcionario encontrado.')
            response.status_code = 404
        return response

