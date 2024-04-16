from flask import Flask
from flask_jwt_extended import JWTManager, jwt_required, get_jwt_identity
from datetime import timedelta
from employees.modules.employees.controller import employees_controller
from employees.modules.roles.controller import role_controller
from employees.service.connect import Connect as EmployeesConnect
from msAuthentication.modules.auth import auth_blueprint
from msAuthentication.service.connect import Connect as AuthConnect

app = Flask(__name__)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'chave_secreta'

app.config['JWT_TOKEN_LOCATION'] = ['headers']


app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)


app.register_blueprint(employees_controller)
app.register_blueprint(role_controller)
app.register_blueprint(auth_blueprint)


EmployeesConnect().create_table()
EmployeesConnect().init_database()

AuthConnect().create_table()
AuthConnect().init_database()

if __name__ == "__main__":
    app.run(debug=True)
