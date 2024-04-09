import psycopg2
class Connect:
    def __init__(self):
        config = dict(
            dbname="PBD_2024",
            user="postgres", password="1532",
            host="localhost", port="5432"
        )
        self._connection = psycopg2.connect(**config)

    def create_tables(self):
        cursor = self._connection.cursor()
        from modules.users.dao import DAOUsers
        cursor.execute(DAOUsers().create_table())

        self._connection.commit()
        cursor.close()

    def get_instance(self):
        return self._connection

    def init_database(self, version='v1'):
        if version == 'v1':
            self.create_tables()
        if version == 'v2':
            self.update_database()

    def update_database(self):
        pass