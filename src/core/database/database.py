import psycopg2

from src.core.database.schema import SCHEMA, SET_SCHEMA, COMPANY_DATA_TABLE


class Database:
    """
    A simple wrapper around a psycopg2 PostgreSQL connection to manage
    database connection, schema/table creation, and query execution.
    """
    __connection = None

    def connect(self, host, port, dbname, user, password):
        """
        Establishes a connection to the PostgreSQL database if not already connected
        or if the existing connection is closed.

        Args:
            host (str): Database server hostname or IP.
            port (int): Database server port.
            dbname (str): Database name.
            user (str): Username for authentication.
            password (str): Password for authentication.
        """
        if not self.__connection or self.__connection.closed != 0:
            self.__connection = psycopg2.connect(
                host=host,
                port=port,
                dbname=dbname,
                user=user,
                password=password
            )

    def create_db(self):
        """
        Creates the database schema and tables by executing the respective SQL commands.
        """
        self.__create_schemas()
        self.__create_tables()

    def __create_schemas(self):
        """
        Executes the SQL commands to create the database schemas.
        """
        self.execute(SCHEMA)
        self.execute(SET_SCHEMA)

    def __create_tables(self):
        """
        Executes the SQL command to create the database tables.
        """
        self.execute(COMPANY_DATA_TABLE)

    def fetch_one(self, command, values=None):
        """
        Executes a query and fetches a single row from the result.

        Args:
            command (str): SQL query to execute.
            values (tuple, optional): Parameters for the SQL query.

        Returns:
            tuple: The first row of the query result, or None if no rows.
        """
        cursor = self.__connection.cursor()
        cursor.execute(command, values)
        result = cursor.fetchone()
        cursor.close()
        return result

    def fetch_all(self, command, values=None):
        """
        Executes a query and fetches all rows from the result.

        Args:
            command (str): SQL query to execute.
            values (tuple, optional): Parameters for the SQL query.

        Returns:
            list of tuples: All rows returned by the query.
        """
        cursor = self.__connection.cursor()
        cursor.execute(command, values)
        result = cursor.fetchall()
        cursor.close()
        return result

    def execute(self, command, values: tuple = None):
        """
        Executes a SQL command (INSERT, UPDATE, DELETE, etc.) and commits the transaction.

        Args:
            command (str): SQL command to execute.
            values (tuple, optional): Parameters for the SQL command.

        Returns:
            int: Number of rows affected by the command.
        """
        cursor = self.__connection.cursor()
        cursor.execute(command, values)
        self.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected

    def execute_insert_many(self, command, values: list[tuple]):
        """
        Executes a SQL command multiple times with different parameter sets (bulk insert).

        Args:
            command (str): SQL command to execute.
            values (list of tuples): List of parameter tuples for each execution.

        Returns:
            int: Number of rows affected by the command.
        """
        cursor = self.__connection.cursor()
        cursor.executemany(command, values)
        self.commit()
        rows_affected = cursor.rowcount
        cursor.close()
        return rows_affected

    def commit(self):
        """
        Commits the current transaction to the database.
        """
        self.__connection.commit()
