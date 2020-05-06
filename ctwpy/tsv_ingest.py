from ctwingest.io import make_dir_or_complain, write_all_worksheet, delete_dir
from ctwingest.marker_table import run_pipe
import ctwingest.scanpyapi as ad_obj
import tarfile
import pandas as pd
import os.path
import anndata


def make_tarfile(output_filename, source_dir):
    with tarfile.open(output_filename, "w:gz") as tar:
        tar.add(source_dir, arcname=os.path.basename(source_dir))


def tsv_ingest(worksheet_name, input_dir_path, clustering_solution):
    print("BEGIN tsv_ingest")

    #print("Attempt to gather cell type mapping")
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
    #print("Running marker generation")
    ''' from scanpy_ingest:
    xys = ad_obj.get_xys(ad, key="X_umap")
    clustering = ad_obj.get_obs(ad, cluster_name)
    markers_df = run_pipe(ad, cluster_name)
    exp = ad_obj.get_expression(ad, use_raw)
    '''

    print("read coordinates from xys.tsv")

    # cell x, y coordinates
    xys = pd.read_csv(input_dir_path + "xys.tsv", sep = "\t", index_col = 0)


    print("read cluster assignments from clustering.tsv")

    # cell cluster assignments
    clustering = pd.read_csv(input_dir_path + "clustering.tsv", sep = "\t", index_col = 0)
    # expression matrix


    print("read exp from exp.tsv")

    exp = pd.read_csv(input_dir_path + "exp.tsv", sep = "\t", index_col = 0)


    print("get clusters object")

    # count of cells per cluster
    if os.path.isfile(input_dir_path + "clusters.tsv"):
        print("read clusters from clusters.tsv")
        clusters = pd.read_csv(input_dir_path + "clusters.tsv", sep = "\t", index_col = 0)
    else:
        print("get clusters from clustering assignments read from clustering.tsv")
        clusters = pd.DataFrame(clustering["cluster"].value_counts())
        clusters.columns = ["cell_count"]
        clusters.index.rename("cluster", inplace=True)


    print("create anndata object")
    exp = exp.transpose()
    ad = anndata.AnnData(X=exp, obs=clustering)
    has_raw = ad_obj.has_raw(ad)
    # cw_20200506 doesn't seem like ad.obsm['xys'] is ever used & it was causing an error
    # ad.obsm['xys'] = xys.values

    print("get markers_df from run_pipe")
    # markers_df = run_pipe(ad, 'cluster')
    markers_df = run_pipe(ad, 'cluster', use_raw=has_raw)


    print("generate output")

    print("worksheet_name:%s" % (worksheet_name))

    # Make the directory to tar into.
    make_dir_or_complain(worksheet_name)

    # cw_20200506 mapping is always DNE
    # Copy given files and generated data, then compress
    # try:
    #     mapping
    # except NameError:
    #     write_all_worksheet(worksheet_name, xys=xys, exp=exp,
    #         clustering=clustering, markers=markers_df, celltype=mapping)
    # else:
    #     write_all_worksheet(worksheet_name, xys=xys, exp=exp,
    #         clustering=clustering, markers=markers_df)

    write_all_worksheet(worksheet_name, xys=xys, exp=exp,
        clustering=clustering, markers=markers_df)


    ctw_filename = "%s.ctw.tgz" % worksheet_name
    print("ctw_filename:%s" % (ctw_filename))
    make_tarfile(ctw_filename, source_dir=worksheet_name)


    print("cleanup")

    delete_dir(worksheet_name)

    print("END tsv_ingest")
