from setuptools import setup, find_packages

setup(
    name='ctwpy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', "ctwingest"
    ],
    entry_points='''
        [console_scripts]
        ctw-scanpy-obs=ctwpy.cli:scanpy_obs
        ctw-from-scanpy=ctwpy.cli:from_scanpy
        ctw-from-tsv=ctwpy.cli:from_tsv
        ctw-upload=ctwpy.cli:upload_worksheet
    ''',
)
