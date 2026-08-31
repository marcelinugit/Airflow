CREATE OR REPLACE TABLE `{project_id}.{system}_bronze.{table}` AS
WITH base AS (
  SELECT
      *,
      CURRENT_DATE() AS ingestion_date_bronze,
      CURRENT_TIMESTAMP() AS ingestion_timestamp_bronze
  FROM `{project_id}.{system}_raw.{table}`
),
dedup AS (
  SELECT
    *,
    ROW_NUMBER() OVER (
      PARTITION BY {pk}
      ORDER BY ingestion_timestamp_bronze DESC
    ) AS rn
  FROM base
)

SELECT
  * EXCEPT(rn)
FROM dedup
WHERE rn = 1;