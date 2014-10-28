#!/usr/bin/env python
# -*- coding: utf-8 -*-
import setuptools
from setuptools import setup, find_packages


if setuptools.__version__ < '0.7':
    raise RuntimeError("setuptools must be newer than 0.7")

version = "0.1.3"

setup(
    name="pinger",
    version=version,
    author="Pedro Palhares (pedrospdc)",
    author_email="pedrospdc@gmail.com",
    description="Website monitoring tool",
    url="https://github.com/pedrospdc/pinger",
    download_url="https://github.com/pedrospdc/pinger/tarball/{}".format(version),
    packages=find_packages(),
    zip_safe=False,
    license="MIT",
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Environment :: Console",
        "Intended Audience :: Developers",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
    ],
    install_requires=[
        "requests>=2.4.3",
        "peewee>=2.4.0"
    ],
    scripts=["bin/pinger"],
)
