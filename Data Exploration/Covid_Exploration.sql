--SELECT *
--FROM covid_deaths
--ORDER BY 3,4 ;

/* 
SELECT *
FROM covid_vaccinations
ORDER BY 3,4; 
*/

SELECT location, date, total_cases, new_cases, total_deaths, population
FROM covid_deaths
ORDER BY 1,2;

-- Examining Daily Total Cases vs Total Deaths
SELECT location, date, total_cases, total_deaths, (total_deaths/total_cases)*100 AS death_percentage 
FROM covid_deaths
WHERE continent IS NOT NULL
ORDER BY 1,2;

-- Examining at Daily Total Cases vs Population
SELECT location, date, total_cases, population, (total_cases/population)*100 AS infection_rate 
FROM covid_deaths
WHERE continent IS NOT NULL
ORDER BY 1,2;


-- Finding countries with the Highest Infection rate compared to population
SELECT location, population, MAX(total_cases) AS highest_cases_count, MAX((total_cases/population))*100 AS highest_infection_rate 
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY highest_infection_rate DESC;

-- Finding countries with the Highest Death count 
SELECT location, MAX(CAST(total_deaths AS int)) AS total_death_count
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY location
ORDER BY total_death_count DESC;


-- Finding continents with the Highest Death count 
SELECT location, MAX(CAST(total_deaths AS int)) AS total_death_count
FROM covid_deaths
WHERE continent IS NULL
GROUP BY location
ORDER BY total_death_count DESC;

-- Daily number of new cases and death (global)
SELECT 
	date, 
	SUM(new_cases) AS global_new_cases, 
	SUM(CAST(new_deaths AS int)) AS global_new_deaths, 
	SUM(CAST(new_deaths AS int))/SUM(new_cases)*100 AS global_death_percentage
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY date
ORDER BY 1,2;

-- Total number of new cases and death (global) -- 05 Jun 2021
SELECT  
	SUM(new_cases) AS total_cases, 
	SUM(CAST(new_deaths AS int)) AS total_deaths, 
	SUM(CAST(new_deaths AS int))/SUM(new_cases)*100 AS total_death_percentage
FROM covid_deaths
WHERE continent IS NOT NULL
ORDER BY 1,2;



-- Total Population vs Vaccinations
WITH pop_vs_vac (continent, location, date, population, new_vaccinations, cumulative_vaccinations)
AS 
	(SELECT 
		dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
		SUM(CAST(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS cumulative_vaccinations
	FROM covid_deaths dea
	JOIN covid_vaccinations vac
	ON dea.location = vac.location AND dea.date = vac.date
	WHERE dea.continent IS NOT NULL)
SELECT *, (cumulative_vaccinations/population)*100 AS vaccinations_rate
FROM pop_vs_vac


-- Create temp table
DROP TABLE IF EXISTS #percent_population_vaccinated
CREATE TABLE #percent_population_vaccinated
(
	continent nvarchar(255),
	location nvarchar(255),
	date datetime,
	population numeric,
	new_vaccinations numeric,
	cumulative_vaccinations numeric
								);

INSERT INTO #percent_population_vaccinated
SELECT 
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(CAST(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS cumulative_vaccinations
FROM covid_deaths dea
JOIN covid_vaccinations vac
ON dea.location = vac.location AND dea.date = vac.date;

SELECT *, cumulative_vaccinations/population*100 AS cumulative_vaccination_rates
FROM  #percent_population_vaccinated;


-- Creating view to store data for visualizations
DROP VIEW IF EXISTS percent_population_vaccinated
CREATE VIEW percent_population_vaccinated AS
SELECT 
	dea.continent, dea.location, dea.date, dea.population, vac.new_vaccinations,
	SUM(CAST(vac.new_vaccinations as int)) OVER (PARTITION BY dea.location ORDER BY dea.location, dea.date) AS cumulative_vaccinations
FROM covid_deaths dea

JOIN covid_vaccinations vac
ON dea.location = vac.location AND dea.date = vac.date
WHERE dea.continent IS NOT NULL;


-- FOR EXCEL AND TABLEAU

-- 1. Total number of new cases and death (global) -- 05 Jun 2021
SELECT  
	SUM(new_cases) AS total_cases, 
	SUM(CAST(new_deaths AS int)) AS total_deaths, 
	SUM(CAST(new_deaths AS int))/SUM(new_cases)*100 AS total_death_percentage
FROM covid_deaths
WHERE continent IS NOT NULL

ORDER BY 1,2;

-- 2.Finding continents with the Highest Death count 
SELECT location, MAX(CAST(total_deaths AS int)) AS total_death_count
FROM covid_deaths
WHERE continent IS NULL
AND location NOT IN ('World', 'European Union','International')
GROUP BY location
ORDER BY total_death_count DESC;

-- 3. Finding countries with the Highest Infection rate compared to population
SELECT location, population, MAX(total_cases) AS highest_cases_count, MAX((total_cases/population))*100 AS highest_infection_rate 
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY location, population
ORDER BY highest_infection_rate DESC;

-- 4.
SELECT location, population, date, MAX(total_cases) AS highest_cases_count, MAX((total_cases/population))*100 AS highest_infection_rate 
FROM covid_deaths
WHERE continent IS NOT NULL
GROUP BY location, population, date
ORDER BY highest_infection_rate DESC;