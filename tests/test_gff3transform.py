import os.path

import pytest

from src.ensembl_ingest.gff3transform import GFF3Genome


@pytest.fixture()
def sample_gz_genome_path(test_resources_root):
    return os.path.join(
        test_resources_root, "Aegilops_tauschii.Aet_v4.0.56.gff3.gz"
    )


@pytest.mark.skip(reason="Takes long to run")
def test_unpacking_gz(sample_gz_genome_path: str) -> None:
    gff3 = GFF3Genome(sample_gz_genome_path)
    assert len(gff3._genome_gff3.lines) == 4107556


def test_parse_subset(subset_genome_path: str) -> None:
    gff3 = GFF3Genome(subset_genome_path)
    assert len(gff3._genome_gff3.lines) == 24


def test_parse_to_node_link(subset_genome_path: str) -> None:
    gff3 = GFF3Genome(subset_genome_path)
    gff3.transform_to_node_link()
    assert len(gff3.nodes) == 14
    assert len(gff3.links) == 10
