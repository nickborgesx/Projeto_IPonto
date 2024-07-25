from flask import Flask
from iponto.modules.company.controller import company_controller
from iponto.modules.employees.controller import employees_controller
from iponto.modules.roles.controller import roles_controller
from iponto.modules.scale.controller import scale_controller
from iponto.service.connect import Connect as EmployeeConnect
from iponto.service.connect import Connect as RolesConnect
from iponto.service.connect import Connect as CompanyConnect
from iponto.service.connect import Connect as ScaleConnect
from iponto.service.connect import Connect

app = Flask(__name__)
Connect().init_database()


app.register_blueprint(roles_controller)
app.register_blueprint(company_controller)
app.register_blueprint(employees_controller)
app.register_blueprint(scale_controller)

EmployeeConnect().create_table()
CompanyConnect().create_table()
RolesConnect().create_table()
ScaleConnect().create_table()

EmployeeConnect().init_database()
CompanyConnect().init_database()
RolesConnect().init_database()
ScaleConnect().init_database()

if __name__ == "__main__":
    app.run(debug=True, port=5001)
