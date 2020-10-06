import pathlib
import setuptools

# The directory containing this file
HERE = pathlib.Path(__file__).parent

# The text of the README file
README = (HERE / "README.md").read_text()

setuptools.setup(
    name='miditapyr',
    version='0.0.1',
    description='Tabulate midi data in DataFrames and write back to midi files',
    long_description=README,
    long_description_content_type="text/markdown",
    url='https://urssblogg.netlify.app/',
    author='Urs Wilke',
    author_email='urs.wilke@gmail.com',
    license='MIT',
    packages=setuptools.find_packages(),
    install_requires=[
        'pandas',
        'numpy',
        'mido'],
    zip_safe=False)
