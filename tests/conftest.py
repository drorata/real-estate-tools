import json
import shutil
from pathlib import Path

import pytest

# from real_estate_tools.utils import get_property_detail, fetch_properties
FIXTURE_DIR = Path(__file__).parent.resolve() / "test_files"


@pytest.fixture
def complete_result(tmp_path):
    shutil.copy(FIXTURE_DIR / "complete_result.json", tmp_path)
    return tmp_path / "complete_result.json"


@pytest.fixture
def complete_result_dict(complete_result):
    with open(complete_result, "r") as f:
        return json.load(f)
