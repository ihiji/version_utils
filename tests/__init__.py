"""
__init__.py module for version_utils
"""

# Standard library imports
from __future__ import absolute_import, division, print_function
from os import environ
from sys import path
import logging

# Third party imports

# Local imports


logger = logging.getLogger('version_utils')

path.append('..')

logger.setLevel(logging.DEBUG)
logger.addHandler(logging.StreamHandler())
