class Employees():
    def __init__(self, name, cpf, roles_id, id=None):
        self.id = id
        self.name = name
        self.cpf = cpf
        self.roles_id = roles_id

    def get_json(self):
        return {
            'id': self.id,
            'name': self.name,
            'cpf': self.cpf,
            'roles_id': self.roles_id
        }