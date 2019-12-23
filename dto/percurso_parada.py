class PercursoParada:
    def __init__(self, numero: 'numero', sentido: 'sentido', cod_parada: 'cod', sequencial: 'sequencial'):
        self.numero = numero
        self.sentido = sentido
        self.cod_parada = cod_parada
        self.sequencial = sequencial
        self.parada = None

    def set_parada(self, parada):
        self.parada = parada
