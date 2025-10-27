{{ config(materialized='view') }}

SELECT
    series_id,

    -- Καθαρό, business-friendly όνομα δείκτη
    CASE
        WHEN series_id = 'GDPC1' THEN 'Real GDP (Billions $)'
        WHEN series_id = 'CPIAUCSL' THEN 'Consumer Price Index (1982-1984=100)'
        WHEN series_id = 'PCE' THEN 'Personal Consumption Expenditures (Billions)'
        WHEN series_id = 'UNRATE' THEN 'Unemployment Rate (%)'
        WHEN series_id = 'INDPRO' THEN 'Industrial Production (2017=100)'
        WHEN series_id = 'FEDFUNDS' THEN 'Federal Funds Rate (%)'
        ELSE indicator_name
    END AS indicator_name,
    TRY_TO_DATE(observation_date) AS observation_date,
    TRY_TO_DOUBLE(value) AS value,
    file_load_date

FROM {{ source('raw', 'fred_data') }}
WHERE value IS NOT NULL
