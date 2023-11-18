from real_estate_tools.utils import clean_zpid


def test_simple():
    input_zpid = "12344_ZPID"
    result = clean_zpid(input_zpid)
    expected_res = "12344"

    assert result == expected_res


def test_null_case():
    input_zpid = "12344"
    result = clean_zpid(input_zpid)
    expected_res = "12344"

    assert result == expected_res
