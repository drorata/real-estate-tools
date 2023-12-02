from real_estate_tools.consts import ZP_Data
from real_estate_tools.utils import fetch_properties


def test_get_data_from_ready_response(mocker, complete_result_dict):
    # Create a mocker object
    class DummyResponce:
        def json(self) -> None:
            return complete_result_dict

    rr = mocker.patch("requests.request")
    rr.return_value = DummyResponce()

    # Call the function under test
    result = fetch_properties(1, [2])

    # Assert the result
    assert isinstance(result[0], ZP_Data)


def test_get_data_from_empty_respone(mocker):
    # Create a mocker object
    class DummyResponce:
        def json(self) -> None:
            return {"is_success": False, "message": "some message"}

    rr = mocker.patch("requests.request")
    rr.return_value = DummyResponce()

    # Call the function under test
    result = fetch_properties(1, [2])

    # Assert the result
    assert result == []
