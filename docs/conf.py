# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html
import inspect
import os
import jamfmcp
import sys
import warnings
from pathlib import Path

from jamfmcp.__about__ import __title__, __version__

sys.path.insert(0, os.path.abspath(".."))
sys.path.insert(0, os.path.abspath("../src"))
sys.path.append(str(Path(".").resolve()))

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = "Jamf MCP"
copyright = "Copyright &copy; 2025, Andrew Lerman"
author = "Andrew Lerman"

version = __version__
release = f"{__title__}"

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.intersphinx",
    "sphinx.ext.linkcode",
    "myst_parser",
    "sphinx_copybutton",
    "sphinx_design",
    "sphinx_iconify",
    "sphinxcontrib.autodoc_pydantic",
    "sphinx.ext.autosectionlabel",
]

# Intersphinx mapping
intersphinx_mapping = {
    "python": ("https://docs.python.org/3", None),
    "jamfsdk": ("https://macadmins.github.io/jamf-pro-sdk-python", None),
    "pydantic": ("https://docs.pydantic.dev/latest", None),
}

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Suppress specific warnings
suppress_warnings = [
    "autodoc",                # Suppress duplicate object warnings from autodoc
    "myst.xref_ambiguous",    # Suppress ambiguous cross-reference warnings
    "autosectionlabel.*",     # Suppress duplicate label warnings
]

# Autodoc configuration
add_module_names = False
autodoc_typehints = "both"
autodoc_member_order = "bysource"
autosectionlabel_prefix_document = True

toc_object_entries_show_parents = "hide"

# Pydantic opts
autodoc_pydantic_model_show_json = False
autodoc_pydantic_model_show_field_summary = False

# MyST opts
myst_enable_extensions = [
    "colon_fence",
    "substitution",
    "tasklist",
]

# MyST heading anchors
myst_heading_anchors = 3

# MyST substitutions
myst_substitutions = {
    "version": __version__,
    "release": release,
}

# Pygments opts
pygments_style = "one-light"
pygments_dark_style = "one-dark-pro"

# -- Link Code  --------------------------------------------------------------
# based on pandas doc/source/conf.py
def linkcode_resolve(domain, info):
    """Generate external links to source code on GitHub."""
    if domain != "py":
        return None

    modname = info.get("module")
    fullname = info.get("fullname")

    submod = sys.modules.get(modname)
    if submod is None:
        return None

    obj = submod
    for part in fullname.split("."):
        try:
            with warnings.catch_warnings():
                warnings.simplefilter("ignore", FutureWarning)
                obj = getattr(obj, part)
        except AttributeError:
            return None

    try:
        fn = inspect.getsourcefile(inspect.unwrap(obj))
    except TypeError:
        try:  # property
            fn = inspect.getsourcefile(inspect.unwrap(obj.fget))
        except (AttributeError, TypeError):
            fn = None
    if not fn:
        return None

    try:
        source, lineno = inspect.getsourcelines(obj)
    except (TypeError, OSError):
        try:
            source, lineno = inspect.getsourcelines(obj.fget)  # property
        except (AttributeError, TypeError):
            lineno = None

    linespec = f"#L{lineno}-L{lineno + len(source) - 1}" if lineno else ""

    # Convert to relative path for GHlinks
    fn = os.path.relpath(fn, start=os.path.dirname(jamfmcp.__file__))

    return f"https://github.com/liquidz00/jamfmcp/blob/main/src/jamfmcp/{fn}{linespec}"

# -- Options for copy button  ------------------------------------------------
# https://sphinx-copybutton.readthedocs.io/en/latest/use.html
copybutton_prompt_text = r">>> |\.\.\. |\$ "
copybutton_prompt_is_regexp = True

# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = "shibuya"
html_static_path = ["_static"]
html_title = f"{release}"


html_theme_options = {
    "dark_code": True,
    "nav_links": [
        {
            "title": "Changelog",
            "url": "https://github.com/liquidz00/jamfmcp/blob/main/CHANGELOG.md",
            "external": True,
        },
        {
            "title": "More",
            "children": [
                {
                    "title": "MacAdmins Foundation",
                    "url": "https://www.macadmins.org"
                },
                {
                    "title": "JamfNation",
                    "url": "https://community.jamf.com"
                },
                {
                    "title": "Jamf Pro Documentation",
                    "url": "https://learn.jamf.com/en-US/bundle/jamf-pro-documentation-current/page/Jamf_Pro_Documentation.html"
                },
            ],
        },
    ],
}
