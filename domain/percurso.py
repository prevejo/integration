from domain.entity import Entity


class Percurso(Entity):

    def __init__(self, numero: 'numero', sentido: 'sentido', origem: 'origem', destino: 'destino', geo: 'geo'):
        super(Percurso, self).__init__()
        self.numero = numero
        self.sentido = sentido
        self.origem = origem
        self.destino = destino
        self.geo = geo
        self.paradas = []

    def add_parada(self, parada):
        self.paradas.append(parada)
