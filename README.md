# ctwpy
Generate and Upload Cell Type Worksheets to the UCSC Cell Atlas.

### installation

For now, simply clone the repository, make a virtual environment and then pip install to it. This will expose the cli while you are inside the virtual env.

```
git clone https://github.com/Stuartlab-UCSC/ctwpy.git
cd ctwpy
virtualenv env
. env/bin/activate
pip install --editable .
```

### Command Line Interface
```
# Check out the help documentation:
ctw-from-scanpy --help

ctw-upload --help



# Create a Cell Type Worksheet formated file from a scanpy object.
ctwpy from-scanpy dataset-filename.h5ad 

# Send the created Cell Type Worksheet to the UCSC Cell Atlas
ctwpy to-cell-atlas dataset-filename.ctw.tar.gz credentials.json
```
