class Roles:
    def __init__(self, title, id=None):
        self.title = title
        self.id = id

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title
        }