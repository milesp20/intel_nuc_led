"""
Python setuptools wrapper for Python 2.6 or greater.
"""

from __future__ import print_function

import os
import sys

try:
    from pkg_resources import parse_version
    from setuptools import find_packages, setup

    import setuptools
except ImportError as err:
    print('Python 2.6 or greater and setuptools is required for install:', file=sys.stderr)
    print('\thttps://packaging.python.org/en/latest/installing.html#requirements-for-installing-packages',
          file=sys.stderr)
    sys.exit(1)

def read_file(file_name):
    """
    File read wrapper for loading data unmodified from arbritrary file.
    """

    file_data = None

    try:
        with open(file_name, 'r') as fin:
            file_data = fin.read()
    except Exception as err: # pylint: disable=broad-except
        print('Failed to read data from file \'%s\': %s' % (file_name, str(err)), file=sys.stderr)
        sys.exit(1)

    return file_data

if issubclass(sys.version_info.__class__, tuple):
    PYTHON_VERSION = ".".join(map(str, sys.version_info[:3]))
else:
    PYTHON_VERSION = '.'.join(map(str, [sys.version_info.major, sys.version_info.minor, sys.version_info.micro]))

if parse_version(PYTHON_VERSION) < parse_version('2.6'):
    print('Python 2.6 or greater is required.')
    sys.exit(1)

PYTHON_3_EXTRAS = {}

if parse_version(PYTHON_VERSION) >= parse_version('3'):
    setuptools.use_2to3_on_doctests = True

    PYTHON_3_EXTRAS['convert_2to3_doctests'] = []
    PYTHON_3_EXTRAS['use_2to3'] = True
    PYTHON_3_EXTRAS['use_2to3_exclude_fixers'] = []
    PYTHON_3_EXTRAS['use_2to3_fixers'] = []

VERSION = read_file(os.path.join(os.path.dirname(__file__), 'VERSION')).strip()

setup( # pylint: disable=star-args
    author='Julio Lajara',
    author_email='julio@tvisioninsights.com',
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Environment :: Console',
        'Intended Audience :: Information Technology',
        'Intended Audience :: System Administrators',
        'License :: OSI Approved :: GNU General Public License v2 (GPLv2)',
        'Natural Language :: English',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Unix Shell',
        'Topic :: Software Development :: Libraries :: Python Modules',
        'Topic :: System :: Systems Administration',
        'Topic :: Utilities'
    ],
    description='NUC WMI CLI userland for intel_nuc_led kernel module',
    download_url='https://github.com/tvision-insights/intel_nuc_led',
    entry_points={
        'console_scripts': [
            
        ]
    },
    include_package_data=True,
    install_requires=[
        'setuptools'
    ],
    license='GPLv2',
    long_description=read_file('README.md'),
    keywords='cli intel kernel led nuc wmi',
    maintainer='Julio Lajara',
    maintainer_email='julio@tvisioninsights.com',
    name='nuc_wmi',
    package_dir={
        '': 'python'
    },
    packages=find_packages('python', exclude=['test', 'test.*']),
    setup_requires=[
        'setuptools'
    ],
    test_loader='setuptools.command.test:ScanningLoader',
    tests_require=[
        'coverage',
        'mock',
        'nose',
        'nose-cov',
        'setuptools'
    ],
    test_suite='test.unit.nuc_wmi',
    url='https://github.com/tvision-insights/intel_nuc_led',
    version=VERSION,
    zip_safe=True,
    **PYTHON_3_EXTRAS
)
