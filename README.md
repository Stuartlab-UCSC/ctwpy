# ctwpy
Generate and Upload Cell Type Worksheets to the UCSC Cell Atlas from a scanpy anndata
object, or from tsv files.

If you want to generate a worksheet from a seurat object, install the package, 
Stuartlab-UCSC/ctw-seurat instead of this one.

### What is a Cell Type Worksheet?
A Cell Type Worksheet is an application designed to ease the burden of manual cell type annotation from single cell
mRNA sequencing experiments. It lets you explore the specificity of markers across clusters and label the clusters
with a cell type annotation.

The web application provides three interactive components for this goal:

1. An editable dot plot visualizing marker specificity and cell type annotation across all clusters.
2. A scatter plot visualizing gene expression across all cells.
3. A table of gene metric rankings per cluster.

Here's a rough visual of the layout of the application, the gene metrics are explored via the table at the bottom.
![Alt text](cell_atlas_layout.png)

This python package manipulates a scanpy object or tsv files into the ctw format 
and provides an avenue for uploading a worksheet to the UCSC Cell Atlas.

### Requirements
python3.4+[git](https://gist.github.com/derhuerst/1b15ff4652a867391f03), [pip](https://pip.pypa.io/en/stable/installing/), and [virtualenv](https://virtualenv.pypa.io/en/latest/installation/)

### Install

If you haven't done so already, head over to the [Cell Atlas registry](https://cellatlasapi.ucsc.edu/user/register)
and make an account, remember to answer the confirmation email. You'll be using your email and password to upload
data to the server.

Clone the repository and make a virtual environment.
```
git clone https://github.com/Stuartlab-UCSC/ctwpy.git
cd ctwpy
# Create a python3 virtual environment to install the package in.
virtualenv -p $(which python3) env
```
 Once inside your virtual environment use pip3 to install dependencies.
```
# Enter virtual environment
source env/bin/activate
# Use pip to install the ctwingest dependency
pip3 install --editable git+git://github.com/Stuartlab-UCSC/ctwingest.git#egg=ctwingest
# Use pip to install this package
pip3 install --editable .
```
Now you'll be able to access the applications command line interface. The command line interface is available anytime you enter the environment.
### Command Line Interface
```
# Enter virtual environment
source env/bin/activate

# Check out the help documentation:
ctw-from-scanpy --help

ctw-from-tsv --help

ctw-upload --help

# Create a Cell Type Worksheet formatted file from a scanpy object.
ctw-from-scanpy worksheet-name dataset-filename.h5ad

# Or create a Cell Type Worksheet formatted file from tsv files.
ctw-from-tsv worksheet-name myTsvFileDir

# Send the created Cell Type Worksheet to the UCSC Cell Atlas.
ctw-upload worksheet-name.ctw.tgz credentials.json
```

To upload a worksheet to the server, you'll notice the credentials.json file is necessary. Use our
[example](https://github.com/Stuartlab-UCSC/ctwpy/blob/master/credentials.json) for a starting
place.

### Preparing tsv files
If you want to create a worksheet from tsv files rather than a scanpy object, those file formats
are described here.

The Cell Type Worksheet ingest tsv files consist of a minimum of 3 tab delimited files, and two 
optional files:

1. Expression Matrix

|       gene       | AAACCTGCAAACTGTC | AAACCTGCAAGGGTCA | AAACCTGCAAGTAATG | ... |
|:----------------:|:----------------:|------------------|------------------|-----|
| TP53 |         0        | 0                | 0                | ... |
| ALKBH6 |         1        | 0                | 1                | ... |
| MYLH1 |         2        | 1                | 3                | ... |
| TMNT2 |         0        | 4.5              | 0                | ... |
| TTN |        3.4       | 0                | 2                | ... |


     + File name is "exp.tsv"
     + Gene names are rows, Cell IDs are columns
     + Can be filtered down to genes of interest
     
2. Cell to Cluster Assignment

|      cellids     | cluster |
|:----------------:|:-------:|
| AAACCTGCAAACTGTC |    1    |
| AAACCTGCAAGGGTCA |    1    |
| AAACCTGCAAGTAATG |    2    |
| AAACCTGCACATAACC |    3    |
| AAACCTGCAGACGCCT |    3    |

     + File name is "clustering.tsv"
     + First column contains cell IDs
     + Second column contains cluster assignment
     
3. XY Coordinates

|      cellids     |  x  | y   |
|:----------------:|:---:|-----|
| AAACCTGCAAACTGTC | 1.1 | 0.4 |
| AAACCTGCAAGGGTCA | 1.5 | 0.8 |
| AAACCTGCAAGTAATG | 2.2 | 3.2 |
| AAACCTGCACATAACC | 3.3 | 4.5 |
| AAACCTGCAGACGCCT | 3.4 | 4.7 |

     + File name is "xys.tsv"
     + First column contains cell IDs
     + Second Column contains x coordinates
     + Third Column contains y coordinates
    
4. Gene Metrics Per Cluster (optional)

|  gene  | t-statistic | pct.exp | avg.exp.scaled | ... | cluster |
|:------:|:-----------:|---------|----------------|-----|---------|
|  TP53  |     3.4     | 46      | 2.2            | ... | 1       |
| ALKBH6 |    -0.86    | 0       | -0.1           | ... | 1       |
|  TP53  |     -0.1    | 15.2    | -0.01          | ... | 2       |
| ALKBH6 | 1.2         | 35      | 0.95           | ... | 2       |
|  TP53  |     3.8     | 88.2    | 2.5            | ... | 3       |
| ALKBH6 |     3.4     | 100     | 2.5            | ... | 3       |

     + File name is "markers.tsv"
     + First column contains genes
     + Last column contains cluster IDs
     + At least 2 columns in-between "gene" and "cluster", e.g. "avg.exp" and "pct.exp"
     + If this file is omitted, gene metrics will be calculated from your data

5. Cluster cell counts and cell types (optional)

| cluster | cell_count | cell_type |
|:--------:|:------------:|--------------------------------- |
| 1 |         5313 |         T-cell |
| 2 |         2562 | |
| ... | | |

     + File name is "clusters.tsv"
     + First column contains cluster IDs
     + Last column contains cell types
     + cell_type values are optional
     + If this file is omitted, cell counts will be summed for you and clusters will have no cell_types
