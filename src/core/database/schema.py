SCHEMA = "CREATE SCHEMA IF NOT EXISTS company;"
SET_SCHEMA = "SET SCHEMA 'company';"

COMPANY_DATA_TABLE = """
                     CREATE TABLE IF NOT EXISTS company.company_data( url varchar PRIMARY KEY, 
                                                                      name varchar, 
                                                                      content JSONB,
                                                                      processed_variables JSONB, 
                                                                      imported_date timestamp, 
                                                                      last_processed_date timestamp);
                     """
UPSERT_DATA_IN_BATCH = """
                        INSERT INTO company.company_data (url, name, content, processed_variables, imported_date, last_processed_date)
                        VALUES (%s, %s, %s, %s, %s, %s) ON CONFLICT (url) DO
                        UPDATE
                            SET 
                                name = EXCLUDED.name,
                                content = EXCLUDED.content,
                                processed_variables = EXCLUDED.processed_variables,
                                imported_date = EXCLUDED.imported_date,
                                last_processed_date = EXCLUDED.last_processed_date;
                        """

UPDATE_PROCESSED_DATA = """
                        UPDATE company.company_data SET processed_variables = %s,
                                                        last_processed_date = %s
                                                    WHERE url = %s;                            
                        """

SELECT_COMPANY_BY_URL= "SELECT * FROM company.company_data WHERE url = %s;"
SELECT_PREVIOUSLY_PROCESSED= """
                                SELECT *
                                FROM company.company_data
                                WHERE last_processed_date = (
                                    SELECT MAX(last_processed_date)
                                    FROM company.company_data
                                );
                              """
