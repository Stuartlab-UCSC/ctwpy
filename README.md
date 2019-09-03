# ctwpy
Generate and Upload Cell Type Worksheets to the UCSC Cell Atlas.

### installation

For now, simply clone the repository and place the package in your python path. This package should work out of the box with any environment that supports scanpy. If you are having installation issues the requirments.txt file at the root of this repository contains a list of dependencies.

```
git clone https://github.com/Stuartlab-UCSC/ctwpy.git
cd ctwpy
export PYTHONPATH=$PYTHONPATH:$(pwd)
```

### Command Line Interface
```
# Check out the help documentation:
ctwpy --help

ctwpy from-scanpy --help

# Create a Cell Type Worksheet formated file from a scanpy object.
ctwpy from-scanpy dataset-filename.h5ad 

# Send the created Cell Type Worksheet to the UCSC Cell Atlas
ctwpy to-cell-atlas dataset-filename.ctw.tar.gz credentials.json
```
