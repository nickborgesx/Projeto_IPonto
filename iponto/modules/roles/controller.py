import flask
from iponto.modules.roles.dao import DAORole

roles_controller = flask.Blueprint('role_controller', __name__)
dao_role = DAORole()
module_name = 'role'