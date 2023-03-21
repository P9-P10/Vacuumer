from Purpose import Purpose
from columntablepair import ColumnTablePair
from DatabaseConnections.databaseconnection import DatabaseConnection
from DatabaseConnections.sqlite_connection import SqliteConnection


class Vacuumer:
    def __init__(self, db_connection: DatabaseConnection):
        self.connection = db_connection
        script = open("metadata_tables_creation.sql", "r").read()
        self.initiator(script)
        self.table_column_meta_data = {}

    def initiator(self,database_creation_script):
        self.connection.run_script(database_creation_script)

    def run(self):
        query_result = self.connection.run_query(
            "SELECT purpose,"
            "ttl,"
            "target_table,"
            "target_column,"
            "legally_required,"
            "origin,"
            "start_time FROM gdpr_metadata ORDER BY target_table,target_column;")
        self.populate_table_column_metadata(query_result)
        self.deleter()
        print("Woo")

    def deleter(self):
        for key, columntablepair in self.table_column_meta_data.items():
            purpose_with_legal_reason = columntablepair.get_purposes_with_legal_reason()
            if purpose_with_legal_reason:
                print("Got here")
            else:
                print("Also got here")

    def populate_table_column_metadata(self, query_result: [(str, str, str, str, int, str, str)]):
        for (purpose_name, ttl, target_table, target_column, legally_required, origin, start_time) in query_result:
            dict_name = target_table + target_column
            purpose = Purpose(purpose_name, ttl, origin, start_time, legally_required)
            self.add_or_update_dict(dict_name, purpose, target_column, target_table)

    def add_or_update_dict(self, dict_name, purpose, target_column, target_table):
        if dict_name in self.table_column_meta_data:
            self.table_column_meta_data[dict_name].add_purpose(purpose)
        else:
            md = ColumnTablePair(target_table, target_column)
            md.add_purpose(purpose)
            self.table_column_meta_data[dict_name] = md


if __name__ == "__main__":
    connection = SqliteConnection("sqlite.sql")
    vacuumer = Vacuumer(connection)
    vacuumer.run()
