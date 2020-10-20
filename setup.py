import pathlib
from setuptools import setup, find_packages

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='miditapyr',
    version='0.0.1',
    description='Tabulate midi data in DataFrames and write back to midi files',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/urswilke/miditapyr/',
    author='Urs Wilke',
    author_email='urs.wilke@gmail.com',
    license='MIT',
    packages=find_packages(),
    install_requires=find_packages(where='.'),
    package_dir={
        '': '.',
    },
    zip_safe=False)
