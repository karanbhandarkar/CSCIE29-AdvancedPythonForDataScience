# -*- coding: utf-8 -*-

"""Top-level package for pset utils."""

from pkg_resources import DistributionNotFound, get_distribution

__author__ = "Solution Solution"
__email__ = "solution@harvard.edu"

try:
    __version__ = get_distribution(__name__).version
except DistributionNotFound:
    # package is not installed
    from setuptools_scm import get_version
    import os
    __version__ = get_version(os.path.dirname(os.path.dirname(__file__))
)

