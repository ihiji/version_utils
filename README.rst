.. -*- mode: rst; coding: utf-8 -*-

==========================================================
version_utils - pure python version parsing and comparison
==========================================================

:Source:        https://github.com/ihiji/version_utils
:PyPI:          https://pypi.python.org/pypi/version_utils
:Travis:        https://travis-ci.org/ihiji/version_utils
:Maintainer:    Matthew Planchard <mplanchard@ihiji.com>
:License:       GPLv3

.. contents:: Table of Contents
    :backlinks: top

Introduction
------------

``version_utils`` is under active development. It is designed to provide a 
pure Python convenience library capable of parsing and comparing package and
version strings for a variety of packaging standards. Whenever possible,
the exact logic of existing package management comparison standards will be
implemented so that users can trust that the results are equivalent to what
they would get on the command-line.

Using ``version_utils`` ensures that packages can be compared even on systems
without access to the command line or distro-provided tools on various Linux
systems, allowing for easier and more consistent unit testing, safer 
deployment to multiple distributions, and easier and quicker development due
to a well-documented API and standardized function calls.

Current Status and Roadmap
--------------------------

Currently, only RPM/Yum style packages are supported, but we have plans to add
dpkg/Debian in the near future. Development will probably slow from there, 
although Pacman/Arch and various other distributions are on the radar.

Note that the ``compare_versions`` function in the ``rpm`` module will probably
work for the majority of ``.deb`` package versions. However, there are some
differences, and it will fail in certain cases. Use at your own risk until
official support for debian version parsing is released.

Installation
------------

This package has no dependencies, so a simple::

    pip install version_utils

should suffice. Feel free to build from source as well, if you prefer.

Basic Use
---------

Check the API documentation to ensure the module you are seeking to use is
present. The example below uses the ``rpm`` module. From your application::

    from subprocess import PIPE, Popen
    from version_utils import rpm
    
    pkg_req = 1.07
    
    # Get a package string for an installed package
    out, err = Popen(['rpm', '-q', 'foo'], stdout=PIPE, stderr=PIPE).communicate()
    sys_pkg_str = out
    
    # Get package information
    sys_package = rpm.package(sys_package)
    sys_pkg_name = sys_package.name
    sys_pkg_version = sys_package.version

    # Compare versions
    result = rpm.compare_versions(pkg_req, sys_pkg_version)
    
    if result < 0:  # sys_pkg was newer
        print('System package {0} does not satisfy
              requirement!'.format(sys_pkg_name))


In addition to indirectly comparing versions, a ``compare_packages``
function is provided to directly compare package strings, using the
same logic as the package manager::

    from version_utils import rpm

    sys_pkg = 'perl-Compress-Raw-Zlib-2.021-136.el6_6.1.x86_64'
    repo_pkg = 'perl-Compress-Raw-Zlib-2.021-138.el6_6.1.x86_64'

    result = rpm.compare_packages(repo_pkg, sys_pkg)

    if result > 0:  # repo_pkg is newer
        print('Repo package is newer')


The ``Package`` class can be used to succinctly transmit package
information. A factory function, ``rpm.package()``, is provided to
instantiate ``Package`` instances::

    from version_utils import rpm

    pkg_str = 'pkgconfig-0.23-9.1.el6.x86_64'
    pkg = rpm.package(pkg_str)

    # Get package name, epoch, version, release, and architecture as a tuple
    print(pkg.info)

    # Access the package string that was parsed to make the Package object
    print(pkg.package)

    # Access the epoch, version, and release information as a tuple
    print(pkg.evr)

    # Access name, epoch, version, release, and architecture independently
    print('Name: {0}, Epoch: {1}, Version: {2}, Release: {3}, Arch:
          {4}'.format(pkg.name, pkg.epoch, pkg.version, pkg.release, pkg.arch))


Contributing
------------

Contributions to ``version_utils`` are welcome. Feel free to fork, raise
issues, etc.


Contributors
------------

I would like to express my sincere thanks to the following GitHub users for
their contributions to and assistance with this project:

* Joseph Knight (jknightihiji_)
* Thomas Hoger (thoger_)
* Marcus Furlong (furlongm_)

.. _jknightihiji: https://github.com/jknightihiji
.. _thoger: https://github.com/thoger
.. _furlongm: https://gibhub.com/furlongm


Changelog
---------

0.3.0
+++++

Added labelCompare functionality for parity with the official `rpm`
package

Updated tests to use py.test; added more tests

Improved test logging

Improved logging efficiency with `%s` formatting

0.2.3
+++++

Fixed issue `#7`_ where version strings without epoch strings and with multi-
digit primary version numbers would return the first digit of the primary
version as the epoch and the second digit as the primary version.

.. _#7: https://github.com/ihiji/version_utils/issues/7

0.2.2
+++++

Added ``version.py`` with automatic version parsing by ``setup.py``

Added ``rpm`` and ``common`` modules to ``__init__.py``

Imported ``__version__`` and ``__version_info__`` information into
``__init__.py``

Added ``tox.ini`` and tox integration

Improved error handling in the ``compare_versions`` function in ``rpm``

0.2.1
+++++

Bugfix release only

0.2.0
+++++

Added `common.Package` class and `rpm.package` method to
return a Package object when parsing package strings.

Deprecated public access to the `rpm.parse_package` method, although the
function remains unchanged for backwards compatibility.

0.1.1
+++++

Added VersionUtilsError and RpmError classes. RpmError is thrown
if a package string cannot be parsed. All errors inherit from
VersionUtilsError

0.1.0
+++++

Initial release

