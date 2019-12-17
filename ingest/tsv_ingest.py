
from ingest.io import make_dir_or_complain, write_all_worksheet, delete_dir
from ingest.marker_table import run_pipe
import ingest.scanpyapi as ad_obj
import tarfile


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def tsv_ingest(worksheet_name, input_dir_path, clustering_solution):
    print("not yet implemented")
    return
    
    # TODO: if clusters.tsv is not provided, calculate the cell counts.
    print("Attempt to gather cell type mapping")
    ''' from scanpy_ingest:
    mapping = ad_obj.celltype_mapping(ad, cluster_name, celltype_key)
    if mapping is None:
        print("No Cell Type Mapping Found")
    else:
        print("Mapping Found: preview:", mapping.head())

    use_raw = ad_obj.has_raw(ad)
    '''
    
    # TODO: if markers.tsv is not provided, read in the needed tsvs as pandas
    # dataframes to calculate the gene metrics.
    print("Running marker generation")
    ''' from scanpy_ingest:
    xys = ad_obj.get_xys(ad, key="X_umap")
    clustering = ad_obj.get_obs(ad, cluster_name)
    markers_df = run_pipe(ad, cluster_name)
    exp = ad_obj.get_expression(ad, use_raw)
    '''
    
    # Make the directory to tar into.
    make_dir_or_complain(worksheet_name)
    
    # Copy given files and generated data, then compress
    ''' from scanpy_ingest:
    write_all_worksheet(worksheet_name, xys=xys, exp=exp,
        clustering=clustering, markers=markers_df, celltype=mapping)

    ctw_filename = "%s.ctw.tgz" % worksheet_name
    make_tarfile(ctw_filename, source_dir=worksheet_name)
    delete_dir(worksheet_name)
    '''
