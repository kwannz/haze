"""
Sphinx Configuration for Haze-Library
======================================

Configuration file for the Sphinx documentation builder.
"""

import os
import sys

# Add the source directory to the path for autodoc
sys.path.insert(0, os.path.abspath('../rust/python'))

# -- Project information -----------------------------------------------------

project = 'Haze-Library'
copyright = '2025, Haze Team'
author = 'Haze Team'

# The full version, including alpha/beta/rc tags
release = '0.1.0'
version = '0.1.0'

# -- General configuration ---------------------------------------------------

extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.autosummary',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'myst_parser',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']

# The suffix(es) of source filenames.
source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# The master toctree document.
master_doc = 'index'

# -- Options for HTML output -------------------------------------------------

html_theme = 'furo'  # Modern, clean theme

html_static_path = ['_static']

html_theme_options = {
    "light_css_variables": {
        "color-brand-primary": "#2962FF",
        "color-brand-content": "#2962FF",
    },
    "dark_css_variables": {
        "color-brand-primary": "#448AFF",
        "color-brand-content": "#448AFF",
    },
}

# -- Extension configuration -------------------------------------------------

# Napoleon settings for Google-style docstrings
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = True
napoleon_use_admonition_for_examples = True
napoleon_use_admonition_for_notes = True
napoleon_use_admonition_for_references = True
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True
napoleon_type_aliases = None

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__',
}

autodoc_typehints = 'description'
autodoc_typehints_description_target = 'documented'

# Autosummary settings
autosummary_generate = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
    'pandas': ('https://pandas.pydata.org/docs/', None),
    'numpy': ('https://numpy.org/doc/stable/', None),
}

# TODOs
todo_include_todos = True

# MyST parser settings
myst_enable_extensions = [
    "colon_fence",
    "deflist",
    "fieldlist",
    "tasklist",
]
