#!/usr/bin/env python
import scielodocument
try:
    from setuptools import setup
except ImportError:
    from distutils.core import setup


setup(
    name="scielodocument",
    version='.'.join(scielodocument.__version__),
    description="Utility to load article documents from the xmlwos API.",
    author="SciELO",
    author_email="scielo-dev@googlegroups.com",
    license="BSD 2-clause",
    url="http://docs.scielo.org",
    packages=['scielodocument'],
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