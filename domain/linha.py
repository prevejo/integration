from domain.entity import Entity


class Linha(Entity):

    def __init__(self, numero: 'numero', descricao: 'descricao', tarifa: 'tarifa'):
        super(Linha, self).__init__()
        self.numero = numero
        self.descricao = descricao
        self.tarifa = tarifa
        self.percursos = []

    def add_percurso(self, percurso):
        self.percursos.append(percurso)
