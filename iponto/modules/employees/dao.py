from iponto.modules.employees.modelo import Employees
from iponto.modules.employees.sql import SQLEmployees
from iponto.service.connect import Connect


class DAOEmployees(SQLEmployees):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, employees: Employees):
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (employees.name, employees.cpf, employees.roles_id, employees.company_id))
        employee_id = cursor.fetchone()[0]
        employees.id = employee_id
        self.connection.commit()
        return employees

    def get_all_employees(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Employees(**i) for i in results]
        return results

    def get_by_cpf(self, cpf):
        query = self._SELECT_BY_CPF
        cursor = self.connection.cursor()
        cursor.execute(query, (cpf,))
        results = cursor.fetchall()
        if results:
            cols = [desc[0] for desc in cursor.description ]
            results = [dict(zip(cols,i)) for i in results]
            results = [Employees(**i) for i in results]
            return results
        else:
            return None

    def get_id_by_cpf(self, cpf):
        query = self._SELECT_ID_BY_CPF
        cursor = self.connection.cursor()
        cursor.execute(query, (cpf,))
        results = cursor.fetchone()
        if results:
            return results[0]
        else:
            return None

    def update_employees(self, employees: Employees):
        if not isinstance(employees, Employees):
            raise Exception('Tipo inválido')
        query = self._UPDATE_EMPLOYEE
        cursor = self.connection.cursor()
        cursor.execute(query, (employees.name, employees.cpf, employees.roles_id, employees.company_id, employees.id))
        self.connection.commit()
        return employees

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        results = cursor.fetchone()
        if results:
            cols = [desc[0] for desc in cursor.description]
            employees_dict = dict(zip(cols, results))
            return Employees(**employees_dict)
        else:
            return None


