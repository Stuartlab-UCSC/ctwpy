"""
Input/output functions for user files.

Handles reading of file formats and path munging to directory where user data is kept

TODO: remove 'abort' calls into the the user api code.
"""
import os
import gzip
import json
import pandas as pd

import ctwpy.filenames as keys
from shutil import rmtree

def make_dir_or_complain(ctw_path):
    try:
        os.mkdir(ctw_path)
    except FileExistsError as BadAttemptToOverwrite:
        raise FileExistsError("Attempted to overwrite %s " % ctw_path)

def delete_dir(ctw_path):
    rmtree(ctw_path)

def write_df(path_root, df, type_key):
    """Write a pandas data frame as a pickle."""
    path = os.path.join(path_root, type_key)
    df.to_pickle(path, protocol=4)


def read_gene_expression(path, gene):
    return pd.read_pickle(path).loc[gene]


def read_cluster(path):
    clustering = pd.read_pickle(path)
    clustering = clustering.astype(str)
    return clustering


def markers_manip(marker_df):
    """Impose format restrictions on markers table dataframe."""
    marker_df["cluster"] = marker_df["cluster"].astype(str)
    cols = marker_df.columns.tolist()
    cols.insert(0, cols.pop(cols.index('gene')))
    marker_df = marker_df.reindex(columns=cols)
    return marker_df


def read_markers_df(path):
    df = pd.read_pickle(path)
    df = markers_manip(df)
    return df


def read_xys(path):
    xys = pd.read_pickle(path)
    xys.columns = ["x", "y"]
    return xys


def read_json(path):
    with open(path) as json_file:
        data = json.load(json_file)
    return data

def read_json_gzipd(path):
    with gzip.GzipFile(path, 'r') as fin:
        json_bytes = fin.read()

    json_str = json_bytes.decode('utf-8')
    data = json.loads(json_str)
    return data


def write_all_worksheet(worksheet_root, markers=None, xys=None, exp=None, clustering=None, celltype=None):
    write_df(worksheet_root, exp, keys.EXPRESSION)
    write_df(worksheet_root, markers_manip(markers), keys.MARKER_TABLE)
    write_df(worksheet_root, xys, keys.XYS)
    write_df(worksheet_root, clustering, keys.CLUSTERING)
    write_df(worksheet_root, celltype, keys.CELL_TYPE_ANNOTATION)


def is_valid_file(tarsfilename):
    for key in keys.all_filenames:
        if key in tarsfilename:
            return True
    return False


def name_transform(filename):
    """Returns the filename constant that was found in a filename."""
    for key in fname_keys:
        if key in filename:
            return key
    raise ValueError("The file name could not be transformed into a valid filename constant")