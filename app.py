from flask import Flask
from flask_jwt_extended import JWTManager
from datetime import timedelta
from msAuthentication.modules.user.controller import user_controller
from msAuthentication.service.connect import Connect as UserConnect

app = Flask(__name__)

app.config['JWT_SECRET_KEY'] = 'chave_secreta'
app.config['JWT_TOKEN_LOCATION'] = ['headers']
app.config['JWT_ACCESS_TOKEN_EXPIRES'] = timedelta(hours=1)

jwt = JWTManager(app)

app.register_blueprint(user_controller)

UserConnect().create_table()
UserConnect().init_database()

if __name__ == "__main__":
    app.run(host='127.0.0.1', port=5000)


