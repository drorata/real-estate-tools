import pytest

from real_estate_tools.geoutils import _forward_search_locationiq


def test_faulty_call():
    with pytest.raises(RuntimeError):
        _forward_search_locationiq("")


def test_valid_call():
    result = _forward_search_locationiq("Brandenburger Tor")
    assert isinstance(result, dict)
