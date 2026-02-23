set NAMES utf8mb4;
set foreign_key_checks=0;

drop database if exists poncho;
create database poncho character set utf8mb4 collate utf8mb4_unicode_ci;
use poncho;
 
create table users(
	id BIGINT auto_increment primary key,
	first_name varchar(50) not null,
	second_name varchar(50),
	p_last_name varchar(100) not null,
	m_last_name varchar(100) not null,
	email varchar(50) not null unique,
	matricula varchar(10) unique,
	num_telefono varchar(12),
	password varchar(100) not null,
	salt varchar(10) not null,
	admin boolean default false not null,
	degree varchar(5),
	semester tinyint
);

create table socio (
   id int auto_increment primary key,
   name varchar(100) not null 
);

create table dias (
	id tinyint auto_increment primary key,
	description varchar(50) unique
);

create table modalidad (
	id tinyint auto_increment primary key,
	description varchar(50) unique
);

create table horario (
	id tinyint auto_increment primary key,
	description varchar(50) unique
);

create table project (
	id int auto_increment primary key,
	name varchar(100) not null,
	id_socio int not null,
	id_modalidad tinyint not null,
	id_dias tinyint not null, 
	id_horario tinyint not null,
	cupos int not null,
	descripcion_horario varchar(256),
	descripcion varchar(512),
	foreign key(id_socio) references socio(id),
	foreign key(id_modalidad) references modalidad(id),
	foreign key(id_dias) references dias(id),
	foreign key(id_horario) references horario(id)
);

create table inscripcion (
	id BIGINT auto_increment primary key,
	id_alumno BIGINT not null,
	id_proyecto INT not null,
	fecha_inscripcion DATETIME DEFAULT NOW(),
	id_status tinyint,
	id_token BIGINT,
	foreign key(id_alumno) references users(id),
	foreign key(id_proyecto) references project(id),
	foreign key(id_status) references status(id),
	foreign key(id_token) references token(id)
);

create table status (
	id tinyint AUTO_INCREMENT,
	name varchar(10) not null unique,
	primary key(id)
);

create table token (
	id BIGINT AUTO_INCREMENT,
	id_proyecto int,
	token varchar(10) unique,
	used boolean default false,
	primary key(id),
	foreign key (id_proyecto) references project(id)
);

CREATE TABLE email_verification_codes (
    id BIGINT AUTO_INCREMENT PRIMARY KEY,
    id_user BIGINT NOT NULL,
    code_hash VARCHAR(255) NOT NULL,
    expires_at DATETIME NOT NULL,
    used BOOLEAN DEFAULT FALSE,
    created_at DATETIME DEFAULT NOW(),
    FOREIGN KEY (id_user) REFERENCES users(id)
);

set foreign_key_checks = 1;

-- Status

insert into status (name) values ('Pendiente'), ('Rechazado'), ('Aceptado');

