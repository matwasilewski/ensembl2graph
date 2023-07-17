import os.path

import pytest

from src.ensembl_ingest.gff3transform import GFF3Genome


@pytest.fixture()
def sample_gz_genome_path(test_resources_root):
    return os.path.join(test_resources_root,
                        "Aegilops_tauschii.Aet_v4.0.56.gff3.gz")


def test_unpacking_gz(sample_gz_genome_path: str) -> None:
    gff3 = GFF3Genome(sample_gz_genome_path)
