:: MySQL Dump System
:: Copyright (C) 2008-2014 Hive Solutions Lda.
::
:: This file is part of MySQL Dump System.
::
:: MySQL Dump System is free software: you can redistribute it and/or modify
:: it under the terms of the GNU General Public License as published by
:: the Free Software Foundation, either version 3 of the License, or
:: (at your option) any later version.
::
:: MySQL Dump System is distributed in the hope that it will be useful,
:: but WITHOUT ANY WARRANTY; without even the implied warranty of
:: MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
:: GNU General Public License for more details.
::
:: You should have received a copy of the GNU General Public License
:: along with MySQL Dump System. If not, see <http://www.gnu.org/licenses/>.

:: __author__    = João Magalhães <joamag@hive.pt>
:: __version__   = 1.0.0
:: __revision__  = $LastChangedRevision$
:: __date__      = $LastChangedDate$
:: __copyright__ = Copyright (c) 2008-2014 Hive Solutions Lda.
:: __license__   = GNU General Public License (GPL), Version 3

:: turns off the echo
@echo off

:: sets the temporary variables
set RELATIVE_PATH=../lib/
set SCRIPT_NAME=mysql_dump.py

:: executes the initial python script with
:: the provided arguments
python "%~dp0/%RELATIVE_PATH%/%SCRIPT_NAME%" %*

:: exits the process
exit /b %ERRORLEVEL%
