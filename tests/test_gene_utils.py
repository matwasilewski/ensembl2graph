import os

import pytest
from gff3 import Gff3

from src.ensembl_ingest.utils.gene_utils import get_line_idx_2_entity_id_maps


@pytest.fixture()
def subset_genome_path(test_resources_root):
    return os.path.join(test_resources_root,
                        "Aegilops_tauschii_subset.gff")


@pytest.fixture()
def test_gff_object(subset_genome_path: str) -> Gff3:
    yield Gff3(subset_genome_path)


def test_extract_ids_from_gff(test_gff_object: Gff3) -> None:
    line_idx_2_entity_id, entity_id_2_line_idx = get_line_idx_2_entity_id_maps(test_gff_object)
    assert len(line_idx_2_entity_id) == 24
    assert len(entity_id_2_line_idx) == 14
