import logging
import os
import sys

import click

from src.ensembl_ingest.ftp2local import EnsemblFTPSession
from src.ensembl_ingest.gff3transform import GFF3Genome


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


@click.command()
@click.option(
    '--file', required=True, type=str, help='Path to the genome file'
)
@click.option(
    '--output_file',
    required=True,
    help='The output JSON filename.',
)
def cli_to_graph(file_name, output_file_name):
    if not output_file_name.endswith(".json"):
        output_file_name += ".json"

    if not os.path.isfile(file_name):
        logging.error(f"Input file: {file_name} does not exist!")
        sys.exit(1)

    logging.info("Starting transform from gff3 to json...")
    _gff3_to_graph_json(file_name, output_file_name)
    logging.info("Transform from gff3 to json successful")


def _gff3_to_graph_json(file_name, output_file_name):
    genome = GFF3Genome(file_name)
    genome.to_node_link_json(output_file_name)


if __name__ == '__main__':
    main()
