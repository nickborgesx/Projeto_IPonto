from flask import Blueprint, request, jsonify
from modules.users.dao import DAOUsers

users_controller = Blueprint('users_controller', __name__)
dao_users = DAOUsers()
module_name = 'users'