from real_estate_tools import consts, utils


def test_base():
    property = consts.PropertyDetails(
        lot_area=10,
        living_area=200,
        address="foo bar",
        full_address="foo bar",
        lat=10,
        lon=11,
        baths=2,
        rooms=3,
        garages=0,
        built_year=1900,
        listed_date="2023-01-01",
        listed_price=100_000,
    )

    result = utils.properties_to_df([property, property])

    assert result.shape[0] == 2

    expected_cols = set(consts.PropertyDetails.model_fields)
    assert set(result.columns) == expected_cols


def test_single_property():
    property = consts.PropertyDetails(
        lot_area=10,
        living_area=200,
        address="foo bar",
        full_address="foo bar",
        lat=10,
        lon=11,
        baths=2,
        rooms=3,
        garages=0,
        built_year=1900,
        listed_date="2023-01-01",
        listed_price=100_000,
    )

    result = utils.properties_to_df([property])

    assert result.shape[0] == 1

    expected_cols = set(consts.PropertyDetails.model_fields)
    assert set(result.columns) == expected_cols
