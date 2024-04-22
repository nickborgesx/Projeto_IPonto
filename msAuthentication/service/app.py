from flask import Flask
from msAuthentication.modules.user.controller import user_controller
from msAuthentication.service.connect import Connect as UserConnect
from msAuthentication.service.connect import Connect

app = Flask(__name__)
Connect().init_database()
app.register_blueprint(user_controller)

UserConnect().create_table()
UserConnect().init_database()

if __name__ == "__main__":
    app.run(debug=True, port=5000)
