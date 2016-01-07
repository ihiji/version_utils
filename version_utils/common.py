"""
Module for implementation of functionality common to various package
management systems.
"""

# Standard library imports
from __future__ import (absolute_import, division,
                        print_function, unicode_literals)
from logging import getLogger

# Local imports

logger = getLogger(__name__)


class Package(object):
    """A class to hold information about a system package

    All parameters except ``name`` are optional and default to None

    :param str name: package name
    :param str epoch: epoch string, default None
    :param str version: version string, default None
    :param str release: release string, default None
    :param str arch: architecture string, default None
    :param str package: original package manager style package string,
        default None
    :ivar str name: package name
    :ivar str epoch: package epoch
    :ivar str version: package version
    :ivar str arch: package architecture
    :ivar tuple evr: a 3-tuple containing (epoch, version, release)
    :ivar tuple info: a 5-tuple containing (name, epoch, version, release,
        architecture)
    :ivar str package: the system-style package string
    """

    def __init__(self, name, epoch=None, version=None, release=None,
                 arch=None, package_str=None):
        self.name = name
        self.epoch = epoch
        self.version = version
        self.release = release
        self.arch = arch
        self.evr = (epoch, version, release)
        self.info = (name, epoch, version, release, arch)
        self.package = package_str

    def __str__(self):
        """Create a string representation of a Package object"""
        return ('Package Object: {0}'.format(self.info))

    def __repr__(self):
        """Full representation of a Package object"""
        return ('Package("{0}", "{1}", "{2}", "{3}", "{4}", '
                '"{5}")'.format(self.name, self.epoch, self.version,
                                self.release, self.arch, self.package))
