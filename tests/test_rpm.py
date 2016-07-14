"""
Test module for version_utils
"""

# Builtin imports
from logging import getLogger

# Third party imports
import pytest

# Local imports
from version_utils import rpm
from version_utils import errors

logger = getLogger(__name__)

# Version strings for testing, along with their parsed information
version_info = [
    (
        'nmap-6.40-1.i386',
        {
            'name': 'nmap',
            'epoch': '0',
            'version': '6.40',
            'release': '1',
            'arch': 'i386'
        }
    ),
    (
        'python-pyinvision-0.2.9-1.noarch',
        {
            'name': 'python-pyinvision',
            'epoch': '0',
            'version': '0.2.9',
            'release': '1',
            'arch': 'noarch'
        }
    ),
    (
        'gcc-4.4.7-16.el6.x86_64',
        {
            'name': 'gcc',
            'epoch': '0',
            'version': '4.4.7',
            'release': '16.el6',
            'arch': 'x86_64'
        }
    ),
    (
        'ncurses-libs-5.7-3.20090208.el6.i686',
        {
            'name': 'ncurses-libs',
            'epoch': '0',
            'version': '5.7',
            'release': '3.20090208.el6',
            'arch': 'i686'
        }
    ),
    (
        'perl-Compress-Raw-Zlib-2.021-136.el6_6.1.x86_64',
        {
            'name': 'perl-Compress-Raw-Zlib',
            'epoch': '0',
            'version': '2.021',
            'release': '136.el6_6.1',
            'arch': 'x86_64'
        }
    ),
    (
        'libX11-1.6.0-2.2.el6.x86_64',
        {
            'name': 'libX11',
            'epoch': '0',
            'version': '1.6.0',
            'release': '2.2.el6',
            'arch': 'x86_64'
        }
    ),
    (
        'pkgconfig-0.23-9.1.el6.x86_64',
        {
            'name': 'pkgconfig',
            'epoch': '0',
            'version': '0.23',
            'release': '9.1.el6',
            'arch': 'x86_64'
        }
    ),
    (
        'ruby-1.8.7.374-4.el6_6.x86_64',
        {
            'name': 'ruby',
            'epoch': '0',
            'version': '1.8.7.374',
            'release': '4.el6_6',
            'arch': 'x86_64'
        }
    ),
    (
        'openssl-1.0.1e-42.el6.x86_64',
        {
            'name': 'openssl',
            'epoch': '0',
            'version': '1.0.1e',
            'release': '42.el6',
            'arch': 'x86_64'
        }
    ),
    (
        'ntp-4.2.2p1-9.el5.centos.2.1.x86_64',
        {
            'name': 'ntp',
            'epoch': '0',
            'version': '4.2.2p1',
            'release': '9.el5.centos.2.1',
            'arch': 'x86_64'
        }
    ),
    (
        'ruby-1:1.8.7.374-4.el6_6.x86_64',
        {
            'name': 'ruby',
            'epoch': '1',
            'version': '1.8.7.374',
            'release': '4.el6_6',
            'arch': 'x86_64'
        }
    ),
    (
        'openssl-1.~0.1e-42.el6.x86_64',
        {
            'name': 'openssl',
            'epoch': '0',
            'version': '1.~0.1e',
            'release': '42.el6',
            'arch': 'x86_64'
        }
    ),
    (
        'firefox-45.0-4.fc22.x86_64',
        {
            'name': 'firefox',
            'epoch': '0',
            'version': '45.0',
            'release': '4.fc22',
            'arch': 'x86_64'
        }
    ),
    (
        'aaa_base-13.2+git20140911.61c1681-10.1.x86_64',
        {
            'name': 'aaa_base',
            'epoch': '0',
            'version': '13.2+git20140911.61c1681',
            'release': '10.1',
            'arch': 'x86_64'
        }
    )
]

version_info_no_arch = [
    ('.'.join(i[0].split('.')[:-1]), i[1]) for i in version_info
]


@pytest.mark.parametrize('version_info', version_info)
def test_pop_arch(version_info):
    """Test the pop_arch function"""
    vs, info = version_info
    char_list = list(vs)
    arch = rpm._pop_arch(char_list)
    assert info['arch'] == arch


@pytest.mark.parametrize('version_info', version_info)
def test_parse_information(version_info):
    """test the parse_information function for all version_info"""
    vs, info = version_info
    evr = (info['epoch'], info['version'], info['release'])
    parsed = rpm.parse_package(vs)
    assert info['name'] == parsed['name']
    assert evr == parsed['EVR']
    assert info['arch'] == parsed['arch']


@pytest.mark.parametrize('version_info', version_info)
def test_package(version_info):
    """Test the package function with all version_info"""
    vs, info = version_info
    expect = (info['name'], info['epoch'], info['version'],
              info['release'], info['arch'])
    pkg = rpm.package(vs)
    assert expect == pkg.info


@pytest.mark.parametrize('version_info', version_info_no_arch)
def test_package_no_arch(version_info):
    """Test the package function with the no_arch option"""
    vs, info = version_info
    expect = (info['name'], info['epoch'], info['version'],
              info['release'], None)
    pkg = rpm.package(vs, arch_included=False)
    assert expect == pkg.info


evr_list = [
    (('0', '1.0', '5a'), ('0', '1.0', '5a'), 0),
    (('0', '1.0', '5a'), ('1', '1.0', '5a'), -1),
    (('0', '1.1', '5a'), ('0', '1.0', '5a'), 1),
    (('0', '1.0', '5a'), ('0', '1.0', '5b'), -1),
]


@pytest.mark.parametrize('evr_a,evr_b,exp', evr_list)
def test_evrs(evr_a, evr_b, exp, func=rpm.compare_evrs):
    """Test the compare_evrs function"""
    res = func(evr_a, evr_b)
    assert res == exp


@pytest.mark.parametrize('evr_a,evr_b,exp', evr_list)
def test_label_compare(evr_a, evr_b, exp):
    """Test the label_compare function"""
    test_evrs(evr_a, evr_b, exp, func=rpm.labelCompare)


def test_parse_package_bad_package_no_arch():
    """Test that a package with no architecture raises an error"""
    with pytest.raises(errors.RpmError):
        rpm.parse_package('what_even_is_this_thing')


def test_parse_package_bad_package():
    """Test that an unparseable package raises an error"""
    with pytest.raises(errors.RpmError):
        rpm.parse_package('blargleblargle.aiiii')


@pytest.mark.parametrize('test,expect', [
    ('1.05', '1.05'),
    ('.104', '104'),
    ('~104', '~104'),
    ('~.4', '~.4'),
    ('!444', '444')
])
def test_check_leading(test, expect):
    """Check that stripping leading characters works as expected"""
    test_list = list(test)
    rpm._check_leading(test_list)
    res = ''.join(test_list)
    assert expect == res


@pytest.mark.parametrize('test,expect', [
    ('0012', '12'),
    ('120', '120'),
    ('000000000005', '5'),
    ('101', '101'),
    ('0000', '')
])
def test_trim_zeros(test, expect):
    """Test that zeros are trimmed as expected"""
    test_list = list(test)
    rpm._trim_zeros(test_list)
    res = ''.join(test_list)
    assert expect == res


@pytest.mark.parametrize('test_a,test_b', [
    (('0012', '12'), ('120', '120')),
    (('04', '4'), ('0', ''))
])
def test_trim_zeros_multi(test_a, test_b):
    """Test passing multiple arguments to trim_zeros"""
    a_test, a_expect = test_a
    b_test, b_expect = test_b
    a_list, b_list = list(a_test), list(b_test)
    rpm._trim_zeros(a_list, b_list)
    res_a, res_b = ''.join(a_list), ''.join(b_list)
    assert a_expect == res_a
    assert b_expect == res_b


@pytest.mark.parametrize('test,expect', [
    ('1.05', '1'),
    ('12.44', '12'),
    ('12a4.2', '12'),
    ('aa4', ''),
    ('.1234', '')
])
def test_pop_digits(test, expect):
    """Test that digit blocks are properly popped from strings"""
    test_list = list(test)
    digits = rpm._pop_digits(test_list)
    res = ''.join(digits)
    assert expect == res


@pytest.mark.parametrize('test,expect', [
    ('1.00', ''),
    ('aaer2r', 'aaer'),
    ('a23', 'a'),
    ('a.2', 'a'),
    ('.a22', '')
])
def test_pop_letters(test, expect):
    """Test that letter blocks are properly popped from strings"""
    test_list = list(test)
    letters = rpm._pop_letters(test_list)
    res = ''.join(letters)
    assert expect == res


@pytest.mark.parametrize('block_a,block_b,exp', [
    ('12345', '12345', 0),
    ('12345', '1234', 1),
    ('1234', '12345', -1),
    ('12345', '12346', -1),
    ('12346', '12345', 1),
    ('0012', '0012', 0),
    ('00123', '0012', 1),
    ('0012', '00123', -1),
    ('00123', '00124', -1),
    ('00124', '00123', 1),
    ('aawef', 'bawef', -1),
    ('boiwjef', 'aawoeijf', 1),
    ('aaaa', 'aaaa', 0)
])
def test_compare_blocks(block_a, block_b, exp):
    """Test block comparison"""
    list_a, list_b = list(block_a), list(block_b)
    res = rpm._compare_blocks(list_a, list_b)
    assert exp == res


@pytest.mark.parametrize('str_a,str_b,exp', [
    ('12.12', '12.13', 0),
    ('12.12', 'a.13', 1),
    ('a12.5', '12.5', -1),
    ('01ab', '01ac', 0),
    ('012ab', '02ab', 1),
    ('abc123', 'abc123', 0),
    ('abd123', 'abc123', 1)
])
def test_get_block_res(str_a, str_b, exp):
    """Test _get_block_res, which returns the result of the first block"""
    list_a, list_b = list(str_a), list(str_b)
    res = rpm._get_block_result(list_a, list_b)
    assert exp == res


@pytest.mark.parametrize('ver_a,ver_b,exp', [
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
])
def test_compare_versions(ver_a, ver_b, exp):
    res = rpm.compare_versions(ver_a, ver_b)
    assert exp == res
