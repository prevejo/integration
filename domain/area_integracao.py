from domain.entity import Entity


class AreaIntegracao(Entity):

    def __init__(self, descricao: 'descricao', geo: 'geo'):
        super(AreaIntegracao, self).__init__()
        self.descricao = descricao
        self.geo = geo
        self.paradas = []

    def add_parada(self, parada):
        self.paradas.append(parada)
