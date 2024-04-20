import psycopg2
from iponto.modules.employees.sql import SQLEmployees
from iponto.modules.roles.sql import SQLRole


class Connect:
    def __init__(self):
        config = dict(dbname="iponto",
                      user="postgres",
                      # password="redgaw",
                      password="1532",
                      host="localhost", port="5432")
        self._connection = psycopg2.connect(**config)

    def create_table(self):
        from iponto.modules.employees.dao import DAOEmployees
        from iponto.modules.roles.dao import DAORole
        cursor = self._connection.cursor()
        cursor.execute(DAORole().create_table())
        cursor.execute(DAOEmployees().create_table())
        self._connection.commit()
        cursor.close()

    def get_instance(self):
        return self._connection

    def init_database(self):
       cursor = self._connection.cursor()
       cursor.execute(SQLEmployees().CREATE_TABLE)
       cursor.execute(SQLRole().CREATE_TABLE)
       self._connection.commit()
       cursor.close()

