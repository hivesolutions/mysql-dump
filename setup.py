#!/usr/bin/python
# -*- coding: utf-8 -*-

# MySQL Dump System
# Copyright (C) 2008-2014 Hive Solutions Lda.
#
# This file is part of MySQL Dump System.
#
# MySQL Dump System is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# MySQL Dump System is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with MySQL Dump System. If not, see <http://www.gnu.org/licenses/>.

__author__ = "João Magalhães <joamag@hive.pt>"
""" The author(s) of the module """

__version__ = "1.0.0"
""" The version of the module """

__revision__ = "$LastChangedRevision$"
""" The revision number of the module """

__date__ = "$LastChangedDate$"
""" The last change date of the module """

__copyright__ = "Copyright (c) 2008-2014 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import setuptools

setuptools.setup(
    name = "mysql_dump",
    version = "0.2.0",
    author = "Hive Solutions Lda.",
    author_email = "development@hive.pt",
    description = "MySQL Dump System",
    license = "GNU General Public License (GPL), Version 3",
    keywords = "mysql dump database export",
    url = "http://mysqldump.hive.pt",
    zip_safe = True,
    py_modules = [
        "mysql_dump"
    ],
    package_dir = {
        "" : os.path.normpath("src")
    },
    entry_points = {
        "console_scripts" : [
            "mysql_dump = mysql_dump:main"
        ]
    },
    classifiers = [
        "Development Status :: 5 - Production/Stable",
        "Topic :: Utilities",
        "License :: OSI Approved :: GNU General Public License (GPL)",
        "Operating System :: OS Independent",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2.6",
        "Programming Language :: Python :: 2.7"
    ]
)
