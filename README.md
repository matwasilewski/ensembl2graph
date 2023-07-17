# Ensembl Ingest

This is a simple ingest service for ensembl genes. It contains two CLIs:
- `get_genes` that retrieves files from Ensembl FTP server
- `gff3_to_graph` that parses a gff3 or gff3.gz file into a node-link .json that can be loaded by networkX

## Requirements

This package  depends on poetry: https://python-poetry.org/docs/#installation

After installing poetry, run `poetry install` to create a virtual environment and create scripts.

## Usage
### Get Genes

This command retrieves genes from Ensembl FTP server.

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

### GFF3 to JSON

This command parses genes in GFF3 format into [node-link json](https://networkx.org/documentation/stable/reference/readwrite/generated/networkx.readwrite.json_graph.node_link_data.html#networkx.readwrite.json_graph.node_link_data)
that can be then loaded by networkX or by neo4j.

```bash
poetry run gff3_to_graph --help                                                                                                                                           ✔  3.0.0   14:35:34 
Usage: gff3_to_graph [OPTIONS]

  This command parses GFF3 genes and generates .json node-link graph
  representations

Options:
  --file_name TEXT         Path to the genome file  [required]
  --output_file_name TEXT  The output JSON filename.  [required]
  --help                   Show this message and exit.  
```



### Sample usage

Sample usage: download `aegilops_tauschii` to `local_genes_dir`:

```bash
poetry run get_genes --organism_name aegilops_tauschii --output_dir local_genes_dir
```

Parse genome into a graph representation in json

```bash
poetry run gff3_to_graph --file_name local_genes_dir/Aegilops_tauschii.Aet_v4.0.56.gff3.gz --output_file_name aegilops_tauschii_graph.json
```

### How to use in networkX?

```python
import networkx as nx
import json

with open("aegilops_tauschii_graph.json") as f: 
    aegilops_tauschii_json = json.load(f)

graph = nx.node_link_graph(data=aegilops_tauschii_json, directed=True)
```

## Deployment

This tools was created as a CLI utility for bioinformatics, but also with intention of being deployed as a ingest service.
Towards this end, this tools was intentionally split into two separate tools, the ingestor and the parser. Below, I consider deployment options for this service:

### Serverless container platform

The package could easily be containerised, have a simple endpoint added and exposed, and be run on a serverless container platform such as CloudRun (GCP) or AWS App Runner.
It would Extract resources from FTP server and transform them to .json graph files, subsequently uploading to GCS / S3 storage solution, effectively merging all three steps of ETL.
It would be triggered by regular HTTPS requests.

### Airflow

If an Airflow deployment was accessible, a better way to deploy this Ensembl ingest service would be to deploy it on Airflow.
1. A sensor running daily would pick up a change in FTP server if a new release would become available.
2. Dedicated Airflow operator such as `FTPFileTransmitOperator` would download files from the service to intermediate storage.
3. This service's parsing functionality (enclosed in `PythonOperator`, `PythonVirtualenvOperator` or ideally, `KubernetesPodOperator`) would process `gff3.gz` files one by one, producing .json for graphs.
4. Cloud-dependent operator would move the processed data to storage, or would trigger another operator / DAG that would upload them to a graph database.

