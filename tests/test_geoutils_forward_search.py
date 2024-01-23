from unittest import mock

import pytest

from real_estate_tools.geoutils import UnsupportedGeoDecoderBackend, forward_search


def test_base():
    with pytest.raises(UnsupportedGeoDecoderBackend):
        forward_search(address="lalala", backend="unsupported backend")


def test_call_locationiq():
    with mock.patch(
        "real_estate_tools.geoutils._forward_search_locationiq"
    ) as mocked_function:
        # Call the function to be tested, passing in the mock object
        forward_search(address="lalala")
        mocked_function.assert_called_once()
