from flask import Blueprint, request, jsonify
from employees.modules.roles.dao import DAORole
from employees.modules.roles.modelo import Role

role_controller = Blueprint('role_controller', __name__)
dao_role = DAORole()
module_name = 'roles'
