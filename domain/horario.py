from domain.entity import Entity


class Horario(Entity):

    def __init__(self, horario: 'horario'):
        super(Horario, self).__init__()
        self.horario = horario
