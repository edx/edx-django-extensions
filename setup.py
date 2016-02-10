#!/usr/bin/env python
# pylint: disable=missing-docstring

from setuptools import setup, find_packages

setup(
    name='edx-management-commands',
    version='0.0.1',
    description='Reusable automation and configuration utilities for edX Django applications',
    author='edX',
    url='https://github.com/edx/edx-django-extensions',
    license='AGPL',
    classifiers=[
        'Development Status :: 3 - Alpha',
        'Environment :: Web Environment',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Framework :: Django',
    ],
    packages=find_packages(exclude=['tests']),
    install_requires=[
        'django>=1.8.7,<1.9',
    ],
)
