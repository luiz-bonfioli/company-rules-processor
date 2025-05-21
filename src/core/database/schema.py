SCHEMA = "CREATE SCHEMA IF NOT EXISTS company;"
SET_SCHEMA = "SET SCHEMA 'company';"

COMPANY_DATA_TABLE = "CREATE TABLE IF NOT EXISTS company.company_data( id uuid PRIMARY KEY, job_id uuid, content JSONB);"
INSERT_DATA_IN_BATCH = "INSERT INTO company.company_data (id, job_id, content) VALUES (%s, %s, %s);"

COMPANY_TABLE = "CREATE TABLE IF NOT EXISTS company.company( id uuid PRIMARY KEY, name varchar);"
INSERT_COMPANIES_IN_BATCH = "INSERT INTO company.company (id, name) VALUES (%s, %s);"
