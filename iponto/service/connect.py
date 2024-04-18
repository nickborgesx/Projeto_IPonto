import psycopg2

class Connect:
    def __init__(self):
        config = dict(dbname="iponto",
                      user="postgres", password="1532",
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

    def init_database(self, version='v1'):
        if version == 'v1':
            self.create_table()
        if version == 'v2':
            self.update_database()

    def update_database(self):
        pass
