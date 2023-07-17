import gzip
import json
import os.path
import shutil
import tempfile

from gff3 import Gff3

from src.ensembl_ingest.utils.exceptions import GFF3Exception
from src.ensembl_ingest.utils.gene_utils import get_node_and_rel_from_record


class GFF3Genome:
    def __init__(self, path: str) -> None:
        self._genome_gff3 = Gff3()
        self.nodes = []
        self.links = []
        self.transformed_to_node_link = False

        if not os.path.isfile(path):
            raise GFF3Exception(f"File: {path} does not exist!")

        if path.endswith(".gz"):
            self.unpack_genome_in_gz(path)
        else:
            self._genome_gff3.parse(path)

    def unpack_genome_in_gz(self, path: str) -> None:
        with tempfile.TemporaryDirectory() as temp_dir:
            # Construct the path to the temporary file (in the temporary directory)
            temp_file_path = os.path.join(temp_dir, 'temp_file')

            # Open the .gz file, open the temporary file, and use `shutil.copyfileobj` to decompress the .gz file
            with gzip.open(path, 'rb') as f_in:
                with open(temp_file_path, 'wb') as f_out:
                    shutil.copyfileobj(f_in, f_out)

            self._genome_gff3.parse(temp_file_path)

    def transform_to_node_link(self):
        self.transformed_to_node_link = True

        for record in self._genome_gff3.lines:
            node, _ = get_node_and_rel_from_record(record)
            if node is not None:
                self.nodes.append(node)

        node_ids = {node["id"] for node in self.nodes}

        for record in self._genome_gff3.lines:
            _, rels = get_node_and_rel_from_record(record)
            self.verify_nodes_exist(node_ids, rels)
            for link in rels:
                self.links.append(link)

    @staticmethod
    def verify_nodes_exist(nodes_ids, links):
        for link in links:
            if link["source"] not in nodes_ids:
                raise RuntimeError(f"Node: {link['source']} is missing")
            elif link["target"] not in nodes_ids:
                raise RuntimeError(f"Node: {link['target']} is missing")

    def to_node_link_json(self, file_path: str) -> None:
        if not self.transformed_to_node_link:
            self.transform_to_node_link()

        data = {
            "nodes": self.nodes,
            "links": self.links,
        }

        with open(file_path, "w") as f:
            json.dump(data, f)
