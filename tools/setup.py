#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import find_packages, setup

requirements = ['Click>=6.0',
                'pandas',
                'tweepy',
                'feather-format',
                'xlutils',
                'openpyxl',
                ]

setup_requirements = ['pytest-runner', ]

test_requirements = ['pytest', ]

setup(
    author="Khalid Chakhmoun",
    author_email='fr.ckhalid@gmail.com',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'Natural Language :: English',
        'Programming Language :: Python :: 3.6',
    ],
    description="Tools",
    entry_points={
        'console_scripts': [
            'tools=tools.cli:main',
        ],
    },
    install_requires=requirements,
    include_package_data=True,
    keywords='tools',
    name='tools',
    packages=find_packages(include=['tools']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/KhalidCK/tools',
    version='0.1.0',
    zip_safe=False,
)
