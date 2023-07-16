import pytest
import tempfile

from src.ensembl_ingest.ftp2local import EnsemblFTPSession
from src.ensembl_ingest.utils.exceptions import FTPError


@pytest.fixture()
def session():
    yield EnsemblFTPSession(organism="plants", release="release-55")


def test_ensembl_session() -> None:
    # FIXME: This is acccesing the webserver directly. Should be replaced with https://pypi.org/project/pytest-localftpserver/
    session = EnsemblFTPSession(organism="plants", release="release-55")
    assert session._ftp.pwd() == f"/pub/release-55/plants/{session.format}"


def test_if_aegilops_tauschii_present(session: EnsemblFTPSession) -> None:
    list_in_plants = session._ftp.nlst()
    assert "aegilops_tauschii" in list_in_plants


def test_change_organism(session: EnsemblFTPSession) -> None:
    session.change_organism_type("fungi")
    fungi_pwd = session._ftp.pwd()
    assert session.organism_type == "fungi"
    assert fungi_pwd == f"/pub/release-55/fungi/{session.format}"


def test_raise_exception_when_changing_to_nonexistent_organism(
    session: EnsemblFTPSession,
) -> None:
    with pytest.raises(FTPError) as e_info:
        session.change_organism_type("midichlorian")
    assert str(e_info.value).startswith(
        f"Organism: midichlorian does not exist in {session.ensembl_url}, in release: release-55. Available organisms in this release:"
    )


def test_change_release(session: EnsemblFTPSession) -> None:
    new_release = "release-47"
    session.change_release(new_release)
    new_pwd = session._ftp.pwd()
    assert session.release == new_release
    assert new_pwd == f"/pub/{new_release}/plants/{session.format}"


def test_raise_exception_when_changing_to_nonexistent_release(
    session: EnsemblFTPSession,
) -> None:
    nonexistent_release = "release-2137"
    with pytest.raises(FTPError) as e_info:
        session.change_release(nonexistent_release)
    assert str(e_info.value).startswith(
        f"Release: {nonexistent_release} does not exist in {session.ensembl_url}. Available releases:"
    )


def test_change_organism_and_release(session: EnsemblFTPSession) -> None:
    new_release = "release-47"
    new_organism = "fungi"
    session.change_release_and_organism_type(
        release=new_release, organism=new_organism
    )
    new_pwd = session._ftp.pwd()
    assert session.release == new_release
    assert session.organism_type == new_organism
    assert new_pwd == f"/pub/{new_release}/{new_organism}/{session.format}"


def test_output_dir() -> None:
    with tempfile.TemporaryDirectory("output_dir") as tmp_dir_name:
        session = EnsemblFTPSession(
            organism="plants", release="release-55", output_dir=tmp_dir_name
        )
        assert session.output_dir == tmp_dir_name
