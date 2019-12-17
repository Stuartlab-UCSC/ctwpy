"""
cli exposed via flask
"""
import click
from ingest.webapi import upload, read_credentials
import ingest.scanpyapi as ad_obj
import ingest.scanpy_ingest as scanpy_ingest
import os


@click.command(help="Add a scanpy object to the user file system")
@click.argument('worksheet_name')
@click.argument('scanpy_path')
@click.option('--cluster_name', default="louvain",
              help="The name of the key to the clustering solution in the scanpy object, defaults to 'louvain'.")
@click.option('--celltype_key', default="scorect",
              help="The name of the key to the cell type annotation in the scanpy object, defaults to 'scorect'.")
def from_scanpy(worksheet_name, scanpy_path, cluster_name,
                celltype_key=None
):
    print("reading in data...")
    ad = ad_obj.readh5ad(scanpy_path)
    scanpy_ingest(ad, worksheet_name, cluster_name, celltype_key)


@click.command(
    help="""Upload a worksheet to the UCSC Cell Atlas. Requires a credentials.json file filled with login info.
    Read the bottom of the README.md of the git repository.""")
@click.argument('ctw_path')
@click.argument('credentials_path')
@click.option('--group', "-g", default=None, help="A valid group name for the ctw server.")
@click.option('--url', "-u", default="https://cellatlasapi.ucsc.edu/",
              help="Only replace this if you are running your own ctw server.")
def upload_worksheet(ctw_path, credentials_path, url="https://cellatlasapi.ucsc.edu/", group=None):
    credentials = read_credentials(credentials_path)
    upload(ctw_path, credentials, url, group)


@click.command(help="See the keys for the observation matrix")
@click.argument('scanpy_path')
def scanpy_obs(scanpy_path):
    ad = ad_obj.readh5ad(scanpy_path)
    print(ad.obs_keys())

