import sqlite3

from DatabaseConnections.databaseconnection import DatabaseConnection


class SqliteConnection(DatabaseConnection):
    def __init__(self, connection_string):
        super().__init__(connection_string)
        self.connection = sqlite3.connect(self.connection_string)

    def run_query(self, query):
        output = self.connection.execute(query)
        self.connection.commit()
        rows = output.fetchall()
        return rows

    def run_script(self, query):
        self.connection.executescript(query)
        self.connection.commit()
