import psycopg2

from src.core.database.schema import SCHEMA, SET_SCHEMA, COMPANY_DATA_TABLE


class Database:
    __connection = None

    def connect(self, host, port, dbname, user, password):
        if not self.__connection or self.__connection.closed != 0:
            self.__connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )

    def create_db(self):
        self.__create_schemas()
        self.__create_tables()

    def __create_schemas(self):
        self.execute(SCHEMA)
        self.execute(SET_SCHEMA)

    def __create_tables(self):
        self.execute(COMPANY_DATA_TABLE)

    def execute(self, command, values=None):
        cursor = self.__connection.cursor()
        cursor.execute(command, values)
        self.commit()
        cursor.close()

    def fetch_one(self, command, values=None):
        cursor = self.__connection.cursor()
        cursor.execute(command, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def execute_insert(self, command, values):
        cursor = self.__connection.cursor()
        cursor.execute(command, values)
        self.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected

    def execute_insert_many(self, command, values: list[tuple]):
        cursor = self.__connection.cursor()
        cursor.executemany(command, values)
        self.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected

    def commit(self):
        self.__connection.commit()
