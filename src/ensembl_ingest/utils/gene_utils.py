import copy
import logging
from typing import Tuple, Dict, Any, Union, Optional

from gff3 import Gff3


def get_line_idx_2_entity_id_maps(gff: Gff3) -> Tuple[
    Dict[str, str], Dict[str, str]]:
    line_idx_2_entity_id = {}
    entity_id_2_line_idx = {}

    for record in gff.lines:
        if "line_index" not in record:
            raise RuntimeError(
                f"Record: {record} does not have a line index. Aborting!")

        line_idx = record["line_index"]
        entity_id = record.get("attributes", {}).get("ID", None)

        if line_idx in line_idx_2_entity_id:
            raise RuntimeError(
                f"Line index: {line_idx} already exists. Aborting!")
        if entity_id in entity_id_2_line_idx:
            raise RuntimeError(
                f"Entity index: {entity_id} already exists. Aborting!")

        line_idx_2_entity_id[line_idx] = entity_id

        if entity_id is not None:
            entity_id_2_line_idx[entity_id] = line_idx

    return line_idx_2_entity_id, entity_id_2_line_idx


def extract_node_data(record: Dict[str, Any]) -> Tuple[
    Dict[str, Optional[Any]], Any, Any]:
    data = {
        "directive": record.get("directive", None),
        "type": record.get("type", None),
        "seqid": record.get("seqid", None),
        "start": record.get("start", None),
        "end": record.get("end", None),
        "score": record.get("score", None),
        "source": record.get("source", None),
        "strand": record.get("strand", None),
        "phase": record.get("phase", None),
    }
    attributes, parents = extract_attributes_and_parents(record.get("attributes", {}))
    return data, attributes, parents


def extract_attributes_and_parents(attributes):
    attributes_modified = copy.deepcopy(attributes)
    parents = attributes_modified.get("Parent", [])

    if "Parent" in attributes_modified:
        del attributes_modified["Parent"]

    if "ID" in attributes_modified:
        attributes_modified["id"] = attributes_modified["ID"]
        del attributes_modified["ID"]

    return attributes_modified, parents


def get_node_and_rel_from_record(gene_record: Dict[str, Any]):
    data, attributes, parents_raw = extract_node_data(gene_record)
    node = data
    node.update(attributes)
    node_id = node.get("id", None)

    if node_id is None:
        logging.warning(f"Node {node} missess ID...")
        return node, []

    parents = []
    for parent in parents_raw:
        parents.append({"source": node_id, "target": parent})

    return node, parents
