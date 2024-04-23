from msAuthentication.modules.user.modelo import User
from msAuthentication.modules.user.sql import SQLUser
from msAuthentication.service.connect import Connect


class DAOUser(SQLUser):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def verify_credentials(self, username, password):
        query = self._USERS_VALID
        cursor = self.connection.cursor()
        cursor.execute(query, (username, password))
        user_data = cursor.fetchone()
        cursor.close()
        if user_data:
            return User(*user_data)
        else:
            return None

    def verify_password(self, password):
        query = self._PASS_VALID
        cursor = self.connection.cursor()
        cursor.execute(query, (password,))
        return cursor.fetchone() is not None

    def user_name(self, username):
        query = self._USER_NAME
        cursor = self.connection.cursor()
        cursor.execute(query, (username,))
        return cursor.fetchone() is not None