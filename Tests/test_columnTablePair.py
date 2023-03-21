from Purpose import Purpose
from columntablepair import ColumnTablePair


def test_get_purpose_with_legal_reason_returns_purpose():
    legal_purpose = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    columntablepair = ColumnTablePair("Table", "Column")
    columntablepair.add_purpose(legal_purpose)
    assert columntablepair.get_purposes_with_legal_reason()


def test_get_purpose_with_legal_reason_does_not_return_purpose_with_no_legal_reason():
    non_legal_purpose = Purpose("Name", "TTL", "Origin", "Start_time", 0)
    columntablepair = ColumnTablePair("Table", "Column")
    columntablepair.add_purpose(non_legal_purpose)
    assert not columntablepair.get_purposes_with_legal_reason()


def test_get_purpose_with_legal_reason_returns_correct_purposes():
    legalPurpose = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    anotherlegalPurpose = Purpose("AnotherName", "TTL", "Origin", "Start_time", 1)
    non_legal_purpose = Purpose("Name", "TTL", "Origin", "Start_time", 0)
    columntablepair = ColumnTablePair("Table", "Column")
    columntablepair.add_purpose(legalPurpose)
    columntablepair.add_purpose(anotherlegalPurpose)
    columntablepair.add_purpose(non_legal_purpose)
    assert columntablepair.get_purposes_with_legal_reason()
    assert len(columntablepair.get_purposes_with_legal_reason()) == 2


def test_add_purpose():
    purpose = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    columntablepair = ColumnTablePair("Table", "Column")
    columntablepair.add_purpose(purpose)
    assert len(columntablepair.purposes) == 1
    assert columntablepair.purposes[0] == purpose


def test_add_purpose_does_not_add_purpose_if_its_in_the_list():
    purpose = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    purpose2 = Purpose("Name", "TTL", "Origin", "Start_time", 1)
    columntablepair = ColumnTablePair("Table", "Column")
    columntablepair.add_purpose(purpose)
    columntablepair.add_purpose(purpose2)
    assert len(columntablepair.purposes) == 1
    assert columntablepair.purposes[0] == purpose
