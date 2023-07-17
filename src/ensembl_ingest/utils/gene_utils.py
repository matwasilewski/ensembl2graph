from typing import Tuple, Dict

from gff3 import Gff3


def get_line_idx_2_entity_id_maps(gff: Gff3) -> Tuple[Dict[str, str], Dict[str, str]]:
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
