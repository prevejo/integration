import concurrent.futures
import asyncio
from collections import defaultdict
from domain.area_integracao import AreaIntegracao
from domain.linha import Linha
from domain.operacao import Operacao
from domain.operador import Operador
from domain.parada import Parada
from domain.percurso import Percurso
from domain.terminal import Terminal
from dto.area_integracao_parada import AreaIntegracaoParada
from dto.percurso_operacao import PercursoOperacao
from dto.percurso_parada import PercursoParada
from dto.percurso_terminal import PercursoTerminal
from model.model import Model
from model.resource import Resource


class ModelJoiner:
    
    resources = {
        'LINHAS': Resource('LINHAS', Linha),
        'PERCURSOS': Resource('PERCURSOS', Percurso),
        'PARADAS': Resource('PARADAS', Parada),
        'PARADAS_PERCURSOS': Resource('PARADAS_PERCURSOS', PercursoParada),
        'AREAS_INTEGRACAO': Resource('AREAS_INTEGRACAO', AreaIntegracao),
        'PARADAS_AREAS_INTEGRACAO': Resource('PARADAS_AREAS_INTEGRACAO', AreaIntegracaoParada),
        'TERMINAIS': Resource('TERMINAIS', Terminal),
        'PERCURSOS_TERMINAIS': Resource('PERCURSOS_TERMINAIS', PercursoTerminal),
        'OPERADORES': Resource('OPERADORES', Operador),
        'PERCURSOS_OPERACOES': Resource('PERCURSOS_OPERACOES', PercursoOperacao)
    }

    def __init__(self, logger):
        self.logger = logger

    async def join(self, model_loader):
        executor = concurrent.futures.ThreadPoolExecutor(max_workers=3)
        async_loop = asyncio.get_event_loop()
        result_linhas = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['LINHAS'])
        result_percursos = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['PERCURSOS'])
        result_paradas = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['PARADAS'])
        result_paradas_percursos = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['PARADAS_PERCURSOS'])
        result_areas_integracao = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['AREAS_INTEGRACAO'])
        result_paradas_areas = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['PARADAS_AREAS_INTEGRACAO'])
        result_terminais = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['TERMINAIS'])
        result_percursos_terminais = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['PERCURSOS_TERMINAIS'])
        result_operadores = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['OPERADORES'])
        result_percursos_operacoes = async_loop.run_in_executor(executor, model_loader.load_resource, self.resources['PERCURSOS_OPERACOES'])

        self.log('fetch linhas...')
        from_result_linhas = await result_linhas

        self.log('fetch percursos...')
        from_result_percursos = await result_percursos

        linhas = self.join_percursos_and_linhas(from_result_linhas, from_result_percursos)
        percursos = [p for l in linhas for p in l.percursos]

        self.log('fetch paradas...')
        paradas = await result_paradas
        self.log('fetch paradas_percursos...')
        paradas_percursos = await result_paradas_percursos

        self.join_percursos_and_paradas(percursos, paradas_percursos, paradas)

        self.log('fetch areas_integracao...')
        areas_integracao = await result_areas_integracao
        self.log('fetch paradas_areas...')
        paradas_areas_integracao = await result_paradas_areas

        self.join_areas_integracao_and_paradas(areas_integracao, paradas_areas_integracao, paradas)

        self.log('fetch terminais...')
        terminais = await result_terminais
        self.log('fetch percursos_terminais...')
        percursos_terminais = await result_percursos_terminais

        self.join_percursos_and_terminais_and_paradas(terminais, percursos_terminais, percursos, paradas)

        self.log('fetch operadores...')
        operadores = await result_operadores
        self.log('fetch percursos_operacoes...')
        percursos_operacoes = await result_percursos_operacoes

        operacoes = self.join_percursos_and_operadores(percursos, percursos_operacoes, operadores)

        return Model(linhas, percursos, paradas, paradas_percursos, areas_integracao, terminais, operadores, operacoes)

    def log(self, log):
        self.logger(log)

    @staticmethod
    def join_percursos_and_linhas(linhas, percursos):
        by_sentido = defaultdict(list)

        for p in percursos:
            by_sentido[(p.numero, p.sentido)].append(p)

        sentidos = [sentido for sentido in by_sentido.items() if len(sentido[1]) == 1]

        by_linha = defaultdict(list)

        for linha in linhas:
            by_linha[linha] = [sentido[1] for sentido in sentidos if sentido[0][0] == linha.numero]
            by_linha[linha] = [item for sublist in by_linha[linha] for item in sublist]

        percursos_by_linha = [p for p in by_linha.items() if len(p[1]) > 0]

        for linha in percursos_by_linha:
            for percurso in linha[1]:
                linha[0].add_percurso(percurso)

        return [linha[0] for linha in percursos_by_linha]

    @staticmethod
    def join_percursos_and_paradas(percursos, percursos_paradas, paradas):
        paradas_by_cod = defaultdict(list)

        for p in paradas:
            paradas_by_cod[p.cod] = p

        percursos_paradas = [pp for pp in percursos_paradas if pp.cod_parada in paradas_by_cod]

        for pp in percursos_paradas:
            pp.set_parada(paradas_by_cod[pp.cod_parada])

        percursos_paradas_by_percurso = defaultdict(list)

        for pp in percursos_paradas:
            percursos_paradas_by_percurso[(pp.numero, pp.sentido)].append(pp)

        for percurso in percursos:
            for pp in percursos_paradas_by_percurso[(percurso.numero, percurso.sentido)]:
                percurso.add_parada(pp)

    @staticmethod
    def join_areas_integracao_and_paradas(areas_integracao, areas_integracao_paradas, paradas):
        paradas_by_cod = defaultdict(list)

        for p in paradas:
            paradas_by_cod[p.cod].append(p)

        for area in areas_integracao:
            for area_parada in [ai for ai in areas_integracao_paradas if ai.descricao_area == area.descricao]:
                if area_parada.cod_parada in paradas_by_cod:
                    area.add_parada(paradas_by_cod[area_parada.cod_parada][0])

    @staticmethod
    def join_percursos_and_terminais_and_paradas(terminais, percursos_terminais, percursos, paradas):
        terminais_by_cod = defaultdict()
        for t in terminais:
            terminais_by_cod[t.cod] = t

        by_percursos = defaultdict()
        for p in percursos:
            by_percursos[(p.numero, p.sentido)] = p

        novas_paradas = []

        for terminal in terminais:
            parada = Parada('T' + terminal.cod, terminal.geo_centroid, terminal.geo_centroid)
            paradas.append(parada)
            novas_paradas.append(parada)
            terminal.set_parada(parada)

        for pt in percursos_terminais:
            if (pt.numero, pt.sentido) in by_percursos:
                percurso = by_percursos[(pt.numero, pt.sentido)]
                if pt.cod_terminal in terminais_by_cod:
                    parada = terminais_by_cod[pt.cod_terminal].parada

                    if pt.starts:
                        for parada_percurso in percurso.paradas:
                            parada_percurso.sequencial += 1
                        seq = 1
                        percurso_parada = PercursoParada(percurso.numero, percurso.sentido, parada.cod, seq)
                        percurso_parada.set_parada(parada)
                        percurso.paradas.insert(0, percurso_parada)

                    if pt.ends:
                        seq = max([p.sequencial for p in percurso.paradas] + [0]) + 1
                        percurso_parada = PercursoParada(percurso.numero, percurso.sentido, parada.cod, seq)
                        percurso_parada.set_parada(parada)
                        percurso.paradas.append(percurso_parada)

        return novas_paradas

    @staticmethod
    def join_percursos_and_operadores(percursos, percursos_operacoes, operadores):
        perc_set = defaultdict()
        for p in percursos:
            perc_set[(p.numero, p.sentido)] = p

        op_set = defaultdict()
        for operador in operadores:
            op_set[operador.descricao] = operador

        op_validas = [op for op in percursos_operacoes if
                      op.operador in op_set and (op.numero, op.sentido) in perc_set]

        operacoes = []
        for op in op_validas:
            operacao = Operacao(op.segunda, op.terca, op.quarta, op.quinta, op.sexta, op.sabado, op.domingo)
            operacao.set_horarios(op.horarios)
            operacao.set_percurso(perc_set[(op.numero, op.sentido)])
            operacao.set_operador(op_set[op.operador])
            operacoes.append(operacao)

        return operacoes
