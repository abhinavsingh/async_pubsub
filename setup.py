# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import async_pubsub

classifiers = [
    'Development Status :: 4 - Beta',
    'Environment :: Console',
    'Intended Audience :: Developers',
    'Intended Audience :: System Administrators',
    'License :: OSI Approved :: BSD License',
    'Operating System :: MacOS',
    'Operating System :: POSIX',
    'Operating System :: Unix',
    'Programming Language :: Python :: 2.7',
    'Topic :: Utilities',
]

install_requires = open('requirements.txt', 'rb').read().strip().split()

setup(
    name                = 'async_pubsub',
    version             = async_pubsub.__version__,
    description         = async_pubsub.__description__,
    long_description    = open('README.md').read().strip(),
    author              = async_pubsub.__author__,
    author_email        = async_pubsub.__author_email__,
    url                 = async_pubsub.__homepage__,
    license             = async_pubsub.__license__,
    packages            = find_packages(),
    install_requires    = install_requires,
    classifiers         = classifiers
)