# Ensembl Ingest

This is a simple ingest service for ensembl genes. It contains a CLI, and is containerised.

## Requirements

It depends on poetry: https://python-poetry.org/docs/#installation

After installing poetry, run `poetry install` to create a virtual environemnt and create scripts.

## Usage

Help:
```bash
poetry run get_genes --help

Usage: get_genes [OPTIONS]

Options:
  --organism_name TEXT  The name of organism.  [required]
  --organism_type TEXT  The type of the organism.
  --release TEXT        The release version.
  --output_dir TEXT     The output directory.
  --help                Show this message and exit.
  
```

### Sample usage
Sample usage: download `aegilops_tauschii` to `local_directory`:

```bash
poetry run get_genes --organism_name aegilops_tauschii --output_dir local_directory
```

