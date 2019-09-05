"""
Create a Marker table from an AnnData Object.
"""
from statsmodels.stats.proportion import proportions_ztest
from scipy.stats import ttest_ind
import pandas as pd
import numpy as np
from ctwpy.scanpyapi import proportion_expressed_cluster, centroids, get_expression, std_gt_0_genes


def run_pipe(ad, cluster_solution_name="louvain", use_raw=True):
    """Returns a markers table from an anndata object. Looks for anndata.raw to
    make metrics directly from counts. If .raw is not there then proceeds with whatever is in anndata.expression_matrix.
    Metrics are t-statistic a proportions z-statistic, their pvalues and log2fc."""

    # Grab the expression matrix and get ready for processing.
    expression_matrix = get_expression(ad, use_raw=use_raw)
    expression_matrix = expression_matrix.transpose()
    expression_matrix = expression_matrix.dropna(axis='columns', how='all')

    # A cluster solution is a mapping from cell->cluster.name
    cluster_solution = ad.obs[cluster_solution_name]
    cluster_solution = cluster_solution.dropna()
    clusters = cluster_solution.unique()

    print("Calculating centroids and proportions of %d samples and %d genes with %d clusters" % (
        expression_matrix.shape[0], expression_matrix.shape[1], len(clusters)
    ))
    proportions = proportion_expressed_cluster(ad, cluster_solution)
    centroid_df = centroids(ad, cs_name=cluster_solution_name, use_raw=True)



    # Filter to genes that have some standard deviation across thier means
    # Weak filtering intended to prevent downstream errors.
    marker_genes = std_gt_0_genes(centroid_df)
    print(
        "Removing %d genes because standard deviation across means is 0"
        % (expression_matrix.shape[1] - len(marker_genes))
    )
    expression_matrix = expression_matrix[marker_genes]

    # Current implementation builds one dataframe for each cluster and then concats them together.
    dfs = []
    for cluster_name in clusters:
        print("Calculating Cluster ", cluster_name)
        df = pd.DataFrame(
            index=expression_matrix.columns,
            columns=["tstat", "zstat", "pct.exp", "log2fc", "zpval", "tpval", "cluster"]
        )
        df['cluster'] = cluster_name

        cell_names = cluster_solution.index[(cluster_solution == cluster_name).tolist()]
        other_cell_names = cluster_solution.index[(cluster_solution != cluster_name).tolist()]
        pseudocount = .1
        df['log2fc'] = np.log2(expression_matrix.loc[cell_names].mean() + pseudocount) - np.log2(
            expression_matrix.loc[other_cell_names].mean() + pseudocount)

        # set up for proportions z test
        expressed_in_cluster = (expression_matrix.loc[cell_names] > 0).sum()
        expressed_out_cluster = (expression_matrix.loc[other_cell_names] > 0).sum()

        out_size = len(other_cell_names)
        cluster_size = len(cell_names)

        ztest_df = pd.DataFrame([expressed_in_cluster, expressed_out_cluster])
        ztest = lambda x: proportions_ztest(
            count=[x[0], x[1]],
            nobs=[cluster_size, out_size],
            alternative='larger'
        )

        zstat_zpval = ztest_df.apply(ztest, axis='index')
        zstat = zstat_zpval.apply(lambda x: x[0])
        zpval = zstat_zpval.apply(lambda x: x[1])

        ttest = lambda x: ttest_ind(x[cell_names], x[other_cell_names])
        tstat_tpval = expression_matrix.apply(ttest, axis="index")
        tstat = tstat_tpval.apply(lambda x: x[0])
        tpval = tstat_tpval.apply(lambda x: x[1])

        df["tstat"] = tstat
        df['tpval'] = tpval
        df["zstat"] = zstat
        df["zpval"] = zpval
        df['gene'] = df.index.tolist()
        df['pct.exp'] = proportions[cluster_name][df.index]

        dfs.append(df)

    markers_table = pd.concat(dfs, axis=0)
    return markers_table

DEFAULT_LEGEND_METRICS = pd.Series(["tstat", "zstat", "pct.exp"])