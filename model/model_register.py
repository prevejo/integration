class ModelRegister:

    def __init__(self, conn_provider, logger):
        self.conn_provider = conn_provider
        self.logger = logger

    def log(self, log):
        self.logger(log)

    def register(self, model):
        self.log('register paradas... ')
        self.register_paradas(model.paradas)

        self.log('register areas... ')
        self.register_areas_integracao(model.areas_integracao)

        self.log('register paradas & areas... ')
        self.register_areas_integracao_paradas(model.areas_integracao)

        self.log('register terminais... ')
        self.register_terminal(model.terminais)

        self.log('register linhas... ')
        self.register_linhas(model.linhas)

        self.log('register percursos... ')
        self.register_percursos(model.linhas)

        self.log('register paradas & percursos... ')
        self.register_paradas_percursos(model.percursos)

        self.log('register operadores... ')
        self.register_operadores(model.operadores)

        self.log('register operacoes... ')
        self.register_operacoes(model.operacoes)

        self.log('register horarios... ')
        self.register_horarios(model.operacoes)

    def register_paradas(self, paradas):
        sql = "insert into transporte.tb_parada(id, cod, geo, geo_via) values"
        attrs_suppliers = [lambda o: o.cod, lambda o: o.geo, lambda o: o.geo_via]

        id_list = self.insert_batch_list(sql, attrs_suppliers, paradas, 'transporte."seq_tb_parada"')
        # id_list = self.insert_file_list(sql, '1-tb_parada.sql', attrs_suppliers, ['%s', 'X%s', 'X%s'], paradas, True)

        for op, _id in zip(paradas, id_list):
            op.set_id(_id)

    def register_areas_integracao(self, areas_integracao):
        sql = "insert into transporte.tb_area_integracao(id, descricao, geo) values"
        attrs_suppliers = [lambda o: o.descricao, lambda o: o.geo]

        id_list = self.insert_batch_list(sql, attrs_suppliers, areas_integracao, 'transporte."seq_tb_area_integracao"')
        # id_list = self.insert_file_list(sql, '2-tb_area_integracao.sql', attrs_suppliers,
        # ['%s', 'X%s'], areas_integracao, True)

        for op, _id in zip(areas_integracao, id_list):
            op.set_id(_id)

    def register_areas_integracao_paradas(self, areas_integracao):
        sql = "insert into transporte.tb_area_parada(id_area_integracao, id_parada) values"
        line_list = [(area, parada) for area in areas_integracao for parada in area.paradas]
        attrs_suppliers = [lambda t: t[0].get_id(), lambda t: t[1].get_id()]

        self.insert_batch_list(sql, attrs_suppliers, line_list)
        # self.insert_file_list(sql, '3-tb_area_parada.sql', attrs_suppliers,
        # ['%s' for a in attrs_suppliers], line_list)

    def register_terminal(self, terminais):
        sql = "insert into transporte.tb_terminal(id, id_parada, cod, descricao, geo) values"
        attrs_suppliers = [lambda o: o.parada.get_id() if o.parada is not None else None,
                           lambda o: o.cod, lambda o: o.descricao, lambda o: o.geo]

        id_list = self.insert_batch_list(sql, attrs_suppliers, terminais, 'transporte."seq_tb_terminal"')
        # id_list = self.insert_file_list(sql, '4-tb_linha.sql', attrs_suppliers,
        # ['%s', '%s', '%s', 'X%s'], terminais, True)

        for op, _id in zip(terminais, id_list):
            op.set_id(_id)

    def register_linhas(self, linhas):
        sql = "insert into transporte.tb_linha(id, numero, descricao, tarifa) values"
        attrs_suppliers = [lambda o: o.numero, lambda o: o.descricao, lambda o: o.tarifa]

        id_list = self.insert_batch_list(sql, attrs_suppliers, linhas, 'transporte."seq_tb_linha"')
        # id_list = self.insert_file_list(sql, '5-tb_linha.sql', attrs_suppliers,
        # ['%s' for a in attrs_suppliers], linhas, True)

        for op, _id in zip(linhas, id_list):
            op.set_id(_id)

    def register_percursos(self, linhas):
        sql = "insert into transporte.tb_percurso(id, id_linha, sentido, origem, destino, geo) values"
        line_list = [(linha, percurso) for linha in linhas for percurso in linha.percursos]
        attrs_suppliers = [lambda t: t[0].get_id(), lambda t: t[1].sentido, lambda t: t[1].origem,
                           lambda t: t[1].destino, lambda t: t[1].geo]

        id_list = self.insert_batch_list(sql, attrs_suppliers, line_list, 'transporte."seq_tb_percurso"')
        # id_list = self.insert_file_list(sql, '6-tb_percurso.sql', attrs_suppliers,
        # ['%s', '%s', '%s', '%s', 'X%s'], line_list, True)

        for op, _id in zip(line_list, id_list):
            op[1].set_id(_id)

    def register_paradas_percursos(self, percursos):
        sql = "insert into transporte.tb_percurso_parada(id_percurso, id_parada, sequencial) values"
        line_list = [(perc, perc_parada) for perc in percursos for perc_parada in perc.paradas]
        attrs_suppliers = [lambda t: t[0].get_id(), lambda t: t[1].parada.get_id(), lambda t: t[1].sequencial]

        self.insert_batch_list(sql, attrs_suppliers, line_list)
        # self.insert_file_list(sql, '7-tb_percurso_parada.sql', attrs_suppliers,
        # ['%s' for a in attrs_suppliers], line_list)

    def register_operadores(self, operadores):
        sql = "insert into transporte.tb_operador(id, descricao) values"
        attrs_suppliers = [lambda o: o.descricao]

        id_list = self.insert_batch_list(sql, attrs_suppliers, operadores, 'transporte."seq_tb_operador"')
        # id_list = self.insert_file_list(sql, '8-tb_operador.sql', attrs_suppliers,
        # ['%s' for a in attrs_suppliers], operadores, True)

        for op, _id in zip(operadores, id_list):
            op.set_id(_id)

    def register_operacoes(self, operacoes):
        sql = "insert into transporte.tb_operacao(id, id_operador, id_percurso, segunda, terca, quarta, " \
              "quinta, sexta, sabado, domingo) values"
        attrs_suppliers = [lambda o: o.operador.get_id(), lambda o: o.percurso.get_id(), lambda o: o.segunda, lambda o: o.terca, lambda o: o.quarta,
                           lambda o: o.quinta, lambda o: o.sexta, lambda o: o.sabado, lambda o: o.domingo]

        id_list = self.insert_batch_list(sql, attrs_suppliers, operacoes, 'transporte."seq_tb_operacao"')
        # id_list = self.insert_file_list(sql, '9-tb_operacao.sql', attrs_suppliers,
        # ['%s' for a in attrs_suppliers], operacoes, True)

        for op, _id in zip(operacoes, id_list):
            op.set_id(_id)

    def register_horarios(self, operacoes):
        sql = "insert into transporte.tb_horario(id, id_operacao, horario) values"
        line_list = [(operacao, horario) for operacao in operacoes for horario in operacao.horarios]
        attrs_suppliers = [lambda t: t[0].get_id(), lambda t: t[1].horario]

        self.insert_batch_list(sql, attrs_suppliers, line_list, 'transporte."seq_tb_horario"')
        # self.insert_file_list(sql, '91-tb_horario.sql', attrs_suppliers,
        # ['%s' for a in attrs_suppliers], line_list, True)

    def insert_batch_list(self, sql, attrs_suppliers, entities, sequence_name=None, batch_size=100):
        conn_holder = self.conn_provider.get_holder()
        try:
            id_list = None
            conn = conn_holder.connect()

            cursor = conn.cursor()
            try:
                if sequence_name is not None:
                    cursor.execute("SELECT nextval('{0}')".format(sequence_name))
                    id_list = []
                    last_id = cursor.fetchone()[0]

                statements_list = []
                count = 0
                for e in entities:
                    count += 1
                    attrs = [attr(e) for attr in attrs_suppliers]

                    if sequence_name is not None:
                        last_id += 1
                        id_list.append(last_id)
                        values = "nextval('{0}'),".format(sequence_name) + ",".join(['%s' for a in attrs])
                    else:
                        values = ",".join(['%s' for a in attrs])

                    statements_list.append(cursor.mogrify(sql + " (" + values + ")", attrs))

                    if count % batch_size == 0:
                        cursor.execute(b';'.join(statements_list))
                        statements_list.clear()

                if len(statements_list) > 0:
                    cursor.execute(b';'.join(statements_list))
            finally:
                cursor.close()

            conn.commit()

            return id_list
        finally:
            conn_holder.release()

    def insert_file_list(self, sql, file_name, attrs_suppliers, attrs_mask, entities, write_id=False):
        conn_holder = self.conn_provider.get_holder()
        try:
            id_list = None
            conn = conn_holder.connect()

            cursor = conn.cursor()
            try:
                if write_id:
                    id_list = []
                    last_id = 0

                statements_list = []
                for e in entities:
                    attrs = [attr(e) for attr in attrs_suppliers]

                    values = ','.join([a for a in attrs_mask])

                    if write_id:
                        last_id += 1
                        id_list.append(last_id)
                        values = str(last_id) + ',' + values

                    statements_list.append(cursor.mogrify(sql + " (" + values + ")", attrs))
            finally:
                cursor.close()

            with open('C:\\Temp\\' + file_name, 'wb') as file:
                for i in statements_list:
                    file.write(i + b';\n')

            return id_list
        finally:
            conn_holder.release()
