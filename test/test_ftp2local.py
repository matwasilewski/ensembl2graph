from src.ensembl_ingest.ftp2local import EnsemblFTPSession


def test_ensembl_session(caplog) -> None:
    # FIXME: This is acccesing the webserver directly. Should be replaced with https://pypi.org/project/pytest-localftpserver/
    session = EnsemblFTPSession(organism="plants", release="release-55")
    assert session.ftp.pwd() == "/pub/release-55/plants"

    # list_in_plants = session.ftp.nlst()
    # assert "gff3" in list_in_plants
