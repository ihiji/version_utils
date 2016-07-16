"""
version.py module for version_utils

The version set here will be automatically incorporated into setup.py
and also set as the __version__ attribute for the package.
"""

# Standard library imports
from __future__ import unicode_literals

__version_info__ = (0, 3, 0)
__version__ = '.'.join([str(ver) for ver in __version_info__])
