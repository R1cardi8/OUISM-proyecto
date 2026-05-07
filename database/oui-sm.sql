CREATE DATABASE ciudad_db;
USE ciudad_db;


CREATE TABLE usuarios (
  id         INT AUTO_INCREMENT PRIMARY KEY,
  nombre     VARCHAR(100) NOT NULL,
  email      VARCHAR(150) NOT NULL UNIQUE,
  password   VARCHAR(255) NOT NULL,
  rol        VARCHAR(20)  DEFAULT 'usuario',
  fecha      DATETIME     DEFAULT CURRENT_TIMESTAMP
);


CREATE TABLE incidentes (
  id          INT AUTO_INCREMENT PRIMARY KEY,
  usuario_id  INT,
  titulo      VARCHAR(255) NOT NULL,
  descripcion TEXT         NOT NULL,
  tipo        VARCHAR(50)  NOT NULL,
  ubicacion   VARCHAR(255),
  prioridad   VARCHAR(20)  NOT NULL,
  foto        LONGTEXT,
  fecha       DATETIME     DEFAULT CURRENT_TIMESTAMP,
  FOREIGN KEY (usuario_id) REFERENCES usuarios(id)
);