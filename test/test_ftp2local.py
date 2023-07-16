import pytest

from src.ensembl_ingest.ftp2local import EnsemblFTPSession
from src.ensembl_ingest.utils.exceptions import FTPError


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
    session.change_organism_type("fungi")
    fungi_pwd = session._ftp.pwd()
    assert "/pub/release-55/fungi" == fungi_pwd


def test_raise_exception_when_changing_to_nonexistent_organism(
        session: EnsemblFTPSession,
) -> None:
    with pytest.raises(FTPError) as e_info:
        session.change_organism_type("midichlorian")
    assert str(e_info.value).startswith(
        f"Organism: midichlorian does not exist in {session.ensembl_url}, in release: release-55. Available organisms in this release:"
    )


def test_raise_exception_when_changing_to_nonexistent_release(
        session: EnsemblFTPSession,
) -> None:
    nonexistent_release = "release-2137"
    with pytest.raises(FTPError) as e_info:
        session.change_release(nonexistent_release)
    assert str(e_info.value).startswith(
        f"Release: {nonexistent_release} does not exist in {session.ensembl_url}. Available releases:"
    )
