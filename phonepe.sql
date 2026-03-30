-- Aggregated Tables
CREATE TABLE IF NOT EXISTS aggregated_transaction (
    state TEXT,
    year INT,
    quarter INT,
    type TEXT,
    count BIGINT,
    amount DOUBLE PRECISION
);

CREATE TABLE  IF NOT EXISTS aggregated_insurance (
    state TEXT,
    year INT,
    quarter INT,
    type TEXT,
    count BIGINT,
    amount DOUBLE PRECISION
);

CREATE TABLE  IF NOT EXISTS aggregated_user (
    state TEXT,
    year INT,
    quarter INT,
    brand TEXT,
    count BIGINT,
    percentage DOUBLE PRECISION
);

DROP TABLE map_transaction;
CREATE TABLE  map_transaction (
    state TEXT,
    year INT,
    quarter INT,
    district TEXT,
    count BIGINT,
    amount DOUBLE PRECISION
);

CREATE TABLE IF NOT EXISTS map_user (
    state TEXT,
    year INT,
    quarter INT,
    district TEXT,
    registeredUsers BIGINT,
    appOpens BIGINT

);
CREATE TABLE IF NOT EXISTS top_transaction (
    state TEXT,
    year INT,
    quarter INT,
    entity BIGINT,
    count BIGINT,
    amount BIGINT

);
CREATE TABLE IF NOT EXISTS top_insurance (
    state TEXT,
    year INT,
    quarter INT,
    entity BIGINT,
    count BIGINT,
    amount BIGINT

);

CREATE TABLE IF NOT EXISTS top_user (
    state TEXT,
    year INT,
    quarter INT,
    entity BIGINT,
    registeredUsers BIGINT

);

SELECT state, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount DESC;

SELECT type, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY type
ORDER BY total_amount DESC;

SELECT year, quarter, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY year, quarter
ORDER BY year, quarter;

SELECT state, 
       SUM(registeredUsers) AS users,
       SUM(appOpens) AS opens
FROM map_user
GROUP BY state
ORDER BY opens DESC;

SELECT state, SUM(amount) AS total_amount
FROM aggregated_transaction
GROUP BY state
ORDER BY total_amount ASC
LIMIT 10;

SELECT state, SUM(amount)
FROM aggregated_transaction
GROUP BY state
ORDER BY SUM(amount) DESC
LIMIT 10;

SELECT entity, SUM(amount)
FROM top_transaction
GROUP BY entity
ORDER BY SUM(amount) DESC
LIMIT 10;

SELECT state, SUM(registeredUsers)
FROM top_user
GROUP BY state
ORDER BY SUM(registeredUsers) DESC;

SELECT COUNT(*) FROM aggregated_insurance;

SELECT COUNT(*) FROM map_insurance;
SELECT COUNT(*) FROM top_insurance;
SELECT * FROM aggregated_insurance LIMIT 5;
SELECT * FROM map_insurance LIMIT 5;
SELECT * FROM top_insurance LIMIT 5;

