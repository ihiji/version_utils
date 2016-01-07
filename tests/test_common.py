"""
Test module for version_utils
"""

try:
    import unittest2 as unittest
except ImportError:
    import unittest

try:
    from unittest.mock import MagicMock, patch
except ImportError:
    from mock import MagicMock, patch

from logging import getLogger
from sys import path

logger = getLogger(__name__)


path.append('..')
from version_utils.common import Package


class CommonTestCase(unittest.TestCase):
    """Standard tests for the common module"""

    def test_string_repr(self):
        pkg = Package(name='test', epoch='0', version='1.0',
                             release='1', arch='i386',
                             package_str='test_str.str')
        new_pkg = eval(repr(pkg))
        self.assertEqual("Package Object: ('test', '0', '1.0', '1', 'i386')",
                         str(new_pkg))


if __name__ == '__main__':
    unittest.main()
