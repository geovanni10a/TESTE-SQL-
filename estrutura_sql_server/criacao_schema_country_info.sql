GO

CREATE DATABASE countries_info;

GO

USE countries_info;

GO

CREATE SCHEMA country_info; 

GO

CREATE SCHEMA countries;

GO

CREATE TABLE country_info.continents (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) NOT NULL,
	sCode VARCHAR(10) NOT NULL
);

CREATE TABLE country_info.languages (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) NOT NULL,
	sCode VARCHAR(10) NOT NULL
);

CREATE TABLE country_info.currencies (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) NOT NULL,
	sCode VARCHAR(10) NOT NULL
);

CREATE TABLE country_infos.countries (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) NOT NULL,
	sCode VARCHAR(10) NOT NULL,
	capitalCity VARCHAR(255) NOT NULL,
	flagPath VARCHAR(200) NOT NULL,
	phoneCode INTEGER NOT NULL,
	fkCurrency INTEGER FOREIGN KEY REFERENCES country_info.currencies(id),
	fkContinent INTEGER FOREIGN KEY REFERENCES country_info.continents(id)
);

CREATE TABLE country_infos.lang_countries (
	countryID INTEGER FOREIGN KEY REFERENCES country_info.countries(id) ON DELETE CASCADE,
	languageID INTEGER FOREIGN KEY REFERENCES country_info.languages(id) ON DELETE CASCADE
);

GO
