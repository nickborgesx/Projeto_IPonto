from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from iponto.modules.controller import employees_controller
from iponto.service.connect import Connect as EmployeesConnect
from msAuthentication.modules.auth import auth_blueprint
from msAuthentication.service.connect import Connect as AuthConnect

app = Flask(__name__)
jwt = JWTManager(app)

app.config['JWT_SECRET_KEY'] = 'chave_secreta'

app.config['JWT_TOKEN_LOCATION'] = ['headers']


app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)


app.register_blueprint(employees_controller)
app.register_blueprint(auth_blueprint)


EmployeesConnect().create_table()
EmployeesConnect().init_database()

AuthConnect().create_table()
AuthConnect().init_database()

if __name__ == "__main__":
    app.run(debug=True)
