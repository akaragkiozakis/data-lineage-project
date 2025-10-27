{{ config(materialized='view') }}

-- Real interest rates calculation (Fed Funds Rate - Inflation)
WITH cpi AS (
    SELECT
        DATE_TRUNC('year', observation_date) AS year,
        AVG(value) AS cpi_value,
        ROUND(
            100 * (AVG(value) - LAG(AVG(value)) OVER (ORDER BY DATE_TRUNC('year', observation_date)))
            / LAG(AVG(value)) OVER (ORDER BY DATE_TRUNC('year', observation_date)),
            2
        ) AS inflation_yoy
    FROM {{ ref('fred_clean') }}
    WHERE series_id = 'CPIAUCSL'
    GROUP BY DATE_TRUNC('year', observation_date)
),
fed AS (
    SELECT
        DATE_TRUNC('year', observation_date) AS year,
        ROUND(AVG(value), 2) AS fed_funds_rate
    FROM {{ ref('fred_clean') }}
    WHERE series_id = 'FEDFUNDS'
    GROUP BY DATE_TRUNC('year', observation_date)
)

SELECT
    cpi.year,
    ROUND(cpi.inflation_yoy, 2) AS inflation_rate,
    fed.fed_funds_rate,
    ROUND(fed.fed_funds_rate - cpi.inflation_yoy, 2) AS real_interest_rate
FROM cpi
JOIN fed USING (year)
WHERE cpi.inflation_yoy IS NOT NULL
ORDER BY cpi.year