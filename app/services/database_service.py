import mysql.connector
from mysql.connector import Error

class DatabaseService:
    """
    A class to interact with a MySQL database.
    Handles database connections and provides methods to execute queries.
    """
    def __init__(self, host: str, user: str, password: str, database: str):
        """
        Initializes the DatabaseService class with database connection details.

        Args:
            host (str): Database host address.
            user (str): Database username.
            password (str): Database password.
            database (str): Name of the database.
        """
        self.host = host
        self.user = user
        self.password = password
        self.database = database
        self.connection = None

    def connect(self):
        """
        Establishes a connection to the MySQL database.
        """
        try:
            self.connection = mysql.connector.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                database=self.database
            )
            print("Connected to the database successfully!")
        except Error as e:
            print(f"Error connecting to the database: {e}")

    def disconnect(self):
        """
        Closes the connection to the MySQL database.
        """
        if self.connection and self.connection.is_connected():
            self.connection.close()
            print("Database connection closed.")

    def execute_query(self, query: str, params: tuple = None):
        """
        Executes a SQL query and returns the results.

        Args:
            query (str): The SQL query to execute.
            params (tuple): Optional parameters for the query.

        Returns:
            list: A list of rows returned by the query.
        """
        if not self.connection or not self.connection.is_connected():
            print("Error: No active database connection.")
            return None

        cursor = None
        try:
            cursor = self.connection.cursor()
            cursor.execute(query, params or ())
            result = cursor.fetchall()
            return result
        except Error as e:
            print(f"Error executing query: {e}")
            return None
        finally:
            if cursor:
                cursor.close()