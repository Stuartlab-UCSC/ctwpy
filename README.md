# ctwpy
Generate and Upload Cell Type Worksheets to the UCSC Cell Atlas.

### Install

You'll need [git](https://gist.github.com/derhuerst/1b15ff4652a867391f03), [pip](https://pip.pypa.io/en/stable/installing/), and [virtualenv](https://virtualenv.pypa.io/en/latest/installation/) installed on your machine.

Clone the repository and make a virtual environment.
```
git clone https://github.com/Stuartlab-UCSC/ctwpy.git
cd ctwpy
# Create a virtual environment to install the package in.
virtualenv env
```
 Once inside your virtual environment use pip to install dependencies.
```
# Enter virtual environment
source env/bin/activate
# Use pip to install
pip install --editable .
```
Now you'll be able to access the applications command line interface. The command line interface is available anytime you enter the environment.
### Command Line Interface
```
# Enter virtual environment
source env/bin/activate

# Check out the help documentation:
ctw-from-scanpy --help

ctw-upload --help

# Create a Cell Type Worksheet formated file from a scanpy object.
ctw-from-scanpy dataset-filename.h5ad 

# Send the created Cell Type Worksheet to the UCSC Cell Atlas
ctw-upload dataset-filename.ctw.tar.gz credentials.json
```
