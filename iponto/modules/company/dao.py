from iponto.modules.company.modelo import Company
from iponto.modules.company.sql import SQLCompany
from iponto.service.connect import Connect


class DAOCompany(SQLCompany):
    def __init__(self):
        self.connection = Connect().get_instance()

    def create_table(self):
        return self._CREATE_TABLE

    def salvar(self, company: Company):
        query = self._INSERT_INTO
        cursor = self.connection.cursor()
        cursor.execute(query, (company.name, company.cnpj, company.lat, company.lng,))
        company_id = cursor.fetchone()[0]
        company.id = company_id
        self.connection.commit()
        return company

    def get_all_company(self):
        query = self._SELECT_ALL
        cursor = self.connection.cursor()
        cursor.execute(query)
        results = cursor.fetchall()
        cols = [desc[0] for desc in cursor.description]
        results = [dict(zip(cols, i)) for i in results]
        results = [Company(**i) for i in results]
        return results

    def get_by_cnpj(self, cnpj):
        query = self._SELECT_BY_CNPJ
        cursor = self.connection.cursor()
        cursor.execute(query, (cnpj,))
        results = cursor.fetchall()
        if results:
            cols = [desc[0] for desc in cursor.description ]
            results = [dict(zip(cols,i)) for i in results]
            results = [Company(**i) for i in results]
            return results
        else:
            return None

    def get_by_id(self, id):
        query = self._SELECT_BY_ID
        cursor = self.connection.cursor()
        cursor.execute(query, (id,))
        result = cursor.fetchone()
        if result:
            cols = [desc[0] for desc in cursor.description]
            roles_dict = dict(zip(cols, result))
            return Company(**roles_dict)
        else:
            return None

