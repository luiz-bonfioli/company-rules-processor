SCHEMA = "CREATE SCHEMA IF NOT EXISTS company;"
SET_SCHEMA = "SET SCHEMA 'company';"

COMPANY_DATA_TABLE = "CREATE TABLE IF NOT EXISTS company.company_data( url varchar PRIMARY KEY, name varchar, content JSONB);"
UPSERT_DATA_IN_BATCH = """
                            INSERT INTO company.company_data (url, name, content)
                            VALUES (%s, %s, %s) ON CONFLICT (url) DO
                            UPDATE
                                SET 
                                    name = EXCLUDED.name,
                                    content = EXCLUDED.content;
                            """

SELECT_COMPANY_BY_URL= "SELECT * FROM company.company_data WHERE url = %s;"