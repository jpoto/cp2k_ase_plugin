# Configuration file for the Sphinx documentation builder.

project = "cp2k-plugin"
copyright = "2026, CP2K Developers"
author = "CP2K Developers"

extensions = [
    "sphinx.ext.githubpages",
    "sphinx.ext.coverage",
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.autosummary",
    "sphinx.ext.viewcode",
    "myst_parser",
]

source_suffix = {
    ".md": "markdown",
    ".txt": "markdown",
    ".rst": "restructuredtext",
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
html_context = {
    "display_github": True,
    "github_user": "cp2k",
    "github_repo": "cp2k_plugin",
    "github_version": "master",
    "conf_py_path": "/doc/",
}

myst_enable_extensions = ["html_admonition"]
coverage_Show_missing_items = True
autosummary_generate = True
