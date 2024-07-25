import psycopg2
from iponto.modules.company.sql import SQLCompany
from iponto.modules.employees.sql import SQLEmployees
from iponto.modules.roles.sql import SQLRoles
from iponto.modules.scale.sql import SQLScale


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
        from iponto.modules.roles.dao import DAORoles
        from iponto.modules.company.dao import DAOCompany
        from iponto.modules.scale.dao import DAOScale
        cursor = self._connection.cursor()
        cursor.execute(DAORoles().create_table())
        cursor.execute(DAOCompany().create_table())
        cursor.execute(DAOEmployees().create_table())
        cursor.execute(DAOScale().create_table())
        self._connection.commit()
        cursor.close()

    def get_instance(self):
        return self._connection

    def init_database(self):
        cursor = self._connection.cursor()
        cursor.execute(SQLRoles._CREATE_TABLE)
        cursor.execute(SQLCompany._CREATE_TABLE)
        cursor.execute(SQLEmployees._CREATE_TABLE)
        cursor.execute(SQLScale._CREATE_TABLE)
        self._connection.commit()
        cursor.close()
