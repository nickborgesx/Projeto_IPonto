from iponto.modules.employees.modelo import Employees
from iponto.modules.employees.sql import SQLEmployees
from iponto.service.connect import Connect

class DAOEmployees(SQLEmployees):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, employees:Employees):
        if not isinstance(Employees, Employees):
            raise Exception("Erro ao salvar tipo invalido")
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query,(employees.username, employees.password))
        self.connection.commit()
        return employees

    def get_user_name(self, name):
        query = self._SELECT_USER_NAME
        cursor = self.connection.cursor()
        cursor.execute(query, ('%'+name+'%',))
        results = cursor.fetchall()
        if results:
            cols = [desc[0] for desc in cursor.description]
            results = [dict(zip(cols, i)) for i in results]
            return results
        else:
            return None

    def get_employees_by_user_id(self, user_id):
        query = self._SELECT_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (user_id,))
        results = cursor.fetchall()
        if results:
            cols = [desc[0] for desc in cursor.description]
            results = [dict(zip(cols, i)) for i in results]
            return results
        else:
            return None

    def verify_credentials(self, username, password):
        query = self._USERS_VALID
        cursor = self.connection.cursor()
        cursor.execute(query, (username, password))
        result = cursor.fetchone()
        cursor.close()
        return result is not None

    def get_all_employees(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Employees(**i) for i in results]
        return results
