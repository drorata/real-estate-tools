from real_estate_tools.utils import area_to_sqft


def test_sqft():
    assert area_to_sqft(unit="Square feet", value=5.3) == 5.3


def test_non_supported():
    assert area_to_sqft(unit="Some non-supported unit", value=5.3) == 0
