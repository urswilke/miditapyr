# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../../'))
import miditapyr

# -- Project information -----------------------------------------------------

project = 'miditapyr'
copyright = '2021, Urs Wilke'
author = 'Urs Wilke'

# The full version, including alpha/beta/rc tags
release = '0.1.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'nbsphinx', 
    'sphinx.ext.autodoc',
    # from here https://kevin.burke.dev/kevin/sphinx-interlinks/
    'sphinx.ext.intersphinx',
    ]
# Add mappings
intersphinx_mapping = {
    'mido': ('https://mido.readthedocs.io/en/latest', None),
    'pandas': ('http://pandas.pydata.org/pandas-docs/dev', None),
    'python': ('http://docs.python.org/3', None),
}
# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = []

# add logo as explained here:
# https://stackoverflow.com/questions/59215996/how-to-add-a-logo-to-my-readthedocs-logo-rendering-at-0px-wide
html_logo = 'tapir_rect.png'
html_theme_options = {
    'logo_only': False,
    'display_version': False,
}

# from here: https://github.com/readthedocs/sphinx_rtd_theme/issues/117#issuecomment-41571653
def setup(app):
#    app.add_javascript("custom.js")
   app.add_stylesheet("custom.css")

# from here: https://github.com/readthedocs/readthedocs.org/issues/2569
master_doc = 'index'
