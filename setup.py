from setuptools import setup, find_packages

setup(
    name='ctwpy',
    version='0.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'Click', "scanpy>1", "scipy", "pandas", "beautifulsoup4", "requests", "requests_toolbelt", "urllib3<=1.23"
    ],
    entry_points='''
        [console_scripts]
        ctw-scanpy-obs=ctwpy.cli:scanpy_obs
        ctw-from-scanpy=ctwpy.cli:from_scanpy
        ctw-upload=ctwpy.cli:upload_worksheet

    ''',
)
