-- DATA EXPLORATION

-- General Data View --

SELECT location, date, total_cases, new_cases, new_deaths, total_deaths, population 
FROM PortfolioProject..['2023_CovidDeaths$']
--WHERE continent is not NULL	
	WHERE location = 'World'
ORDER BY 1,2

-- Calculatio of Death Ratio (i.e. % of death per reportred cases)

SELECT location, date, total_cases, new_cases, total_deaths, population, 
(total_deaths/total_cases)*100 AS DeathRatio
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL	
--WHERE location = 'Italy'
ORDER BY 1,2

-- Percentage of population infected (rolling)

SELECT location, date, total_cases, new_cases, total_deaths, population, 
(total_cases/population)*100 AS '%Infected'
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL	
--WHERE location = 'Italy'
ORDER BY 1,2

-- Current Infection Rates per Country

SELECT location, population, MAX(total_cases),
MAX(total_cases/population)*100 AS '%Infected'
FROM PortfolioProject..['2023_CovidDeaths$']
--WHERE location = 'Italy'
WHERE continent is not NULL	
GROUP BY location, population
ORDER BY 4 DESC

-- Current Death Count per Country

SELECT location, population, MAX(CAST(total_deaths as int)) as Total_Deaths_Count,
MAX(total_deaths/population)*100 AS '%Death'
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL	
--WHERE location = 'Italy'
GROUP BY location, population
ORDER BY 3 DESC

-- Total number of deaths by continent --
	
	--Sum New Deaths

SELECT continent, SUM(CAST(new_deaths as int)) as Total_Deaths_Count
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL --and continent = 'North America'
GROUP BY continent;

	--Find max value of total deaths per country 

WITH table_cont (continent, location, Tot_Death_Count) 
AS
(
SELECT continent, location, MAX(CAST(total_deaths as int))
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL
GROUP BY continent, location
)
SELECT continent, SUM(Tot_Death_Count) as Cont_Death_Count
FROM table_cont
GROUP BY continent

	--* Note the two measures do not match --> Most consistent value to choose is the Total_death value reported on the last available date

-- Global numbers

SELECT location, MAX(CAST(total_deaths as int)) as Total_Deaths_Count
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE location like 'world'
GROUP BY location;


SELECT date, SUM(new_cases), SUM(cast(new_deaths as int)), SUM(cast(new_deaths as int))/SUM(new_cases)*100 as '%Deaths'
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL
GROUP BY date
order by 1,2

-- New vaccination numbers

SELECT cde.continent, cde.location, cde.date, cde.population, cvac.new_vaccinations
FROM PortfolioProject..['2023_CovidDeaths$'] cde
JOIN PortfolioProject..['2023_CovidVacc$'] cvac
ON cde.location = cvac.location
	and cde.date = cvac.date
WHERE cde.continent is not NULL
ORDER BY 2,3

	-- Total vaccinations are only reported for a few dates.
	-- Creating a column with the rolling number of vaccinations fills in gaps


SELECT cde.continent, cde.location, cde.date, cde.population, cvac.new_vaccinations,
SUM(CONVERT(bigint,cvac.new_vaccinations)) OVER (Partition by cde.location ORDER BY cde.location, cde.date) AS tot_vacc_todate
FROM PortfolioProject..['2023_CovidDeaths$'] cde
JOIN PortfolioProject..['2023_CovidVacc$'] cvac
ON cde.location = cvac.location
	and cde.date = cvac.date
WHERE cde.continent is NULL
ORDER BY 2,3
	-- In many locations the sum of new vaccinations does not correspond to the total vaccinations reported, hence it is best to use the LAST date available for this column
	-- I.E. Select most recent value from total_vaccinations that is not null

SELECT cde.continent, cde.location, cde.population, MAX(cvac.total_vaccinations) AS Max_Vacc
FROM PortfolioProject..['2023_CovidDeaths$'] cde
JOIN PortfolioProject..['2023_CovidVacc$'] cvac
ON cde.location = cvac.location
	and cde.date = cvac.date
WHERE cde.continent is NOT NULL
GROUP BY cde.continent, cde.location, cde.population;

-- rolling percentage of vaccinated vs population
-- cannot be used since total vaccinations do not match the final sum of new vaccinations

WITH rolling_count (Continent, Location, Date, Population, New_Vaccinations, Tot_Vacc_Todate)
AS
(SELECT cde.continent, cde.location, cde.date, cde.population, cvac.new_vaccinations,
SUM(CONVERT(bigint,cvac.new_vaccinations)) OVER (Partition by cde.location ORDER BY cde.location, cde.date) AS tot_vacc_todate
FROM PortfolioProject..['2023_CovidDeaths$'] cde
JOIN PortfolioProject..['2023_CovidVacc$'] cvac
ON cde.location = cvac.location
	and cde.date = cvac.date
WHERE cde.continent is not NULL
)
SELECT *, (Tot_Vacc_Todate/population)
FROM rolling_count


-- with temp_table

DROP TABLE IF EXISTS PercPopVacc
CREATE TABLE PercPopVacc
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_Vaccinations numeric,
Tot_Vacc_Todate numeric
)

INSERT INTO PercPopVacc
SELECT cde.continent, cde.location, cde.date, cde.population, cvac.new_vaccinations,
SUM(CONVERT(bigint,cvac.new_vaccinations)) OVER (Partition by cde.location ORDER BY cde.location, cde.date) AS Tot_Vacc_Todate
FROM PortfolioProject..['2023_CovidDeaths$'] cde
JOIN PortfolioProject..['2023_CovidVacc$'] cvac
ON cde.location = cvac.location
	and cde.date = cvac.date
WHERE cde.continent is not NULL

SELECT *, (Tot_Vacc_Todate/Population)*100 as '%Pop_Vaccinated'
FROM PercPopVacc

-- COMPARE MAX DEATHS TO TOTAL DEATHS ON MOST RECENT DAY
-- the max of total deaths for some locations does not correspond to the number reported on the most recent day

SELECT continent, location, total_deaths
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL	
	AND CONVERT(DATE, date) = '2023-02-13'
	AND total_deaths is not NULL
GROUP BY location, continent, date, total_deaths
ORDER BY 2

SELECT continent, location, MAX(CAST(total_deaths as int)) as Total_Deaths_Count
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not NULL	
	AND total_deaths is not NULL
GROUP BY location, continent
ORDER BY 2

UPDATE PortfolioProject..['2023_CovidDeaths$']
SET new_deaths = 0 
WHERE new_deaths is NULL

-- CREATE ROLLING COUNT OF NEW DEATHS TO RECALCULATE TOTAL DEATHS

WITH tot_deaths_corr_tab AS
(
SELECT  location, SUM(CAST(new_deaths AS INT)) OVER (Partition by location ORDER BY location, date) AS tot_deaths_corr
FROM PortfolioProject..['2023_CovidDeaths$']
WHERE continent is not null
)
SELECT location, MAX(tot_deaths_corr)
FROM tot_deaths_corr_tab
GROUP BY location
HAVING MAX(tot_deaths_corr) > 0
ORDER BY 1
-- THE NUMBERS DO NOT MATCH, LIKELY DO TO SOME ADJUSTMENT IN REPORTING DONE AT THE SOURCE
-- I.E. IN SOME CASES, THE TOTAL DEATHS COUNT REPORTED IS DECREASED WITHOUT EXPLANANTION, LIKELY DUE TO CORRECTIONS DONE UPON INVESTIGATION OF CASES

-- TABLE TO BE EXPORTED TO TABLEAU
SELECT *, (cde.total_deaths/cde.total_cases)*100 AS DeathRatio, (cde.total_cases/cde.population)*100 AS '%Infected'
FROM PortfolioProject..['2023_CovidDeaths$'] cde
JOIN PortfolioProject..['2023_CovidVacc$'] cvac
ON cde.location = cvac.location
	and cde.date = cvac.date