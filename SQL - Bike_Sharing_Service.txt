-- CREATING BigQuery Table from Monthly data tables

SELECT 
  *
FROM
  `Bike_Trip_DataSet.202202`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202203`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202204`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202205`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202206`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202207`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202208`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202209`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202210`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202211`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202212`
UNION ALL
SELECT
  *
FROM
  `Bike_Trip_DataSet.202301`

SELECT *
FROM `Bike_Trip_DataSet.Latest_year_simp`;

-- DATA CLEANING AND ANALYSIS (CREATING TABLE FOR TABLEAU)

-- Remove unused columns --

CREATE OR REPLACE TABLE `Bike_Trip_DataSet.Latest_year_simp` 
AS
SELECT ride_id, rideable_type, started_at, ended_at, start_station_name, start_station_id, end_station_name, end_station_id,member_casual
FROM `Bike_Trip_DataSet.Latest_year`;


-- Data view --  5754248 rows (-130885 = 5623363)
SELECT *
FROM `Bike_Trip_DataSet.Latest_year_simp`
--WHERE start_station_name IS NULL;


-- Ride duration --
SELECT ride_id, TIME(TIMESTAMP_SECONDS(TIMESTAMP_DIFF(ended_at, started_at, SECOND))) AS Ride_Duration
FROM `Bike_Trip_DataSet.Latest_year_simp`;

ALTER TABLE `Bike_Trip_DataSet.Latest_year_simp` 
ADD COLUMN Ride_Duration TIME;

UPDATE `Bike_Trip_DataSet.Latest_year_simp` 
SET Ride_Duration = TIME(TIMESTAMP_SECONDS(TIMESTAMP_DIFF(ended_at, started_at, SECOND)))
WHERE TRUE;

-- Drop non-significant rows: Rides shorter than 60 seconds and longer than 24 hours 130867 rows
SELECT ride_id, TIME(TIMESTAMP_SECONDS(TIMESTAMP_DIFF(ended_at, started_at, SECOND))) AS Ride_Duration;
FROM `Bike_Trip_DataSet.Latest_year_simp`
WHERE TIMESTAMP_DIFF(ended_at, started_at, SECOND) < 60 OR TIMESTAMP_DIFF(ended_at, started_at, SECOND) > 84600;

DELETE FROM `Bike_Trip_DataSet.Latest_year_simp`
WHERE TIMESTAMP_DIFF(ended_at, started_at, SECOND) < 60 OR TIMESTAMP_DIFF(ended_at, started_at, SECOND) > 83599;


-- Average Ride Duration by Month -- 
SELECT EXTRACT(YEAR FROM started_at) AS Year, EXTRACT(MONTH FROM started_at) AS Month, TIME(TIMESTAMP_SECONDS(CAST(ROUND(AVG(TIMESTAMP_DIFF(ended_at, started_at, SECOND))) AS INT))) AS Average_Duration
FROM `Bike_Trip_DataSet.Latest_year_simp`
GROUP BY Month, Year
ORDER BY Year, Month;


-- Reformat Data for Easier Reading --> Create date column

ALTER TABLE `Bike_Trip_DataSet.Latest_year_simp` 
ADD COLUMN Ride_Date DATE;

UPDATE `Bike_Trip_DataSet.Latest_year_simp` 
SET Ride_Date = EXTRACT(DATE FROM started_at)
WHERE TRUE;

-- Output day of the week --
ALTER TABLE `Bike_Trip_DataSet.Latest_year_simp` 
ADD COLUMN Ride_Day_Week STRING;


UPDATE `Bike_Trip_DataSet.Latest_year_simp` 
SET Ride_Day_Week = FORMAT_DATE('%A', Ride_Date)
WHERE TRUE;


-- ADD Month Column ---
ALTER TABLE `Bike_Trip_DataSet.Latest_year_simp` 
ADD COLUMN Ride_Month STRING;

UPDATE `Bike_Trip_DataSet.Latest_year_simp` 
SET Ride_Month = FORMAT_DATETIME('%B', DATETIME(Ride_Date))
WHERE TRUE;

--ADD Year Column--

ALTER TABLE `Bike_Trip_DataSet.Latest_year_simp` 
ADD COLUMN Ride_Year NUMERIC;

UPDATE `Bike_Trip_DataSet.Latest_year_simp` 
SET Ride_Year = EXTRACT(YEAR FROM Ride_Date)
WHERE TRUE;

-- Remove Incomplete Data (no station data)--

SELECT *
FROM `Bike_Trip_DataSet.Latest_year_simp` 
WHERE
start_station_id is NULL 
OR 
start_station_name IS NULL
OR
end_station_name IS NULL
OR
end_station_id IS NULL;


