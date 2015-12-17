"""
errors.py module for version_utils
"""

# Standard library imports
from __future__ import absolute_import, division, print_function

class VersionUtilsError(Exception):
    """Base error class for version_utils exceptions"""
    pass

class RpmError(VersionUtilsError):
    """Error class for the RPM module"""
    pass
