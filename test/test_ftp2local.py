import pytest

from src.ensembl_ingest.ftp2local import EnsemblFTPSession


@pytest.fixture()
def session():
    yield EnsemblFTPSession(organism="plants", release="release-55")


def test_ensembl_session() -> None:
    # FIXME: This is acccesing the webserver directly. Should be replaced with https://pypi.org/project/pytest-localftpserver/
    session = EnsemblFTPSession(organism="plants", release="release-55")
    assert session._ftp.pwd() == "/pub/release-55/plants"


def test_if_gff3_present(session: EnsemblFTPSession) -> None:
    list_in_plants = session._ftp.nlst()
    assert "gff3" in list_in_plants


def test_change_organism(session: EnsemblFTPSession) -> None:
    session.change_organism("fungi")
    fungi_pwd = session._ftp.pwd()
    assert "/pub/release-55/fungi" == fungi_pwd
