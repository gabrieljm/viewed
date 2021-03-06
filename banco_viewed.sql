SET NAMES latin1;

CREATE DATABASE viewed;

USE viewed;

CREATE TABLE usuario (
    nome varchar(100) not null,
    login varchar(100) NOT NULL,
    senha varchar(100) NOT NULL,
    tipo varchar(1) NOT NULL,
    PRIMARY KEY (login)
);

CREATE TABLE midia (
    id int(11) NOT NULL AUTO_INCREMENT,
    titulo varchar(100) NOT NULL,
    genero varchar(100) NOT NULL,
    ano int(4) NOT NULL,
    sinopse varchar(4000) NOT NULL,
    temporadas int(11) NOT NULL,
    PRIMARY KEY (id)
);

CREATE TABLE episodio (
    id int(11) NOT NULL AUTO_INCREMENT,
    midiaId int(11) NOT NULL,
    temporadaId int(11) NOT NULL,
    nome varchar(100),
    PRIMARY KEY (id, midiaId, temporadaId),
    FOREIGN KEY (midiaId) REFERENCES midia(id),
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
    midiaId int(11) NOT NULL,
    temporadaId int(11) NOT NULL,
    episodioId int(11) NOT NULL,
    usuarioId varchar(100) NOT NULL,
    PRIMARY KEY (midiaId, temporadaId, episodioId, usuarioId),
    FOREIGN KEY (midiaId) REFERENCES midia(id),
    FOREIGN KEY (temporadaId) REFERENCES temporada(id),
    FOREIGN KEY (episodioId) REFERENCES episodio(id),
    FOREIGN KEY (usuarioId) REFERENCES usuario(login)
);

INSERT INTO midia (titulo, genero, ano, sinopse, tipo) values (%s, %s, %s, %s, %s);
