import requests
from flask import Blueprint, request, jsonify, make_response
from flask import request as flask_request
from datetime import datetime, timedelta
from iponto.modules.scale.dao import DAOScale
from iponto.modules.scale.modelo import Scale
from iponto.modules.employees.dao import DAOEmployees

scale_controller = Blueprint('scale_controller', __name__)
dao_scale = DAOScale()
dao_employees = DAOEmployees()


def validate_token(token):
    headers = {'Authorization': token}
    response = requests.post('http://127.0.0.1:5000/api/v1/authentication/validation/', headers=headers)
    return response

def generate_work_days(year, month):
    first_day = datetime(year, month, 1)
    if month == 12:
        next_month = datetime(year + 1, 1, 1)
    else:
        next_month = datetime(year, month + 1, 1)
    days_in_month = (next_month - first_day).days
    work_days = [first_day + timedelta(days=i) for i in range(days_in_month) if (first_day + timedelta(days=i)).weekday() < 5]
    return work_days


@scale_controller.route('/api/v1/scale/', methods=['POST'])
def create_scale():
    token = flask_request.headers.get('Authorization')
    auth_response = validate_token(token)
    if auth_response.status_code == 200:
        scale_data = request.json
        errors = []

        for campo in ['type', 'employee_id', 'month', 'year']:
            if campo not in scale_data or not str(scale_data.get(campo, '')).strip():
                errors.append(f'O campo {campo} é obrigatório!')

        if errors:
            response = jsonify({'error': errors})
            response.status_code = 400
            return response

        employee_ids = scale_data.get('employee_id')
        if not isinstance(employee_ids, list):
            response = jsonify({'error': 'O campo employee_id deve ser uma lista de IDs'})
            response.status_code = 400
            return response

        month = scale_data.get('month')
        year = scale_data.get('year')

        created_ids = set()
        existing_ids = []

        for employee_id in employee_ids:
            if not dao_employees.get_by_id(employee_id):
                response = jsonify({'error': f'Funcionário com ID {employee_id} não existe no sistema'})
                response.status_code = 400
                return response

        work_days = generate_work_days(year, month)
        for employee_id in employee_ids:
            existing_scale = dao_scale.get_by_employee_and_date(employee_id, month, year)
            if existing_scale:
                existing_ids.append(employee_id)
                continue

            for day in work_days:
                new_scale = Scale(
                    type=scale_data.get('type'),
                    month=month,
                    year=year,
                    date=day.strftime('%Y-%m-%d'),
                    morning_break='8-12',
                    afternoon_break='13-17',
                    night_break='19-23',
                    employee_id=employee_id,
                    input1=None,
                    exit1=None,
                    input2=None,
                    exit2=None
                )
                saved_scale = dao_scale.salvar(new_scale)
                created_ids.add(employee_id)

        response_data = {
            'created_ids': list(created_ids),
            'existing_ids': existing_ids,
            'message': {
                'created': f'Escalas criadas para os funcionários com IDs: {", ".join(map(str, created_ids))}' if created_ids else '',
                'existing': f'Escalas já existem para os funcionários com IDs: {", ".join(map(str, existing_ids))}' if existing_ids else ''
            }
        }
        response = jsonify(response_data)
        response.status_code = 201
        return response

    elif auth_response.status_code == 401:
        return make_response(jsonify({'error': 'Token de autenticação inválido'}), 401)
    else:
        return make_response(auth_response.text, auth_response.status_code)

