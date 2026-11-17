-- 1. Which colleges have the lowers reported new price?

SELECT
    INSTNM,
    CONTROL,
    NET_PRICE,
    C150_4
FROM read_csv_auto('data/processed/college_metrics.csv')
WHERE NET_PRICE IS NOT NULL
ORDER BY NET_PRICE ASC
LIMIT 20;

--2. Wich colleges have the highest completion rates?

SELECT
    INSTNM,
    CONTROL,
    NET_PRICE,
    C150_4
FROM read_csv_auto('data/processed/college_metrics.csv')
WHERE C150_4 IS NOT NULL
ORDER BY C150_4 DESC