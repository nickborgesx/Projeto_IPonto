from iponto.modules.roles.sql import SQLRoles
from iponto.modules.roles.modelo import Roles
from msAuthentication.service.connect import Connect

class DAORoles(SQLRoles):
    def __init__(self):
        self.connection = Connect().get_instance()
    def create_table(self):
        return self._CREATE_TABLE

    def create_role(self, roles:Roles):
        if not isinstance(roles, Roles):
            raise Exception('Erro ao criar o role, tipo invalido')
        query = self._INSERT_ROLES
        cursor = self.connection.cursor()
        cursor.execute(query(roles.title,))
        self.connection.commit()
        return roles

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            cols = [desc[0] for desc in cursor.description]
            roles_dict = dict(zip(cols, result))
            return Roles(**roles_dict)
        else:
            return None

    def get_by_title(self, title):
        query = self._SELECT_BY_TITLE
        cursor = self.connection.cursor()
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        if result:
            cols = [desc[0] for desc in cursor.description]
            roles_dict = dict(zip(cols, result))
            return Roles(**roles_dict)
        else:
            return None
