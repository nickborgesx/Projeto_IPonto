from flask import Flask
from flask_jwt_extended import JWTManager
from msAuthentication.modules.auth import auth_blueprint
from msAuthentication.service.connect import Connect

app = Flask(__name__)
app.register_blueprint(auth_blueprint)

app.config['JWT_SECRET_KEY'] = 'chave_secreta'
jwt = JWTManager(app)

Connect().create_table()
Connect().init_database()

if __name__ == "__main__":
    app.run(debug=True)