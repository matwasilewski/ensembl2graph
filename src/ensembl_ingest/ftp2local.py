from _socket import gaierror
from ftplib import FTP
from typing import Optional

from src.ensembl_ingest.utils.exceptions import FTPError


class EnsemblFTPSession:
    def __init__(
        self, organism: str, release: str, output_dir: Optional[str] = None
    ) -> None:
        self.organism_type = organism
        self.release = release
        self.format = "gff3"
        self.ensembl_url = "ftp.ensemblgenomes.ebi.ac.uk"
        self.output_dir = output_dir

        try:
            self._ftp = FTP(self.ensembl_url)
            self._ftp.login()
        except gaierror as error:
            raise FTPError(
                f"Failed to connect to {self.ensembl_url}. Error: {error}"
            )
        self.change_release_and_organism_type(
            release=release, organism=organism
        )

    def change_release(self, release: str) -> None:
        releases = {r.split("/")[-1] for r in self._ftp.nlst("/pub")}

        if release not in releases:
            raise FTPError(
                f"Release: {release} does not exist in {self.ensembl_url}. Available releases: {releases}/"
            )

        self.release = release
        self.change_organism_type(organism=self.organism_type)

    def change_organism_type(self, organism: str) -> None:
        available_organisms = {
            org.split("/")[-1]
            for org in self._ftp.nlst(f"/pub/{self.release}")
        }

        if organism not in available_organisms:
            raise FTPError(
                f"Organism: {organism} does not exist in {self.ensembl_url}, in release: {self.release}. Available organisms in this release: {available_organisms}"
            )

        self.organism_type = organism
        self._ftp.cwd(
            f"/pub/{self.release}/{self.organism_type}/{self.format}"
        )

    def change_release_and_organism_type(
        self, release: str, organism: str
    ) -> None:
        self.change_release(release=release)
        self.change_organism_type(organism=organism)
