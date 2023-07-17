import os.path

import pytest

from src.ensembl_ingest.gff3transform import GFF3Genome


@pytest.fixture()
def sample_gz_genome_path(test_resources_root):
    return os.path.join(
        test_resources_root, "Aegilops_tauschii.Aet_v4.0.56.gff3.gz"
    )


@pytest.fixture()
def gff3_full(sample_gz_genome_path):
    gff3 = GFF3Genome(sample_gz_genome_path)
    return gff3


@pytest.fixture()
def gff3_subset(subset_genome_path: str) -> GFF3Genome:
    gff3 = GFF3Genome(subset_genome_path)
    yield gff3


@pytest.mark.skip(reason="Takes long to run")
def test_unpacking_gz(gff3_full) -> None:
    assert len(gff3_full._genome_gff3.lines) == 4107556


def test_parse_subset(gff3_subset) -> None:
    assert len(gff3_subset._genome_gff3.lines) == 24


def test_parse_to_node_link(gff3_subset) -> None:
    gff3_subset.transform_to_node_link()
    assert len(gff3_subset.nodes) == 14
    assert len(gff3_subset.links) == 10


def test_verify_if_all_nodes_from_links_exist(gff3_subset) -> None:
    nodes = [{"id": "child_id", "meta": "lorem"},
             {"id": "parent_id", "meta": "ipsum"}]
    links = [{"source": "child_id", "target": "parent_id"}]
    gff3_subset.verify_nodes_exist(nodes, links)


def test_exception_raised_if_node_from_links_does_not_exist(
        gff3_subset: GFF3Genome) -> None:
    nodes = [{"id": "child_id", "meta": "lorem"},
             {"id": "parent_id", "meta": "ipsum"}]
    links = [{"source": "child_id", "target": "other_parent_id"}]
    with pytest.raises(RuntimeError):
        gff3_subset.verify_nodes_exist(nodes, links)
