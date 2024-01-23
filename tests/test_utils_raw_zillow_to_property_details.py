import json
from pathlib import Path

import pytest

from real_estate_tools.consts import PropertyDetails
from real_estate_tools.utils import raw_zillow_to_property_details

FIXTURE_DIR = Path(__file__).parent.resolve() / "test_files"


@pytest.mark.datafiles(FIXTURE_DIR / "raw_results.json")
def test_base(datafiles):
    with open(Path(datafiles) / "raw_results.json", "r") as f:
        data = json.load(f)
    for item in data:
        assert isinstance(raw_zillow_to_property_details(item), PropertyDetails)
