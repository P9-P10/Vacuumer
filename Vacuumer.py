import datetime
import re

from dateutil.relativedelta import relativedelta

from DatabaseConnections.databaseconnection import DatabaseConnection
from DatabaseConnections.sqlite_connection import SqliteConnection
from Purpose import Purpose
from columntablepair import ColumnTablePair


class Vacuumer:
    def __init__(self, db_connection: DatabaseConnection, sql_creation_script, metadata_selection_query):
        self.connection = db_connection
        self.initiate_database(sql_creation_script)
        self.table_column_meta_data = {}
        self.metadata_selection_query = metadata_selection_query

    def initiate_database(self, database_creation_script):
        self.connection.run_script(database_creation_script)

    def run(self):
        query_result = self.connection.run_query(self.metadata_selection_query)
        self.populate_table_column_metadata(query_result)
        self.delete_expired_tuples()

    def delete_expired_tuples(self):
        results = {}
        for _, columntablepair in self.table_column_meta_data.items():
            for purpose in columntablepair.purposes:
                query = f"SELECT {columntablepair.column}, Creation_date " \
                        f"FROM {columntablepair.table} " \
                        f"JOIN ({purpose.start_time}) " \
                        f"WHERE Creation_date < {self.ttl_last_date_calculator(purpose.ttl)} " \
                        f"AND uid = id;"
                results[self.ttl_last_date_calculator(purpose.ttl)] = self.connection.run_query(query)
        print(results)

    def populate_table_column_metadata(self, query_result: [(str, str, str, str, int, str, str)]):
        for (purpose_name, ttl, target_table, target_column, legally_required, origin, start_time) in query_result:
            purpose = Purpose(purpose_name, ttl, origin, start_time, legally_required)
            self.add_or_update_dict(purpose, target_table, target_column)

    def ttl_last_date_calculator(self, input_string: str, start_date: datetime.datetime = datetime.datetime.now(),
                                 date_format="%Y-%m-%d %H:%M"):
        years = 0
        months = 0
        days = 0
        hours = 0
        minutes = 0
        components = input_string.split(" ")
        for component in components:
            component_num = self.get_number_from_time_component(component)
            if "y" in component:
                years = component_num
            if "m" in component:
                months = component_num
            if "d" in component:
                days = component_num
            if "h" in component:
                hours = component_num
            if "M" in component:
                minutes = component_num

        relative_delta = relativedelta(years=years, months=months, days=days, hours=hours, minutes=minutes)
        ttl_date = start_date - relative_delta
        return '"' + ttl_date.strftime(date_format) + '"'

    @staticmethod
    def get_number_from_time_component(input_string) -> int:
        match = re.findall(r'\d+', input_string)
        if len(match) > 0:
            return int(match[0])
        return None

    def add_or_update_dict(self, purpose: Purpose, target_table: str, target_column: str):
        dict_name = target_table + target_column
        if dict_name in self.table_column_meta_data:
            self.table_column_meta_data[dict_name].add_purpose(purpose)
        else:
            md = ColumnTablePair(target_table, target_column)
            md.add_purpose(purpose)
            self.table_column_meta_data[dict_name] = md


if __name__ == "__main__":
    connection = SqliteConnection("sqlite.sql")
    script = open("metadata_tables_creation.sql", "r").read()
    metadata_selection_script = "SELECT purpose, " \
                                "ttl, " \
                                "target_table, " \
                                "target_column, " \
                                "legally_required, " \
                                "origin, " \
                                "start_time " \
                                "FROM gdpr_metadata " \
                                "ORDER BY target_table,target_column;"
    vacuumer = Vacuumer(connection, script, metadata_selection_script)
    vacuumer.run()
