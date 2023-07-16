from _socket import gaierror
from ftplib import FTP

from src.ensembl_ingest.utils.exceptions import FTPError


class EnsemblFTPSession:
    def __init__(self, organism, release):
        self.organism = None
        self.release = None
        self.ensembl_url = "ftp.ensemblgenomes.ebi.ac.uk"

        try:
            self._ftp = FTP(self.ensembl_url)
            self._ftp.login()
        except gaierror as error:
            raise FTPError(
                f"Failed to connect to {self.ensembl_url}. Error: {error}"
            )
        self.change_release_and_organism(release=release, organism=organism)

    def change_release(self, release):
        releases = {r.split("/")[-1] for r in self._ftp.nlst("/pub")}

        if release not in releases:
            raise FTPError(f"Release: {release} does not exist in {self.ensembl_url}. Available releases: {releases}/")

        self.release = release

    def change_organism(self, organism):
        available_organisms = {org.split("/")[-1] for org in self._ftp.nlst(f"/pub/{self.release}")}

        if organism not in available_organisms:
            raise FTPError(f"Organism: {organism} does not exist in {self.ensembl_url}, in release: {self.release}. Available organisms in this release: {available_organisms}")

        self.organism = organism
        self._ftp.cwd(f"/pub/{self.release}/{self.organism}")

    def change_release_and_organism(self, release, organism):
        self.change_release(release=release)
        self.change_organism(organism=organism)
