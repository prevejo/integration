from domain.entity import Entity
from domain.horario import Horario


class Operacao(Entity):

    def __init__(self, segunda: 'segunda', terca: 'terca', quarta: 'quarta', quinta: 'quinta', sexta: 'sexta', sabado: 'sabado', domingo: 'domingo'):
        super(Operacao, self).__init__()
        self.segunda = segunda == 'S'
        self.terca = terca == 'S'
        self.quarta = quarta == 'S'
        self.quinta = quinta == 'S'
        self.sexta = sexta == 'S'
        self.sabado = sabado == 'S'
        self.domingo = domingo == 'S'
        self.horarios = []
        self.percurso = None
        self.operador = None

    def set_horarios(self, horarios):
        horarios = [('0' * (4 - len(h))) + h if len(h) < 4 else h for h in horarios.split(',')]
        horarios = [('00' if h[:2] == '24' else h[:2], h[2:]) for h in horarios]
        horarios = [h[0] + ':' + h[1] for h in horarios]

        self.horarios = [Horario(h) for h in horarios]

    def set_percurso(self, percurso):
        self.percurso = percurso

    def set_operador(self, operador):
        self.operador = operador
