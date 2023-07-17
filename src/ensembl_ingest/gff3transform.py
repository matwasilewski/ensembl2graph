import gzip
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
        for record in self._genome_gff3.lines:
            node, rels = get_node_and_rel_from_record(record)
            if node is not None:
                self.nodes.append(node)
            for link in rels:
                self.links.append(link)

    def verify_nodes_exist(self, nodes, links):
        # TODO: implement
        pass
