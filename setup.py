#!/usr/bin/env python
# -*- coding: utf-8 -*-
import fut14

try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup

packages = [
    'fut14',
    #'fut14.modules',
]

requires = []

setup(
    name=fut14.__title__,
    version=fut14.__version__,
    #description='',
    long_description=open('README.rst').read(),
    author=fut14.__author__,
    author_email=fut14.__author_email__,
    packages=packages,
    package_data={'': ['LICENSE']},
    package_dir={'fut14': 'fut14'},
    include_package_data=True,
    install_requires=requires,
    license=open('LICENSE').read(),
    classifiers=(
        'Development Status :: 3 - Alpha',
        #'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2.6',
        'Programming Language :: Python :: 2.7',
        #'Programming Language :: Python :: 3',
        #'Programming Language :: Python :: 3.0',  # not tested
        #'Programming Language :: Python :: 3.1',  # not tested
        #'Programming Language :: Python :: 3.2',  # not tested
        #'Programming Language :: Python :: 3.3',
        #'Programming Language :: Python :: Implementation :: CPython',  # not tested
        #'Programming Language :: Python :: Implementation :: IronPython',  # not tested
        'Programming Language :: Python :: Implementation :: PyPy',
        'Topic :: Internet :: WWW/HTTP :: Site Management',
        'Topic :: Software Development :: Libraries :: Python Modules',
    ),
#    entry_points={
#        'console_scripts': [
#            'fut14 = fut14.cli:main',
#        ]
#    }
)
