"""
__init__.py module for version_utils
"""

# Standard library imports
from __future__ import absolute_import, division, print_function
import logging

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Ensure no logging errors if users have not added any handlers
logging.getLogger(__name__).addHandler(NullHandler())


