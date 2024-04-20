import psycopg2
from msAuthentication.modules.user.sql import SQLUser


class Connect:
    def __init__(self):
        config = dict(dbname="authentication",
                      user="postgres",
                      #password="redgaw",
                      password="1532",
                      host="localhost", port="5432")
        self._connection = psycopg2.connect(**config)

    def create_table(self):
        from msAuthentication.modules.user.dao import DAOUser
        cursor = self._connection.cursor()
        cursor.execute(DAOUser().create_table())
        self._connection.commit()
        cursor.close()

    def get_instance(self):
        return self._connection

    def init_database(self):
        cursor = self._connection.cursor()
        cursor.execute(SQLUser._CREATE_TABLE)
        self._connection.commit()
        cursor.close()

