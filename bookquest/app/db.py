import MySQLdb
import re


class DatabaseManager:

    def __init__(self, host, user, password, db):
        self.host = host
        self.user = user
        self.password = password
        self.db = db
        self.connection = None

    def connect(self):
        try:
            self.connection = MySQLdb.connect(
                host=self.host,
                user=self.user,
                password=self.password,
                db=self.db
            )
        except MySQLdb.Error as e:
            print(f"Connection error: {e}")
            self.connection = None

    def disconnect(self):
        if self.connection:
            try:
                self.connection.close()
                self.connection = None
            except MySQLdb.Error as e:
                print(f"Disconnection error: {e}")

    def __validate_query(self, query, query_type):
        valid_commands = {
            "select": "SELECT",
            "insert": "INSERT INTO",
            "update": "UPDATE",
            "delete": "DELETE FROM"
        }

        command = query.strip().split()[0].upper()
        if command != valid_commands.get(query_type, "").upper():
            raise ValueError(f"Query {query_type} is not valid or secure.")

        if re.search(r"(--|\bDROP\b|\bTRUNCATE\b)", query, re.IGNORECASE):
            raise ValueError("The query contains dangerous keywords.")

    def __execute_query(self, query, params, query_type):
        self.__validate_query(query, query_type)
        try:
            with self.connection.cursor() as cursor:
                cursor.execute(query, params)
                if query_type == "select":
                    return cursor.fetchall()
                else:
                    self.connection.commit()
        except MySQLdb.Error as e:
            print(
                f"Error during query execution {query_type.upper()}: {e}")
            if query_type != "select":
                self.connection.rollback()

    def execute_select(self, query, params=None):
        return self.__execute_query(query, params, "select")

    def execute_insert(self, query, params=None):
        self.__execute_query(query, params, "insert")

    def execute_update(self, query, params=None):
        self.__execute_query(query, params, "update")

    def execute_delete(self, query, params=None):
        self.__execute_query(query, params, "delete")
