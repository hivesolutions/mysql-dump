#!/bin/sh
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

# __author__    = João Magalhães <joamag@hive.pt>
# __version__   = 1.0.0
# __revision__  = $LastChangedRevision$
# __date__      = $LastChangedDate$
# __copyright__ = Copyright (c) 2008-2014 Hive Solutions Lda.
# __license__   = GNU General Public License (GPL), Version 3

# sets the temporary variables
USR_BIN_PATH=/usr/bin
PYTHON_PATH=$USR_BIN_PATH/python
SCRIPT_NAME=mysql_dump_pypi.py

# retrieves the script directory path
SCRIPT_DIRECTORY_PATH=$(dirname $(readlink -f $0))

# executes the initial python script with
# the provided arguments
$PYTHON_PATH "$SCRIPT_DIRECTORY_PATH/$SCRIPT_NAME" "$@"

# exits the process
exit $?
