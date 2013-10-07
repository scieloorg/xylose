#!/usr/bin/env python
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="xylose",
    version='0.1',
    description="A SciELO library to abstract a JSON data structure that is a product of the ISIS2JSON conversion using the ISIS2JSON type 3 data model.",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD 2-clause",
    url="http://docs.scielo.org",
    packages=['xylose'],
    classifiers=[
        "Development Status :: 1 - Planning",
        "Intended Audience :: Customer Service",
        "License :: OSI Approved :: BSD License",
        "Programming Language :: Python",
        "Operating System :: POSIX :: Linux",
        "Topic :: System",
        "Topic :: Utilities",
    ],
    setup_requires=["nose>=1.0", "coverage"],
    tests_require=["mocker"],
    test_suite="nose.collector",
)