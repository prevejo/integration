CREATE SCHEMA transporte;

CREATE SEQUENCE transporte.seq_tb_linha;
CREATE SEQUENCE transporte.seq_tb_percurso;
CREATE SEQUENCE transporte.seq_tb_operador;
CREATE SEQUENCE transporte.seq_tb_operacao;
CREATE SEQUENCE transporte.seq_tb_horario;
CREATE SEQUENCE transporte.seq_tb_parada;
CREATE SEQUENCE transporte.seq_tb_area_integracao;
CREATE SEQUENCE transporte.seq_tb_terminal;


create table transporte.tb_linha (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_linha'::regclass),
        numero character varying(5) NOT NULL,
        descricao character varying(255) NOT NULL,
        tarifa numeric(5,2) NOT NULL,

        CONSTRAINT pk_tb_linha PRIMARY KEY(id)
);


create table transporte.tb_percurso (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_percurso'::regclass),
        id_linha integer NOT NULL,
        sentido character varying(8) NOT NULL,
        origem character varying(255) NOT NULL,
        destino character varying(255) NOT NULL,
        geo geometry(LineString,4326) NOT NULL,

        CONSTRAINT pk_tb_percurso PRIMARY KEY(id),
        CONSTRAINT fk_tb_percurso_to_tb_linha FOREIGN KEY(id_linha) REFERENCES transporte.tb_linha(id)
);


create table transporte.tb_operador (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_operador'::regclass),
        descricao character varying(255) NOT NULL,

        CONSTRAINT pk_tb_operador PRIMARY KEY(id)
);


create table transporte.tb_operacao (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_operacao'::regclass),
        id_operador integer NOT NULL,
        id_percurso integer NOT NULL,
        segunda boolean NOT NULL,
        terca boolean NOT NULL,
        quarta boolean NOT NULL,
        quinta boolean NOT NULL,
        sexta boolean NOT NULL,
        sabado boolean NOT NULL,
        domingo boolean NOT NULL,

        CONSTRAINT pk_tb_operacao PRIMARY KEY(id),
        CONSTRAINT fk_tb_operacao_to_tb_operador FOREIGN KEY(id_operador) REFERENCES transporte.tb_operador(id),
        CONSTRAINT fk_tb_operacao_to_tb_percurso FOREIGN KEY(id_percurso) REFERENCES transporte.tb_percurso(id)
);


create table transporte.tb_horario (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_horario'::regclass),
        id_operacao integer NOT NULL,
        horario time NOT NULL,

        CONSTRAINT pk_tb_horario PRIMARY KEY(id),
        CONSTRAINT fk_tb_horario_to_tb_operacao FOREIGN KEY(id_operacao) REFERENCES transporte.tb_operacao(id)
);


create table transporte.tb_parada (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_parada'::regclass),
        cod character varying(5) NOT NULL,
        geo geometry(Point,4326) NOT NULL,
        geo_via geometry(Point,4326) NOT NULL,

        CONSTRAINT pk_tb_parada PRIMARY KEY(id)
);


create table transporte.tb_percurso_parada (
        id_percurso integer NOT NULL,
        id_parada integer NOT NULL,
        sequencial integer NOT NULL,

        CONSTRAINT pk_tb_percurso_parada PRIMARY KEY(id_percurso, id_parada, sequencial),
        CONSTRAINT fk_tb_percurso_parada_to_tb_percurso FOREIGN KEY(id_percurso) REFERENCES transporte.tb_percurso(id),
        CONSTRAINT fk_tb_percurso_parada_to_tb_parada FOREIGN KEY(id_parada) REFERENCES transporte.tb_parada(id)
);


create table transporte.tb_area_integracao (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_area_integracao'::regclass),
        descricao character varying(255) NOT NULL,
        geo geometry(MultiPolygon,4326) NOT NULL,

        CONSTRAINT pk_tb_area_integracao PRIMARY KEY(id)
);


create table transporte.tb_area_parada (
        id_area_integracao integer NOT NULL,
        id_parada integer NOT NULL,

        CONSTRAINT pk_tb_area_parada PRIMARY KEY(id_area_integracao, id_parada),
        CONSTRAINT fk_tb_area_parada_to_tb_area_integracao FOREIGN KEY(id_area_integracao) REFERENCES transporte.tb_area_integracao(id),
        CONSTRAINT fk_tb_area_parada_to_tb_parada FOREIGN KEY(id_parada) REFERENCES transporte.tb_parada(id)
);


create table transporte.tb_terminal (
        id integer NOT NULL DEFAULT nextval('transporte.seq_tb_terminal'::regclass),
        id_parada integer NOT NULL,
        descricao character varying(255) NOT NULL,
        cod character varying(5) NOT NULL,
        geo geometry(Polygon,4326) NOT NULL,

        CONSTRAINT pk_tb_terminal PRIMARY KEY(id),
        CONSTRAINT fk_tb_terminal_to_tb_parada FOREIGN KEY(id_parada) REFERENCES transporte.tb_parada(id)
);

