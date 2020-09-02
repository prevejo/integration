COPY (

select 'insert into transporte.tb_parada(id, cod, geo, geo_via) values (' || id || ',''' || cod || ''',X''' || upper(encode(ST_AsEWKB(geo), 'hex')) || ''',X''' || upper(encode(ST_AsEWKB(geo_via), 'hex')) || ''');' from transporte.tb_parada
union all
select 'insert into transporte.tb_area_integracao(id, descricao, geo) values (' || id || ',''' || replace(descricao, '''', '''''') || ''',X''' || upper(encode(ST_AsEWKB(geo), 'hex')) || ''');' from transporte.tb_area_integracao
union all
select 'insert into transporte.tb_area_parada(id_area_integracao, id_parada) values (' || id_area_integracao || ',' || id_parada || ');' from transporte.tb_area_parada
union all
select 'insert into transporte.tb_terminal(id, id_parada, cod, descricao, geo) values (' || id || ',' || id_parada || ',''' || cod || ''',''' || replace(descricao, '''', '''''') || ''',X''' || upper(encode(ST_AsEWKB(geo), 'hex')) || ''');' from transporte.tb_terminal
union all
select 'insert into transporte.tb_linha(id, numero, descricao, tarifa) values (' || id || ',''' || numero || ''',''' || replace(descricao, '''', '''''') || ''',' || tarifa || ');' from transporte.tb_linha
union all
select 'insert into transporte.tb_percurso(id, id_linha, sentido, origem, destino, geo) values (' || id || ',' || id_linha || ',''' || sentido || ''',''' || replace(origem, '''', '''''') || ''',''' || replace(destino, '''', '''''') || ''',X''' || upper(encode(ST_AsEWKB(geo), 'hex')) || ''');' from transporte.tb_percurso
union all
select 'insert into transporte.tb_percurso_parada(id_percurso, id_parada, sequencial) values (' || id_percurso || ',' || id_parada || ',' || sequencial || ');' from transporte.tb_percurso_parada
union all
select 'insert into transporte.tb_operador(id, descricao) values (' || id || ',''' || replace(descricao, '''', '''''') || ''');' from transporte.tb_operador
union all
select 'insert into transporte.tb_operacao(id, id_operador, id_percurso, segunda, terca, quarta, quinta, sexta, sabado, domingo) values (' || id || ',' || id_operador || ',' || id_percurso || ',' || segunda || ',' || terca || ',' || quarta || ',' || quinta || ',' || sexta || ',' || sabado || ',' || domingo || ');' from transporte.tb_operacao
union all
select 'insert into transporte.tb_horario(id, id_operacao, horario) values (' || id || ',' || id_operacao || ',''' || to_char(horario, 'HH24:MI') || ''');' from transporte.tb_horario
union all
select 'insert into comunidade.tb_informativo(titulo, resumo, dt_publicacao, endereco) values (''Humanos são vistos aos arredores de Brasília'', ''Um bocado de criaturas humanas foram avistadas na madrugada do último domingo na região que até o presente momento era tida como segura, 15 km à sudeste de Brasília, apresentando um comportamento interpretado como animalesco e...'', ''2019-10-21 14:49:01'', ''http://example.com/'');'::text
union all
select 'insert into comunidade.tb_informativo(titulo, resumo, dt_publicacao, endereco) values (''Cresce o número de adeptos ao teletransporte'', ''Após forte oposição do Conselho de Virtudes Transversais, o teletransporte é regulamentado na área 342 e passa a apresenta um número crescente de adeptos no setor. Mesmo que as implicações ainda continuam sendo discutidas pelo conselho, boa parte do...'', ''2019-10-22 15:49:01'', ''http://example.com/'');'::text
union all
select 'insert into comunidade.tb_informativo(titulo, resumo, dt_publicacao, endereco) values (''Mudanças no fluxo temporal causam protestos novamente'', ''Com o índice de influxo tendendo a zero, a Cúpula Eterna outorga mudanças severas no fluxo temporal na tentativa de evitar um eminente colapso da camada realística. Todavia, viajantes reclamam da imprudência na escolha do momento, e ainda...'', ''2019-10-23 16:49:01'', ''http://example.com/'');'::text
union all
select 'insert into comunidade.tb_topico(titulo) values(''Linha de transporte'');'::text
union all
select 'insert into comunidade.tb_topico(titulo) values(''Ponto de embarque'');'::text
union all
select 'insert into comunidade.tb_topico(titulo) values(''Operador'');'::text
union all
select 'insert into comunidade.tb_topico(titulo) values(''Veículo'');'::text

) TO '/tmp/data-h2.sql'
