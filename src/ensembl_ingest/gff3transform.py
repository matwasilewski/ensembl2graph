import os.path

from src.ensembl_ingest.utils.exceptions import GFF3Exception


class GFF3Genome:
    def __init__(self, path: str):
        if not os.path.isfile(path):
            raise GFF3Exception(f"File: {path} does not exist!")
