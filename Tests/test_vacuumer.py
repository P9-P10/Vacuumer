from DatabaseConnections.databaseconnection import DatabaseConnection
from Purpose import Purpose
from Vacuumer import Vacuumer


class MocDBConnection(DatabaseConnection):
    def __init__(self, connection_string):
        super().__init__(connection_string)

    def run_query(self, query):
        pass

    def run_script(self, query):
        pass


def test_add_or_update_dict_adds_element_if_not_present():
    table_name = "Table"
    column_name = "Column"
    purpose = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    dict_name = table_name + column_name
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    vacuumer.add_or_update_dict(purpose, table_name, column_name)
    assert len(vacuumer.table_column_meta_data) == 1
    assert purpose in vacuumer.table_column_meta_data[dict_name].purposes


def test_add_or_update_dict_updates_element_if_present():
    table_name = "Table"
    column_name = "Column"
    dict_name = table_name + column_name
    purpose = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    purpose2 = Purpose("AnotherName", "TTL", "Origin", "Start_time", 0)
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")

    vacuumer.add_or_update_dict(purpose, table_name, column_name)
    vacuumer.add_or_update_dict(purpose2, table_name, column_name)

    assert len(vacuumer.table_column_meta_data) == 1
    assert purpose in vacuumer.table_column_meta_data[dict_name].purposes
    assert purpose2 in vacuumer.table_column_meta_data[dict_name].purposes
