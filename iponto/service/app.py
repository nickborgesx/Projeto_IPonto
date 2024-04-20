from flask import Flask
from iponto.modules.employees.controller import employees_controller
from iponto.modules.roles.controller import roles_controller
from iponto.service.connect import Connect as EmployeeConnect
from iponto.service.connect import Connect as RoleConnect
from iponto.service.connect import Connect

app = Flask(__name__)
Connect().init_database()

app.register_blueprint(roles_controller)
app.register_blueprint(employees_controller)

EmployeeConnect().create_table()
RoleConnect().create_table()

EmployeeConnect().init_database()
RoleConnect().init_database()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
