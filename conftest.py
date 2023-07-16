import os

import pytest


@pytest.fixture()
def test_resources_root() -> str:
    return os.path.join(f"{os.path.dirname(__file__)}", "tests", "resources")
