import datetime

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


def get_date_format():
    return "%Y-%m-%d %H:%M"


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


def test_time_parser_parses_year():
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    start_date = "2023-03-21 13:14"
    expected_date = '"2021-03-21 13:14"'
    result = vacuumer.ttl_last_date_calculator("2y", datetime.datetime.strptime(start_date, get_date_format()))
    assert result == expected_date


def test_time_parser_parses_month():
    start_date = "2023-03-21 13:14"
    expected_date = '"2023-01-21 13:14"'
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.ttl_last_date_calculator("2m", datetime.datetime.strptime(start_date, get_date_format()))
    assert result == expected_date


def test_time_parser_parses_days():
    start_date = "2023-03-21 13:14"
    expected_date = '"2023-03-19 13:14"'
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.ttl_last_date_calculator("2d", datetime.datetime.strptime(start_date, get_date_format()))

    assert result == expected_date


def test_time_parser_parses_hours():
    start_date = "2023-03-21 13:14"
    expected_date = '"2023-03-21 11:14"'
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.ttl_last_date_calculator("2h", datetime.datetime.strptime(start_date, get_date_format()))

    assert result == expected_date


def test_time_parser_parses_minutes():
    start_date = "2023-03-21 13:14"
    expected_date = '"2023-03-21 13:12"'
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.ttl_last_date_calculator("2M", datetime.datetime.strptime(start_date, get_date_format()))

    assert result == expected_date


def test_time_parser_parses_all_in_one():
    start_date = "2023-03-21 13:14"
    expected_date = '"2021-01-19 11:12"'
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.ttl_last_date_calculator("2y 2m 2d 2h 2M",
                                               datetime.datetime.strptime(start_date, get_date_format()))

    assert result == expected_date


def test_get_number_from_time_component_returns_number():
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.get_number_from_time_component("222d")

    assert result == 222

def test_get_number_from_time_component_no_number_given():
    vacuumer = Vacuumer(MocDBConnection("ConnectionString"), "CreationScript", "MetadataSelectionQuery")
    result = vacuumer.get_number_from_time_component("d")

    assert result is None
