"""
cli exposed via flask
"""
import click
from ctwpy.io import make_dir_or_complain, write_all_worksheet, delete_dir
from ctwpy.marker_table import run_pipe
import ctwpy.scanpyapi as ad_obj
import tarfile
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
    print("Attempt to gather cell type mapping")
    mapping = ad_obj.celltype_mapping(ad, cluster_name, celltype_key)

    if mapping is None:
        print("No Cell Type Mapping Found")
    else:
        print("Mapping Found: preview:", mapping.head())

    use_raw = ad_obj.has_raw(ad)
    xys = ad_obj.get_xys(ad, key="X_umap")

    print("Running marker generation")

    clustering = ad_obj.get_obs(ad, cluster_name)


    markers_df = run_pipe(ad, cluster_name)


    exp = ad_obj.get_expression(ad, use_raw)

    # Make the directory to tar up later.
    make_dir_or_complain(worksheet_name)
    write_all_worksheet(worksheet_name, xys=xys, exp=exp, clustering=clustering, markers=markers_df, celltype=mapping)

    ctw_filename = "%s.ctw.tgz" % worksheet_name
    make_tarfile(ctw_filename, source_dir=worksheet_name)
    delete_dir(worksheet_name)


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


@click.command(help="See the keys for the observation matrix")
@click.argument('scanpy_path')
def scanpy_obs(scanpy_path):
    ad = ad_obj.readh5ad(scanpy_path)
    print(ad.obs_keys())

