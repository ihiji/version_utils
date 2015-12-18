"""
setup.py module for version_utils
"""


from __future__ import (absolute_import, unicode_literals)
from setuptools import setup, find_packages


long_description = ('version_utils is a pure Python convenience library for'
                    'parsing system package strings and comparing package '
                    'versions. Currently it only supports RPM/Yum, but there '
                    'are plans in the near future to add dpkg/Debian and '
                    'other packaging standards.')


setup(
    name='version_utils',
    version='0.1.0',
    description=('Library for parsing system package strings and comparing '
                 'package versions'),
    url='http://www.github.com/ihiji/version_utils',
    author='Matthew Planchard',
    author_email='mplanchard@ihiji.com',
    license='License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Console',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: Software Development :: Version Control',
        'Topic :: System :: Software Distribution',
        'Topic :: Utilities'
    ],
    keywords=('ihiji version compare parse rpm yum versions comparison '
              'utility utilities control distribution'),
    packages=find_packages(where='version_utils')
)
