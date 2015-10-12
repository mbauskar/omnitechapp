# -*- coding: utf-8 -*-
from setuptools import setup, find_packages
import os

version = '0.0.1'

setup(
    name='omnitechapp',
    version=version,
    description='omnitechapp',
    author='omnitechapp',
    author_email='omnitechapp',
    packages=find_packages(),
    zip_safe=False,
    include_package_data=True,
    install_requires=("frappe",),
)
