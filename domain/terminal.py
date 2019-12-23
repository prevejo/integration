from domain.entity import Entity


class Terminal(Entity):

    def __init__(self, cod: 'cod', descricao: 'descricao', geo: 'geo', geo_centroid: 'geo_centroid'):
        super(Terminal, self).__init__()
        self.cod = cod
        self.descricao = descricao
        self.geo = geo
        self.geo_centroid = geo_centroid
        self.parada = None

    def set_parada(self, parada):
        self.parada = parada
