from iponto.modules.roles.sql import SQLRole
from iponto.modules.roles.modelo import Role
from msAuthentication.service.connect import Connect

class DAORole(SQLRole):
    def __init__(self):
        self.connection = Connect().get_instance()
    def create_table(self):
        return self._CREATE_TABLE

    def create_role(self, role:Role):
        if not isinstance(role, Role):
            raise Exception('Erro ao criar o role, tipo invalido')
        query = self._INSERT_ROLE
        cursor = self.connection.cursor()
        cursor.execute(query(role.title,))
        self.connection.commit()
        return role

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            cols = [desc[0] for desc in cursor.description]
            quarto_dict = dict(zip(cols, result))
            return Role(**quarto_dict)
        else:
            return None

    def get_by_title(self, title):
        query = self._SELECT_BY_TITLE
        cursor = self.connection.cursor()
        cursor.execute(query, (title,))
        result = cursor.fetchone()
        if result:
            cols = [desc[0] for desc in cursor.description]
            quarto_dict = dict(zip(cols, result))
            return Role(**quarto_dict)
        else:
            return None
