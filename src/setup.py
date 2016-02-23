# -*- coding: utf-8 -*-

"""

setup.py  -  set up program for PyMapLib

======================================================================
AUTHOR:  Wei Wan, Purdue University

EMAIL:   rcac-help@purdue.edu

Copyright (c) 2016  Purdue University

See the file "license.terms" for information on usage and
redistribution of this file, and for a DISCLAIMER OF ALL WARRANTIES.

======================================================================

"""

import os
import sys
from distutils.sysconfig import get_python_lib

from setuptools import find_packages, setup

# Warn if we are installing over top of an existing installation. This can
# cause issues where files that were deleted from a more recent Django are
# still present in site-packages. See #18115.
overlay_warning = False
if "install" in sys.argv:
    lib_paths = [get_python_lib()]
    if lib_paths[0].startswith("/usr/lib/"):
        # We have to try also with an explicit prefix of /usr/local in order to
        # catch Debian's custom user site-packages directory.
        lib_paths.append(get_python_lib(prefix="/usr/local"))
    for lib_path in lib_paths:
        existing_path = os.path.abspath(os.path.join(lib_path, "gabbs"))
        if os.path.exists(existing_path):
            # We note the need for the warning here, but present it after the
            # command is run, so it's more likely to be seen.
            overlay_warning = True
            break


EXCLUDE_FROM_PACKAGES = ['test',
                         'test.*',
                         'test.bin']


setup(
    name='GabbsMaps',
    version='1.0',
    url='https://mygeohub.org',
    author='Eric Wei Wan',
    author_email='wanw@purdue.edu',
    description=('A Python maps API that enables '
                 'geospatial data visualization.'),
    license='MIT',
    packages=find_packages(),
    #packages=find_packages(exclude=EXCLUDE_FROM_PACKAGES),
    package_data = {
        '': ['*.txt'],
        'gabbs': ['resources/style/*.qml'],
        'gabbs': ['layers/gdal_tms/*.xml'],
    },
    include_package_data=True,
)


if overlay_warning:
    sys.stderr.write("""
========
WARNING!
========
You have just installed GABBs Maps over top of an existing
installation, without removing it first. Because of this,
your install may now include extraneous files from a
previous version that have since been removed from
GABBs Maps. This is known to cause a variety of problems. You
should manually remove the
%(existing_path)s
directory and re-install GABBs Maps.
""" % {"existing_path": existing_path})
