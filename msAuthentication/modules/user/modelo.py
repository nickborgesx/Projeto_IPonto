class User:
    def __init__(self, username, password, id=None):
        self.username = username
        self.password = password
        self.id = id

    def get_json(self):
        return {
            'id': self.id,
            'username': self.username,
            'password': self.password
        }
