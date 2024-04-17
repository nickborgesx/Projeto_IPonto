from flask import Blueprint, request, jsonify
from flask_jwt_extended import jwt_required, get_jwt_identity, verify_jwt_in_request, get_jwt
from iponto.modules.employees.dao import DAOEmployees
from iponto.modules.employees.modelo import Employees
from iponto.modules.roles.dao import DAORole
import requests

employees_controller = Blueprint('users_controller', __name__)
dao_employees = DAOEmployees()
module_name = 'iponto'

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

#@employees_controller.route('/api/v1/employeesx/', methods=['GET'])
#@jwt_required()
#def get_employeesx():
#    current_user = get_jwt_identity()
#    dao_employees = DAOEmployees()
#    iponto = dao_employees.get_employees_by_user_id(current_user)
#    if iponto:
#        employees_data = [{"id": employee.id, "name": employee.name, "role": employee.role} for employee in iponto]
#        return jsonify(response=employees_data), 200
#    else:
#        return jsonify({'error': 'Nenhum funcionário encontrado'}), 400

@employees_controller.route('/api/v1/employeesx/', methods=['GET'])
def get_employeesx():
    token = request.headers.get("Authorization")

    auth_api_url = "http://127.0.0.1:5000/api/v1/authentication/validation/"
    auth_response = requests.post(auth_api_url, json={"token": token})

    if auth_response.status_code == 200:
        response_data = auth_response.json()
        if "user_info" in response_data:
            user_info = response_data["user_info"]
            dao_employees = DAOEmployees()
            employees = dao_employees.get_employees_by_user_id(user_info["username"])
            if employees:
                employees_data = [{"id": employee.id, "name": employee.name, "role": employee.role} for employee in employees]
                return jsonify(response=employees_data), 200
            else:
                return jsonify({'error': 'Nenhum funcionário encontrado'}), 400
        else:
            return jsonify({'error': 'Informações do usuário não encontradas na resposta da API de Autenticação'}), 400
    else:
        return jsonify({'error': 'Erro na validação do token JWT'}), auth_response.status_code
