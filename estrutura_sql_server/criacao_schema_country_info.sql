GO

CREATE DATABASE country_info;

GO

USE country_info

GO

CREATE SCHEMA principal 

GO

-- Estrutura básica com tabela única para teste.

CREATE TABLE principal.continents (
	id INTEGER IDENTITY PRIMARY KEY,
	continent_name VARCHAR(100) NOT NULL,
	continent_ISO_code VARCHAR(10) NOT NULL,
);

GO
