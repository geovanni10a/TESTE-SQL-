GO

CREATE DATABASE countries_info;

GO

USE countries_info;

GO

CREATE SCHEMA country_info; 

GO

-- Colocar Constraint UNIQUE nos códigos e nomes??
CREATE TABLE [country_info].[continents] (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) UNIQUE NOT NULL,
	sCode VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE [country_info].[languages] (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) NOT NULL,
	sCode VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE [country_info].[currencies] (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) NOT NULL,
	sCode VARCHAR(10) UNIQUE NOT NULL
);

CREATE TABLE [country_info].[countries] (
	id INTEGER IDENTITY PRIMARY KEY,
	sName VARCHAR(255) UNIQUE NOT NULL,
	sCode VARCHAR(10) UNIQUE NOT NULL,
	capitalCity VARCHAR(255) NOT NULL,
	flagPath VARCHAR(200) NOT NULL,
	phoneCode INTEGER NOT NULL,
	fkCurrency INTEGER FOREIGN KEY REFERENCES country_info.currencies(id),
	fkContinent INTEGER FOREIGN KEY REFERENCES country_info.continents(id)
);

-- Criando tabela joint para unir countries com languages
-- Mudar nome para fk
CREATE TABLE [country_info].[lang_countries] (
	fkCountry INTEGER FOREIGN KEY REFERENCES country_info.countries(id) ON DELETE CASCADE,
	fkLanguage INTEGER FOREIGN KEY REFERENCES country_info.languages(id) ON DELETE CASCADE
);

GO

-- Função para ajustar inserção de dados na tabela joint
CREATE OR ALTER PROCEDURE insert_lang_countries
@fkCountry INTEGER,
@fkLanguage INTEGER
AS 
BEGIN
	SET NOCOUNT ON;

	DECLARE @id_country INTEGER;
	DECLARE @id_language INTEGER;

	-- Verifica se o id do linguagem e pais existe associados em lang_countries
	SELECT @id_language = lc.fkLanguage, @id_country = lc.fkCountry 
	FROM country_info.lang_countries AS lc 
	WHERE lc.fkLanguage = @fkLanguage AND lc.fkCountry = @fkCountry;

	-- Se o pais e a lingua não estiverem associados, adicionar
	IF NOT (@id_language IS NOT NULL AND @id_country IS NOT NULL) 
	BEGIN
		INSERT INTO country_info.lang_countries (fkCountries, fkLanguage)
		VALUES (@fkCountry, @fkLanguage);
	END;

END;
GO


