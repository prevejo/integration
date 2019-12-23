from domain.entity import Entity


class Parada(Entity):

    def __init__(self, cod: 'cod', geo: 'geo', geo_via: 'geo_via'):
        super(Parada, self).__init__()
        self.cod = cod
        self.geo = geo
        self.geo_via = geo_via
