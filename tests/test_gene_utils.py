import os

import pytest
from gff3 import Gff3

from src.ensembl_ingest.utils.gene_utils import (
    get_line_idx_2_entity_id_maps,
    get_node_and_rel_from_record,
)


@pytest.fixture()
def test_gff_object(subset_genome_path: str) -> Gff3:
    yield Gff3(subset_genome_path)


def test_extract_ids_from_gff(test_gff_object: Gff3) -> None:
    line_idx_2_entity_id, entity_id_2_line_idx = get_line_idx_2_entity_id_maps(
        test_gff_object
    )
    assert len(line_idx_2_entity_id) == 24
    assert len(entity_id_2_line_idx) == 14


def test_extract_information_from_gene_from_gff(test_gff_object: Gff3) -> None:
    gene_record = test_gff_object.lines[7]
    node, rels = get_node_and_rel_from_record(gene_record)
    assert node.get("type", None) == "gene"
    assert node.get("seqid", None) == "2D"
    assert node.get("source", None) == "PGSB"
    assert node.get("start", None) == 409518958
    assert node.get("end", None) == 409525564
    assert node.get("score", None) == "."
    assert node.get("strand", None) == "-"
    assert node.get("directive", None) == ""
    assert node.get("score", None) == "."
    assert node.get("phase", None) == "."
    assert node.get("id", None) == "gene:AET2Gv20728000"
    assert node.get("biotype", None) == "protein_coding"
    assert node.get("gene_id", None) == "AET2Gv20728000"
    assert node.get("logic_name", None) == "aet_v4_high_conf"

    assert len(rels) == 0


def test_extract_information_from_chromosome_from_gff(
    test_gff_object: Gff3,
) -> None:
    chromosome_record = test_gff_object.lines[6]
    node, rels = get_node_and_rel_from_record(chromosome_record)
    assert node.get("id", None) == "chromosome:2D"
    assert len(rels) == 0


def test_extract_information_from_trna_from_gff(test_gff_object: Gff3) -> None:
    chromosome_record = test_gff_object.lines[10]
    node, rels = get_node_and_rel_from_record(chromosome_record)
    assert node.get("id", None) == "transcript:ENSRNA050028792-T1"
    assert node.get("biotype", None) == "tRNA"
    assert node.get("tag", None) == "Ensembl_canonical"
    assert node.get("transcript_id", None) == "ENSRNA050028792-T1"

    assert len(rels) == 1
    assert rels[0]["source"] == "transcript:ENSRNA050028792-T1"
    assert rels[0]["target"] == "gene:AET2Gv20728000"
