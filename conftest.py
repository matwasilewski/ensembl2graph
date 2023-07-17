import os

import pytest


@pytest.fixture()
def test_resources_root() -> str:
    return os.path.join(f"{os.path.dirname(__file__)}", "tests", "resources")


@pytest.fixture()
def subset_genome_path(test_resources_root):
    return os.path.join(test_resources_root, "Aegilops_tauschii_subset.gff")
