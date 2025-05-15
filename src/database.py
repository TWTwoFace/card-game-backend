import psycopg2

from src.config.env import DB_HOST, DB_PORT, DB_NAME, DB_PASSWORD, DB_USERNAME


class Database:

    def __init__(self):
        self._connection = psycopg2.connect(
            dbname=DB_NAME, host=DB_HOST,
            port=DB_PORT, user=DB_USERNAME,
            password=DB_PASSWORD)

    def execute_query(self, query: str):
        with self._connection.cursor() as cursor:
            cursor.execute(query)
            response = cursor.fetchall()
        return response

    def commit(self):
        self._connection.commit()

    def __del__(self):
        self._connection.close()

database = Database()
