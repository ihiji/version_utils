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

path.append('..')
from version_utils import rpm
from version_utils import errors


logger = getLogger(__name__)

# Version strings for testing, along with their parsed information
version_strings = {
            'nmap-6.40-1.i386': {
                'name': 'nmap',
                'epoch': '0',
                'version': '6.40',
                'release': '1',
                'arch': 'i386'
            },
            'python-pyinvision-0.2.9-1.noarch': {
                'name': 'python-pyinvision',
                'epoch': '0',
                'version': '0.2.9',
                'release': '1',
                'arch': 'noarch'
            },
            'gcc-4.4.7-16.el6.x86_64': {
                'name': 'gcc',
                'epoch': '0',
                'version': '4.4.7',
                'release': '16.el6',
                'arch': 'x86_64'
            },
            'ncurses-libs-5.7-3.20090208.el6.i686': {
                'name': 'ncurses-libs',
                'epoch': '0',
                'version': '5.7',
                'release': '3.20090208.el6',
                'arch': 'i686'
            },
            'perl-Compress-Raw-Zlib-2.021-136.el6_6.1.x86_64': {
                'name': 'perl-Compress-Raw-Zlib',
                'epoch': '0',
                'version': '2.021',
                'release': '136.el6_6.1',
                'arch': 'x86_64'
            },
            'libX11-1.6.0-2.2.el6.x86_64': {
                'name': 'libX11',
                'epoch': '0',
                'version': '1.6.0',
                'release': '2.2.el6',
                'arch': 'x86_64'
            },
            'pkgconfig-0.23-9.1.el6.x86_64': {
                'name': 'pkgconfig',
                'epoch': '0',
                'version': '0.23',
                'release': '9.1.el6',
                'arch': 'x86_64'
            },
            'ruby-1.8.7.374-4.el6_6.x86_64': {
                'name': 'ruby',
                'epoch': '0',
                'version': '1.8.7.374',
                'release': '4.el6_6',
                'arch': 'x86_64'
            },
            'openssl-1.0.1e-42.el6.x86_64': {
                'name': 'openssl',
                'epoch': '0',
                'version': '1.0.1e',
                'release': '42.el6',
                'arch': 'x86_64'
            },
            'ntp-4.2.2p1-9.el5.centos.2.1.x86_64': {
                'name': 'ntp',
                'epoch': '0',
                'version': '4.2.2p1',
                'release': '9.el5.centos.2.1',
                'arch': 'x86_64'
            },
            'ruby-1:1.8.7.374-4.el6_6.x86_64': {
                'name': 'ruby',
                'epoch': '1',
                'version': '1.8.7.374',
                'release': '4.el6_6',
                'arch': 'x86_64'
            },
            'openssl-1.~0.1e-42.el6.x86_64': {
                'name': 'openssl',
                'epoch': '0',
                'version': '1.~0.1e',
                'release': '42.el6',
                'arch': 'x86_64'
            },
            'firefox-45.0-4.fc22.x86_64': {
                'name': 'firefox',
                'epoch': '0',
                'version': '45.0',
                'release': '4.fc22',
                'arch': 'x86_64'
            }
        }


class RpmTestCase(unittest.TestCase):
    """Tests for standard RPM module usage"""

    def test_pop_arch(self):
        for vs, info in version_strings.items():
            char_list = list(vs)
            arch = rpm._pop_arch(char_list)
            self.assertEqual(info['arch'], arch)

    def test_parse_information(self):
        """test the parse_information function for all version_strings"""
        for vs, info in version_strings.items():
            evr = (info['epoch'], info['version'], info['release'])
            parsed = rpm.parse_package(vs)
            self.assertEqual(info['name'], parsed['name'])
            self.assertEqual(evr, parsed['EVR'])
            self.assertEqual(info['arch'], parsed['arch'])

    def test_package(self):
        """Test the package function with all version_strings"""
        for vs, info in version_strings.items():
            expect = (info['name'], info['epoch'], info['version'],
                      info['release'], info['arch'])
            pkg = rpm.package(vs)
            self.assertEqual(expect, pkg.info)

    def test_parse_package_bad_package_no_arch(self):
        with self.assertRaises(errors.RpmError):
            rpm.parse_package('what_even_is_this_thing')

    def test_parse_package_bad_package(self):
        with self.assertRaises(errors.RpmError):
            rpm.parse_package('blargleblargle.aiiii')

    def test_check_leading(self):
        test_strs = [
            ('1.05', '1.05'),
            ('.104', '104'),
            ('~104', '~104'),
            ('~.4', '~.4'),
            ('!444', '444')
        ]
        for test, expect in test_strs:
            test_list = list(test)
            rpm._check_leading(test_list)
            res = ''.join(test_list)
            self.assertEqual(expect, res)

    def test_trim_zeros(self):
        test_strs = [
            ('0012', '12'),
            ('120', '120'),
            ('000000000005', '5'),
            ('101', '101'),
            ('0000', '')
        ]
        for test, expect in test_strs:
            test_list = list(test)
            rpm._trim_zeros(test_list)
            res = ''.join(test_list)
            self.assertEqual(expect, res)

    def test_trim_zeros_multi(self):
        test_strs = [
            (('0012', '12'), ('120', '120')),
            (('04', '4'), ('0', ''))
        ]
        for test_a, test_b in test_strs:
            a_test, a_expect = test_a
            b_test, b_expect = test_b
            a_list, b_list = list(a_test), list(b_test)
            rpm._trim_zeros(a_list, b_list)
            res_a, res_b = ''.join(a_list), ''.join(b_list)
            self.assertEqual(a_expect, res_a)
            self.assertEqual(b_expect, res_b)

    def test_pop_digits(self):
        test_strs = [
            ('1.05', '1'),
            ('12.44', '12'),
            ('12a4.2', '12'),
            ('aa4', ''),
            ('.1234', '')
        ]
        for test, expect in test_strs:
            test_list = list(test)
            digits = rpm._pop_digits(test_list)
            res = ''.join(digits)
            self.assertEqual(expect, res)

    def test_pop_letters(self):
        test_strs = [
            ('1.00', ''),
            ('aaer2r', 'aaer'),
            ('a23', 'a'),
            ('a.2', 'a'),
            ('.a22', '')
        ]
        for test, expect in test_strs:
            test_list = list(test)
            letters = rpm._pop_letters(test_list)
            res = ''.join(letters)
            self.assertEqual(expect, res)

    def test_compare_blocks(self):
        test_blocks = [
            ('12345', '12345', 0),
            ('12345', '1234', 1),
            ('1234', '12345', -1),
            ('12345', '12346', -1),
            ('12346', '12345', 1),
            ('0012', '0012', 0),
            ('00123', '0012', 1),
            ('0012', '00123', -1),
            ('00123', '00124', -1),
            ('00124', '00123', 1)
        ]
        for a, b, exp in test_blocks:
            list_a, list_b = list(a), list(b)
            res = rpm._compare_blocks(list_a, list_b)
            self.assertEqual(exp, res, msg='Got {0} when comparing {1} to '
                                           '{2}'.format(res, a, b))

    def test_get_block_res(self):
        test_strs = [
            ('12.12', '12.13', 0),
            ('12.12', 'a.13', 1),
            ('a12.5', '12.5', -1),
            ('01ab', '01ac', 0),
            ('012ab', '02ab', 1),
            ('abc123', 'abc123', 0),
            ('abd123', 'abc123', 1)
        ]
        for a, b, exp in test_strs:
            list_a, list_b = list(a), list(b)
            res = rpm._get_block_result(list_a, list_b)
            self.assertEqual(exp, res, msg='Got {0} when comparing {1} to '
                                           '{2}'.format(res, a, b))

    def test_compare_versions(self):
        test_versions = [
            ('~', 'aoi', -1),
            ('aoi', '~', 1),
            ('~', '~', 0),
            ('~', '~a', -1),
            ('1a', 'a1', 1),
            ('1a', '1b', -1),
            ('a1', 'a2', -1),
            ('1.2.3', '1.2.4', -1),
            ('1.02.4', '1.02a.4', 1),
            ('1.02a.4', '1.02b.4', -1),
            ('12345.6', '12345.6', 0),
            ('0.2.3', '1.2.4', -1),
            ('~1.2.3', '1.2.3', -1),
            ('1.2.3.a', '1.2.3.~alpha', 1)
        ]
        for a, b, exp in test_versions:
            res = rpm.compare_versions(a, b)
            self.assertEqual(exp, res, msg='Got {0} when comparing {1} to '
                                           '{2}'.format(res, a, b))


if __name__ == '__main__':
    unittest.main()
