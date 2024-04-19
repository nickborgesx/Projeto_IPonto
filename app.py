import multiprocessing
import threading

from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
import requests
from iponto.modules.roles.controller import roles_controller
from iponto.modules.employees.controller import employees_controller
from msAuthentication.modules.user.controller import user_controller
from msAuthentication.service.connect import Connect as UserConnect
from iponto.service.connect import Connect as EmployeesConnect
from iponto.service.connect import Connect as RoleConnect

def check_api_status(url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            return True
    except Exception as e:
        print(f'Erro ao acessar o URL {url}: {e}')
    return False


appMSAuthentication = Flask(__name__)

appMSAuthentication.config['JWT_SECRET_KEY'] = 'chave_secreta'
appMSAuthentication.config['JWT_TOKEN_LOCATION'] = ['headers']
appMSAuthentication.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)
jwt = JWTManager(appMSAuthentication)
appMSAuthentication.register_blueprint(user_controller, url_prefix='/api/v1/authentication')

appIPonto = Flask(__name__)
appIPonto.register_blueprint(employees_controller, url_prefix='/api/v1/employees')
appIPonto.register_blueprint(roles_controller, url_prefix='/api/v1/roles')

UserConnect().create_table()
UserConnect().init_database()


RoleConnect().create_table()
RoleConnect().init_database()

EmployeesConnect().create_table()
EmployeesConnect().init_database()

def run_MSAuthentication():
    appMSAuthentication.run(port=5000 , debug=False)

def run_Iponto():
    appIPonto.run(port=5001 , debug=False)

if __name__ == "__main__":
    processMSAuthentication = multiprocessing.Process(target=run_MSAuthentication())
    processIponto = multiprocessing.Process(target=run_Iponto())

    processMSAuthentication.start()
    processIponto.start()

    processMSAuthentication.join()
    processIponto.join()

    apiMSAuthentication_url = 'http://127.0.0.1:5000'
    apiIPonto_url = 'http://127.0.0.1:5001'

    if check_api_status(apiMSAuthentication_url):
        print('API authentication conexão OK')
    else:
        print('API authentication conexão falhou')

    if check_api_status(apiIPonto_url):
        print('API Iponto conexão ok')
    else:
        print('API Iponto conexão falhou')