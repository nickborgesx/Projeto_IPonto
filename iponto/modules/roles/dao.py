from iponto.modules.roles.sql import SQLRole
from iponto.modules.roles.modelo import Role

class DAORole(SQLRole):
    def __init__(self):
        from iponto.service.connect import Connect
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

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
