class Company:
    def __init__(self, name, cnpj, lat, lng, id=None):
        self.id = id
        self.name = name
        self.cnpj = cnpj
        self.lat = lat
        self.lng = lng
