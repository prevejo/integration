
create table transporte.tb_localizacao_veiculo (
    num_veiculo character varying(8) NOT NULL,
    num_linha character varying(5),
    ds_sentido character varying(10),
    ds_operadora character varying(20) NOT NULL,
    num_velocidade numeric(5, 2),
    ds_velocidade character varying(4),
    num_direcao numeric(5, 2),
    dt_localizacao timestamp without time zone NOT NULL,
    geo geometry(Point,4326) NOT NULL
);

CREATE INDEX idx_num_linha_loc_veiculo ON transporte.tb_localizacao_veiculo (num_linha);
CLUSTER transporte.tb_localizacao_veiculo USING idx_num_linha_loc_veiculo;



CREATE SCHEMA comunidade;

CREATE SEQUENCE comunidade.seq_tb_informativo;
CREATE SEQUENCE comunidade.seq_tb_topico;
CREATE SEQUENCE comunidade.seq_tb_comentario;


create table comunidade.tb_informativo (
	id integer NOT NULL DEFAULT nextval('comunidade.seq_tb_informativo'::regclass),
	titulo character varying(255) NOT NULL,
	resumo character varying(4000) NOT NULL,
	dt_publicacao timestamp NOT NULL,
	endereco character varying(255) NOT NULL,

	CONSTRAINT pk_tb_informativo PRIMARY KEY(id)
);


create table comunidade.tb_topico (
	id integer NOT NULL DEFAULT nextval('comunidade.seq_tb_topico'::regclass),
	titulo character varying(255) NOT NULL,

	CONSTRAINT pk_tb_topico PRIMARY KEY(id)
);


create table comunidade.tb_comentario (
	id integer NOT NULL DEFAULT nextval('comunidade.seq_tb_comentario'::regclass),
	id_topico integer NOT NULL,
	assunto character varying(255) NOT NULL,
	comentario character varying(4000) NOT NULL,
	relevancia integer NOT NULL,
	dt_publicacao timestamp NOT NULL,

	CONSTRAINT pk_tb_comentario PRIMARY KEY(id),
	CONSTRAINT fk_tb_comentario_to_tb_topico FOREIGN KEY(id_topico) REFERENCES comunidade.tb_topico(id)
);


insert into comunidade.tb_informativo(titulo, resumo, dt_publicacao, endereco) values ('Humanos são vistos aos arredores de Brasília', 'Um bocado de criaturas humanas foram avistadas na madrugada do último domingo na região que até o presente momento era tida como segura, 15 km à sudeste de Brasília, apresentando um comportamento interpretado como animalesco e...', '2019-10-21 14:49:01', 'http://example.com/');
insert into comunidade.tb_informativo(titulo, resumo, dt_publicacao, endereco) values ('Cresce o número de adeptos ao teletransporte', 'Após forte oposição do Conselho de Virtudes Transversais, o teletransporte é regulamentado na área 342 e passa a apresenta um número crescente de adeptos no setor. Mesmo que as implicações ainda continuam sendo discutidas pelo conselho, boa parte do...', '2019-10-22 15:49:01', 'http://example.com/');
insert into comunidade.tb_informativo(titulo, resumo, dt_publicacao, endereco) values ('Mudanças no fluxo temporal causam protestos novamente', 'Com o índice de influxo tendendo a zero, a Cúpula Eterna outorga mudanças severas no fluxo temporal na tentativa de evitar um eminente colapso da camada realística. Todavia, viajantes reclamam da imprudência na escolha do momento, e ainda...', '2019-10-23 16:49:01', 'http://example.com/');
insert into comunidade.tb_topico(titulo) values('Linha de transporte');
insert into comunidade.tb_topico(titulo) values('Ponto de embarque');
insert into comunidade.tb_topico(titulo) values('Operador');
insert into comunidade.tb_topico(titulo) values('Veículo');