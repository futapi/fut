#!/usr/bin/env python
# -*- coding: utf-8 -*-
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


__title__ = 'fut'
__version__ = '0.1.2'
__author__ = 'Piotr Staroszczyk'
__author_email__ = 'piotr.staroszczyk@get24.org'
__license__ = 'GNU GPL v3'
__copyright__ = 'Copyright 2013 Piotr Staroszczyk'

packages = [
    __title__,
    # '%s.modules' % __title__,
]

with open('requirements.txt') as f:
    requires = f.read().splitlines()

with open('README.rst') as f1:
    with open('CHANGELOG.rst') as f2:
        long_desc = f1.read() + '\n\n' + f2.read()

setup(
    name=__title__,
    version=__version__,
    description='%s is a simple library for managing Fifa Ultimate Team.' % __title__,
    long_description=long_desc,
    author=__author__,
    author_email=__author_email__,
    url='https://github.com/oczkers/%s' % __title__,
    download_url='https://github.com/oczkers/%s/releases' % __title__,
    bugtrack_url='https://github.com/oczkers/%s/issues' % __title__,
    platforms='any',
    keywords='%s fifa ultimate team ut pc xbox android ios 360 ps3 playstation' % __title__,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={__title__: __title__},
    include_package_data=True,
    install_requires=requires,
    # license=open('LICENSE').read(),
    license=__license__,
    classifiers=(
        'Development Status :: 3 - Alpha',
        # 'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        # 'Programming Language :: Python :: 3.0',  # not tested
        # 'Programming Language :: Python :: 3.1',  # not tested
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        # 'Programming Language :: Python :: 3.4',  # not tested
        # 'Programming Language :: Python :: Implementation :: CPython',  # not tested
        # 'Programming Language :: Python :: Implementation :: IronPython',  # not tested
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
    # entry_points={
    #     'console_scripts': [
    #         'fut = fut.cli:main',
    #     ]
    # }
)
