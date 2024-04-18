from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from iponto.modules.roles.controller import roles_controller
from iponto.modules.employees.controller import employees_controller
from msAuthentication.modules.user.controller import user_controller
from msAuthentication.service.connect import Connect as UserConnect
from iponto.service.connect import Connect as EmployeesConnect
from iponto.service.connect import Connect as RoleConnect

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'chave_secreta'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

app.register_blueprint(user_controller, url_prefix='/api/v1/authentication')
app.register_blueprint(employees_controller, url_prefix='/api/v1/employees')
app.register_blueprint(roles_controller, url_prefix='/api/v1/roles')

UserConnect().create_table()
UserConnect().init_database()

RoleConnect().create_table()
RoleConnect().init_database()

EmployeesConnect().create_table()
EmployeesConnect().init_database()

if __name__ == "__main__":
    app.run(debug=False)
