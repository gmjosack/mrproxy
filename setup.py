#!/usr/bin/env python

from distutils.core import setup

execfile("mrproxy/version.py")


kwargs = {
    "name": "mrproxy",
    "version": str(__version__),
    "packages": ["mrproxy"],
    "scripts": ["bin/mrproxy"],
    "description": "Mediocre Reverse Proxy.",
    # PyPi, despite not parsing markdown, will prefer the README.md to the
    # standard README. Explicitly read it here.
    "long_description": open("README").read(),
    "author": "Gary M. Josack",
    "maintainer": "Gary M. Josack",
    "author_email": "gary@byoteki.com",
    "maintainer_email": "gary@byoteki.com",
    "license": "MIT",
    "url": "https://github.com/gmjosack/mrproxy",
    "download_url": "https://github.com/gmjosack/mrproxy/archive/master.tar.gz",
    "classifiers": [
        "Programming Language :: Python",
        "Topic :: Software Development",
        "Topic :: Software Development :: Libraries",
        "Topic :: Software Development :: Libraries :: Python Modules",
    ]
}

setup(**kwargs)
