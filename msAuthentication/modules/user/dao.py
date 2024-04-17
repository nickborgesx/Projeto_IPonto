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
        result = cursor.fetchone()
        cursor.close()
        return result is not None