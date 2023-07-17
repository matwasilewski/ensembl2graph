import logging
import os

import click

from src.ensembl_ingest.ftp2local import EnsemblFTPSession


@click.command()
@click.option(
    '--organism_name', required=True, type=str, help='The name of organism.'
)
@click.option(
    '--organism_type',
    default="plants",
    type=str,
    help='The type of the organism.',
)
@click.option(
    '--release',
    default="current",
    type=str,
    help='The release version.',
)
@click.option(
    '--output_dir',
    default=os.path.join(os.getcwd(), "ftp_output"),
    help='The output directory.',
)
def main(organism_name, organism_type, release, output_dir):
    _download_files(organism_name, organism_type, release, output_dir)


def _download_files(organism_name, organism_type, release, output_dir):
    logging.info(
        f"Starting session for organism_type: {organism_type}, release: {release} and output_dir: {output_dir}"
    )
    session = EnsemblFTPSession(
        organism=organism_type, release=release, output_dir=output_dir
    )
    session.get(organism_name)
    session.close()


if __name__ == '__main__':
    main()
