SELECT * 
FROM PortfolioProject..['Covid_deaths']
order by 3,4

SELECT *
	FROM PortfolioProject..['Covid_vaccinations']
	order by 3,4

SELECT Location, date, total_cases, new_cases, total_deaths, population
	FROM PortfolioProject..['Covid_deaths']
	order by 1,2

SELECT Location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS "D/C ratio"
	FROM PortfolioProject..['Covid_deaths']
	WHERE location like '%italy%'
	order by 1,2

SELECT Location, date, total_cases, total_deaths, (total_cases/population)*100 AS "% pop infected"
	FROM PortfolioProject..['Covid_deaths']
	WHERE location like '%italy%'
	order by 1,2


SELECT Location, Population, MAX(total_cases) as total_cases, MAX((total_cases/population)*100) AS "% pop infected"
	FROM PortfolioProject..['Covid_deaths']
	GROUP BY Location, Population 
	ORDER BY "% pop infected" desc


SELECT Location, MAX(cast(total_deaths as int)) as total_deaths, MAX((total_deaths/population)*100) AS "% pop dead"
	FROM PortfolioProject..['Covid_deaths']
	WHERE continent is not NULL
	GROUP BY Location 
	ORDER BY "% pop dead" desc


SELECT continent, MAX(cast(total_deaths as int)) as total_deaths, MAX((total_deaths/population)*100) AS "% pop dead"
	FROM PortfolioProject..['Covid_deaths']
	WHERE continent is not NULL
	GROUP BY continent 
	ORDER BY "% pop dead" desc


SELECT date, sum(population) as total_population, sum(cast(new_cases as int)) as tot_new_cases,
		sum(cast(new_deaths as int)) as tot_new_deaths,
		(sum(cast(new_deaths as int))/sum(population))*100 as deaths_percentage 
	FROM PortfolioProject..['Covid_deaths']
	WHERE continent is not NULL
	GROUP BY date
	ORDER BY date

SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) AS vaccinations_as_of_date
	--,(vaccinations_as_of_date/dea.population)*100 AS perc_pop_vaccinated
FROM PortfolioProject..['Covid_deaths'] dea
JOIN PortfolioProject..['Covid_vaccinations'] vac
	ON dea.location = vac.location
		and dea.date = vac.date
	WHERE dea.continent is not NULL
	ORDER BY 2,3



	----CTE ----

With PopvVac (Continent, Location, Date, Population, New_vaccinations, vaccinations_as_of_date)
as
(
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) AS vaccinations_as_of_date
	--,(vaccinations_as_of_date/dea.population)*100 AS perc_pop_vaccinated
FROM PortfolioProject..['Covid_deaths'] dea
JOIN PortfolioProject..['Covid_vaccinations'] vac
	ON dea.location = vac.location
		and dea.date = vac.date
	WHERE dea.continent is not NULL
	--ORDER BY 2,3
)
Select *, (vaccinations_as_of_date/Population)*100 as perc_pop_vaccinated
FROM PopvVac
WHERE Location like '%canada%'


	----Temp Table ----
DROP TABLE IF EXISTS #ppv
CREATE TABLE #ppv
(
Continent nvarchar(255),
Location nvarchar(255),
Date datetime,
Population numeric,
New_vaccinations numeric,
Vaccinations_as_of_date numeric
)
INSERT INTO #ppv
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location ORDER BY dea.location, dea.date) AS vaccinations_as_of_date
	--,(vaccinations_as_of_date/dea.population)*100 AS perc_pop_vaccinated
FROM PortfolioProject..['Covid_deaths'] dea
JOIN PortfolioProject..['Covid_vaccinations'] vac
	ON dea.location = vac.location
		and dea.date = vac.date
	WHERE dea.continent is not NULL
	--ORDER BY 2,3

Select *, (vaccinations_as_of_date/Population)*100 as perc_pop_vaccinated
FROM #ppv
WHERE Location like '%canada%'


	-- Create VIEW --
DROP VIEW IF EXISTS ppv
CREATE VIEW ppv AS
SELECT dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(cast(vac.new_vaccinations as bigint)) OVER (Partition by dea.location 
		ORDER BY dea.location, dea.date) AS vaccinations_as_of_date
	--,(vaccinations_as_of_date/dea.population)*100 AS perc_pop_vaccinated
FROM PortfolioProject..['Covid_deaths'] dea
JOIN PortfolioProject..['Covid_vaccinations'] vac
	ON dea.location = vac.location
		and dea.date = vac.date
	WHERE dea.continent is not NULL
	--ORDER BY 2,3

SELECT * 
from ppv