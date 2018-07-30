#!/usr/bin/env python
from setuptools import setup


requires = [
    "legendarium>=1.2.0"
]

setup(
    name="xylose",
    version='1.33.2',
    description="A SciELO library to abstract a JSON data structure that is a "
                "product of the ISIS2JSON conversion using the ISIS2JSON type "
                "3 data model.",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD 2-clause",
    url="http://docs.scielo.org",
    packages=['xylose'],
    include_package_data=True,
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Utilities",
    ],
    dependency_links=[],
    setup_requires=[],
    tests_require=[],
    install_requires=requires,
    test_suite="tests",
)
