import os
import shutil
from _socket import gaierror
from ftplib import FTP
from typing import Optional

from src.ensembl_ingest.utils.exceptions import FTPError


class EnsemblFTPSession:
    def __init__(
        self,
        organism: str,
        release: str,
        output_dir: str = os.path.join(os.getcwd(), "ftp_output"),
        allow_overwrite: bool = False,
    ) -> None:
        self.organism_type = organism
        self.release = release
        self.format = "gff3"
        self.ensembl_url = "ftp.ensemblgenomes.ebi.ac.uk"
        self.output_dir = output_dir
        self.allow_overwrite = allow_overwrite

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

    def close(self):
        self._ftp.close()

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

    def _confirm_organism_exists(self, organism_name: str):
        organisms_list = {org.split("/")[-1] for org in self._ftp.nlst()}

        if organism_name not in organisms_list:
            raise FTPError(
                f"Organism: {organism_name} does not exist. Available organisms: {organisms_list}"
            )

    def get(self, organism_name: str):
        self._confirm_organism_exists(organism_name)
        organism_dir = self._make_organism_dir(organism_name)
        current_ftp_pwd = self._ftp.pwd()
        entities = self._ftp.nlst("/".join([current_ftp_pwd, organism_name]))

        for entity in entities:
            entity_name = entity.split("/")[-1]
            organism_filename = os.path.join(organism_dir, entity_name)

            with open(organism_filename, "wb") as f:
                self._ftp.retrbinary('RETR ' + entity, f.write)

    def _make_organism_dir(self, organism_name):
        os.makedirs(self.output_dir, exist_ok=True)
        organism_dir = os.path.join(self.output_dir, organism_name)

        if os.path.exists(organism_dir) and len(os.listdir(organism_dir)) != 0:
            if self.allow_overwrite:
                shutil.rmtree(organism_dir)
            else:
                raise FileExistsError(
                    f"The directory '{organism_dir}' already exists, is not empty and 'allow_overwrite' is set to False."
                )
        os.makedirs(organism_dir)
        return organism_dir
