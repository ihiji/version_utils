"""
The version_utils package currently contains the following modules:

* ``common`` - common functionality, classes, etc.
* ``errors`` - exceptions
* ``rpm`` - rpm version comparison and package comparison functionality

"""

# Standard library imports
from __future__ import absolute_import, division, print_function
import logging

from version_utils import common, errors, rpm
from version_utils.version import __version__, __version_info__

try:  # Python 2.7+
    from logging import NullHandler
except ImportError:
    class NullHandler(logging.Handler):
        def emit(self, record):
            pass

# Ensure no logging errors if users have not added any handlers
logging.getLogger(__name__).addHandler(NullHandler())
