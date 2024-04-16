class Employees():
    def __init__(self, name, username, password, roles_id, id=None):
        self.id = id
        self.name = name
        self.username = username
        self.password = password
        self.roles_id = roles_id
