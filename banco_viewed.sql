SET NAMES latin1;

CREATE DATABASE viewed;

USE viewed;

CREATE TABLE usuario (
    login varchar(100) NOT NULL,
    senha varchar(100) NOT NULL,
    nome varchar(100) not null,
    tipo varchar(1) NOT NULL,
    PRIMARY KEY (login)
);

CREATE TABLE midia (
    id int(11) NOT NULL AUTO_INCREMENT,
    titulo varchar(100) NOT NULL,
    genero varchar(100) NOT NULL,
    ano int(4) NOT NULL,
    sinopse varchar(4000) NOT NULL,
    tipo varchar(1) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE temporada (
    id int(11) NOT NULL AUTO_INCREMENT,
    midiaId int(11) NOT NULL,
    PRIMARY KEY (id, midiaId),
    FOREIGN KEY (midiaId) REFERENCES midia(id)
);

CREATE TABLE episodio (
    id int(11) NOT NULL AUTO_INCREMENT,
    temporadaId int(11) NOT NULL,
    PRIMARY KEY (id, temporadaId),
    FOREIGN KEY (temporadaId) REFERENCES temporada(id)
);

CREATE TABLE favorito (
    midiaId int(11) NOT NULL,
    usuarioId varchar(100) NOT NULL,
    PRIMARY KEY (midiaId, usuarioId),
    FOREIGN KEY (midiaId) REFERENCES midia(id),
    FOREIGN KEY (usuarioId) REFERENCES usuario(login)
);

CREATE TABLE visto (
    episodioId int(11) NOT NULL,
    usuarioId varchar(100) NOT NULL,
    PRIMARY KEY (episodioId, usuarioId),
    FOREIGN KEY (episodioId) REFERENCES episodio(id),
    FOREIGN KEY (usuarioId) REFERENCES usuario(login)
);

INSERT INTO midia (titulo, genero, ano, sinopse, tipo) values (%s, %s, %s, %s, %s);
