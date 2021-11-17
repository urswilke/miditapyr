import pathlib
from setuptools import setup, find_packages

# frm here:
# https://github.com/avinassh/rockstar/blob/master/setup.py#L11,#L19
with open('requirements.txt') as f:
    requirements = f.read().splitlines()

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setup(
    name='miditapyr',
    version='0.1',
    description='Tabulate midi data in DataFrames and write back to midi files',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://github.com/urswilke/miditapyr/',
    author='Urs Wilke',
    author_email='urs.wilke@gmail.com',
    license='MIT',
    packages=find_packages(exclude=['tests*']),
    # install_requires=find_packages(where='.'),
    install_requires=requirements,
    package_dir={'miditapyr': 'miditapyr'},
    package_data={'miditapyr': ['data/*']},
    include_package_data=True,
    # data_files=[('miditapyr/data', ['test_midi_file.mid'])],
    zip_safe=False)
