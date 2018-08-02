#!/usr/bin/env python
# -*- coding: utf-8 -*-

# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT license.


import os

from setuptools import setup, find_packages
from setuptools.command.develop import develop
from setuptools.command.install import install
from setuptools.command.build_py import build_py


def _pre_install(dir):
    from subprocess import check_call
    check_call(['./setup.sh'], shell=True, cwd=os.getcwd())

    # Install local version of Jericho
    try:
        from pip import main as pipmain
    except:
        from pip._internal import main as pipmain
    pipmain(['install', os.path.join(os.getcwd(), "jericho")])


class CustomInstall(install):
    def run(self):
        self.execute(_pre_install, (self.install_lib,),
                     msg="Running post install task")
        install.run(self)


class CustomDevelop(develop):
    def run(self):
        self.execute(_pre_install, (self.install_lib,),
                     msg="Running post install task")
        develop.run(self)


class CustomBuildPy(build_py):
    def run(self):
        _pre_install(None)
        build_py.run(self)


setup(
    name='textworld',
    version='0.0.3',
    author='',
    cmdclass={
        'build_py': CustomBuildPy,
        'install': CustomInstall,
        'develop': CustomDevelop
    },
    packages=find_packages(),
    include_package_data=True,
    scripts=[
        "scripts/tw-data",
        "scripts/tw-play",
        "scripts/tw-make",
        "scripts/tw-stats",
    ],
    license='',
    zip_safe=False,
    description="Microsoft Textworld - A Text-based Learning Environment.",
    cffi_modules=["glk_build.py:ffibuilder"],
    setup_requires=['cffi>=1.0.0'],
    install_requires=open('requirements.txt').readlines(),
    test_suite='nose.collector',
    tests_require=[
        'nose==1.3.7',
    ],
    extras_require={
        'vis': ['pybars3>=0.9.3', 'flask>=1.0.2', 'selenium>=3.12.0', 'gevent>=1.3.2', 'pillow>=5.1.0', 'chromedriver_installer'],
        'prompt': ['prompt-toolkit<2.0.0,>=1.0.15'],
        'gym': ['gym_textworld'],
    },
)
