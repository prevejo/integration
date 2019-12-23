from domain.entity import Entity


class Operador(Entity):

    def __init__(self, descricao: 'descricao'):
        super(Operador, self).__init__()
        self.descricao = descricao
