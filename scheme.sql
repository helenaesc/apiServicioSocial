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
	enrolment_number varchar(10) unique,
	phone_number varchar(12),
	password varchar(100) not null,
	salt varchar(10) not null,
	admin boolean default false not null,
	degree varchar(5),
	semester tinyint
);

create table partner (
   id int auto_increment primary key,
   name varchar(100) not null 
);

create table week_days (
	id tinyint auto_increment primary key,
	name varchar(50) unique
);

create table modality (
	id tinyint auto_increment primary key,
	name varchar(50) unique
);

create table schedule (
	id tinyint auto_increment primary key,
	name varchar(50) unique
);

create table project (
	id int auto_increment primary key,
	name varchar(100) not null,
	id_partner int not null,
	id_modality tinyint not null,
	id_week_days tinyint not null, 
	id_schedule tinyint not null,
	slots int not null,
	schedule_description varchar(256),
	project_description varchar(512),
	foreign key(id_partner) references partner(id),
	foreign key(id_modality) references modality(id),
	foreign key(id_week_days) references week_days(id),
	foreign key(id_schedule) references schedule(id)
);

create table enrolment (
	id BIGINT auto_increment primary key,
	id_student BIGINT not null,
	id_project INT not null,
	enrolment_date DATETIME DEFAULT NOW(),
	id_status tinyint,
	id_token BIGINT,
	foreign key(id_student) references users(id),
	foreign key(id_project) references project(id),
	foreign key(id_status) references status(id),
	foreign key(id_token) references token(id)
);

create table status (
	id tinyint AUTO_INCREMENT primary key,
	name varchar(10) not null unique
);

create table token (
	id BIGINT AUTO_INCREMENT,
	id_project int,
	token varchar(10) unique,
	used boolean default false,
	primary key(id),
	foreign key (id_project) references project(id)
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

insert into week_days (name) values ('entre semana'), ('fines de semana'), ('mixto');
insert into modality (name) values ('en linea'), ('presencial'), ('mixto');
insert into schedule(name) values('matutino'), ('vespertino'), ('mixto');
insert into status(name) values('pendiente'), ('aceptado'), ('rechazado');