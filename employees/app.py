from flask import Flask
from employees.modules.roles.controller import role_controller
from employees.modules.employees.controller import employees_controller
from employees.service.connect import Connect

app = Flask(__name__)
app.register_blueprint(role_controller)
app.register_blueprint(employees_controller)


Connect().create_table()
Connect().init_database()

if __name__ == "__main__":
    app.run(debug=True)
