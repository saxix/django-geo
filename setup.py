#!/usr/bin/env python
import os
import codecs
from distutils.config import PyPIRCCommand
from setuptools import setup, find_packages

dirname = 'geo'

app = __import__(dirname)


def read(*parts):
    here = os.path.abspath(os.path.dirname(__file__))
    return codecs.open(os.path.join(here, *parts), 'r').read()


tests_require = read('geo/requirements/testing.pip')

setup(
    name=app.NAME,
    version=app.get_version(),
    url='https://github.com/saxix/django-geo',
    description="A Django application which manage administrative geographical data.",
    download_url='https://github.com/saxix/django-geo/tarball/master',
    author='sax',
    author_email='sax@os4d.org',
    license='BSD',
    packages=find_packages('.'),
    include_package_data=True,
    platforms=['any'],
    install_requires=read('geo/requirements/install.pip'),
    command_options={
        'build_sphinx': {
            'version': ('setup.py', app.VERSION),
            'release': ('setup.py', app.VERSION)}
    },
    classifiers=[
        'Environment :: Web Environment',
        'Framework :: Django',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Intended Audience :: Developers',
    ],
    long_description=open('README.rst').read()
)
