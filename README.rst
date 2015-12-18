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
    sys_pkg = out
    
    # Get package information
    sys_pkg_info = rpm.parse_package(sys_pkg)
    sys_pkg_ver = sys_pkg_info['EVR'][1]
    
    # Compare versions
    result = rpm.compare_versions(pkg_req, sys_pkg_ver)
    
    if result < 0:  # sys_pkg was newer
        print('System package does not satisfy requirement!')

Note that ``parse_package`` returns a 3-tuple ``(epoc, version, requirement)``,
so if you only need to compare on version, you can pull it out from the tuple. 
