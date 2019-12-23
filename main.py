import asyncio
import time
from db.db import DataBase
from model.model_joiner import ModelJoiner

from model.model_register import ModelRegister
from ws_dft_loader import WSDFTLoader


def log(log_str):
    print(log_str)


def load_from_ws():
    loader = WSDFTLoader()
    joiner = ModelJoiner(log)

    return joiner.join(loader)


def register(model):
    conn_provider = DataBase.instance_output_db()
    try:
        model_register = ModelRegister(conn_provider, log)

        model_register.register(model)
    finally:
        conn_provider.close_all_holders()


async def process():
    model = await load_from_ws()

    register(model)

    log('Linhas   : ' + str(len(model.linhas)))
    log('Percursos: ' + str(len(model.percursos)))
    log('Paradas: ' + str(len(model.paradas)))
    log('PercursosParadas: ' + str(len(model.paradas_percursos)))
    log('AreasIntegracao: ' + str(len(model.areas_integracao)))
    log('Terminais: ' + str(len(model.terminais)))
    log('Operadores: ' + str(len(model.operadores)))
    log('Operacoes: ' + str(len(model.operacoes)))


if __name__ == "__main__":
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)

    start_time = time.time()
    loop.run_until_complete(process())
    print("--- %s seconds ---" % (time.time() - start_time))
