from real_estate_tools.consts import ZP_Data


def test_allowed_lotAreaUnits():
    data = {
        "zpid": 11306973,
        "city": "Pittsburgh",
        "streetAddress": "831 Londonderry Dr",
        "state": "PA",
        "homeStatus": "RECENTLY_SOLD",
        "homeType": "SINGLE_FAMILY",
        "price": 175500,
        "yearBuilt": 1955,
        "lotAreaUnits": "Square Feet",
        "lotAreaValue": 9713.88,
        "livingArea": 1442,
        "bedrooms": 3,
        "bathrooms": 2,
        "priceHistory": None,
        "description": "Some description",
        "latitude": 40.37749,
        "longitude": -80.009445,
        "photos": None,
    }

    data_obj = ZP_Data(**data)
    assert data_obj


def test_not_allowed_lotAreaUnits():
    data = {
        "zpid": 11306973,
        "city": "Pittsburgh",
        "streetAddress": "831 Londonderry Dr",
        "state": "PA",
        "homeStatus": "RECENTLY_SOLD",
        "homeType": "SINGLE_FAMILY",
        "price": 175500,
        "yearBuilt": 1955,
        "lotAreaUnits": "Not allowed value",
        "lotAreaValue": 9713.88,
        "livingArea": 1442,
        "bedrooms": 3,
        "bathrooms": 2,
        "priceHistory": None,
        "description": "Some description",
        "latitude": 40.37749,
        "longitude": -80.009445,
        "photos": None,
    }

    data_obj = ZP_Data(**data)
    assert data_obj
    assert data_obj.lotAreaValue is None
    assert data_obj.lotAreaUnits == "Not allowed value"
