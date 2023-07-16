from _socket import gaierror
from ftplib import FTP


class EnsemblFTPSession:
    def __init__(self, organism, release):
        ensembl_url = "ftp.ensemblgenomes.ebi.ac.uk"

        try:
            self.ftp = FTP(ensembl_url)
            self.ftp.login()
        except gaierror as error:
            raise RuntimeError(
                f"Failed to connect to {ensembl_url}. Error: {error}"
            )

        self.organism = organism
        self.release = release
        # TODO: implement automatic CWD to organism and release when creating a session

    def change_release(self, release):
        self.release = release
        self.ftp.cwd("/pub")
