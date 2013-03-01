#!/usr/bin/python
# -*- coding: utf-8 -*-

# MySQL Dump System
# Copyright (C) 2008-2012 Hive Solutions Lda.
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

__copyright__ = "Copyright (c) 2008-2012 Hive Solutions Lda."
""" The copyright for the module """

__license__ = "GNU General Public License (GPL), Version 3"
""" The license for the module """

import os
import sys
import types
import shutil
import zipfile
import MySQLdb

VERSION = "0.1.0"
""" The current version value for the mysql dump executable """

RELEASE = "100"
""" The release value, should be an internal value related
with the build process """

BUILD = "1"
""" The build value, representing the sub release value
existent in the build process """

RELEASE_DATE = "1 March 2013"
""" The release date value for the current version """

BRANDING_TEXT = "MySQL Dump System %s (Hive Solutions Lda. r%s:%s %s)"
""" The branding text value the template based values
should be defined as constants """

VERSION_PRE_TEXT = "Python "
""" The version pre text value, that appears before the printing
of the branding text second line """

CONVERSION = {
    str : lambda v: "'%s'" % _escape(v),
    unicode : lambda v: "'%s'" % _escape(v.encode("utf-8")),
    int : lambda v: str(v),
    long : lambda v: str(v),
    float : lambda v: str(v),
    types.NoneType : lambda v: "null"
}

RESOLVE = {
    "PRI" : "primary key"
}

## OBJECTIVES
## LER UM JSON global que esta no home directory ou no /etc com a configuracao da migracao

class Exporter:

    def __init__(self, database, host = None, user = None, password = None):
        self.database = database
        self.host = host or "127.0.0.1"
        self.user = user or "root"
        self.password = password or ""
        self.base_path = "c:/export"
        self.connection = None

    def connect(self):
        if self.connection: return
        self.connection = MySQLdb.connect(
            self.host,
            user = self.user,
            passwd = self.password,
            db = self.database
        )

    def ensure(self):
        if self.connection: return
        self.connect()

    def dump(self):
        print("------------------------------------------------------------------------")
        print("Dumping '%s' database into '%s'" % (self.database, self.base_path))
        self.connect()
        if not os.path.exists(self.base_path): os.makedirs(self.base_path)

        try:
            self.dump_schema()
            self.dump_tables()
            self.compress()
        finally:
            shutil.rmtree(self.base_path, ignore_errors = True)

    def dump_schema(self):
        file_path = os.path.join(self.base_path, "schema.sql")
        file = open(file_path, "wb")
        try: self._dump_schema(file)
        finally: file.close()

    def _dump_schema(self, file):
        tables = self.fetch_s(
            "select table_name from information_schema.tables where table_schema = '%s'" % self.database
        )

        # retrieves the current tables length (amount of tables)
        # so that it's possible to calculate the percentage of
        # completion for the current process
        tables_l = len(tables)
        index = 1

        for table in tables:
            print "\r[dump schema] %d/%d tables exported" % (index, tables_l),

            columns = self.fetch_a(
                "select column_name, column_type, column_key\
                     from information_schema.columns\
                     where table_schema = '%s' and table_name = '%s'" %\
                (self.database, table)
            )

            keys = [column[0] for column in columns if column[2] == "PRI"]
            keys_s = ", ".join(keys)
            file.write("create table %s (\n" % table)
            for column in columns:
                column = list(column)
                del column[2]

                column_s = " ".join(column)
                file.write("    %s,\n" % column_s)

            file.write("    primary key(%s)" % keys_s)
            file.write("\n);\n")

            index += 1

    def dump_tables(self):
        tables = self.fetch_s(
            "select table_name from information_schema.tables where table_schema = '%s'" % self.database
        )

        # retrieves the current tables length (amount of tables)
        # so that it's possible to calculate the percentage of
        # completion for the current process
        tables_l = len(tables)
        index = 1

        for table in tables:
            print "\r[dump tables] %d/%d tables exported" % (index, tables_l),

            columns = self.fetch_s(
                "select column_name from information_schema.columns where table_schema = '%s' and table_name = '%s'" %\
                (self.database, table)
            )
            columns_s = ", ".join(columns)
            data = self.fetch_a(
                "select %s from %s" % (columns_s, table)
            )

            file_path = os.path.join(self.base_path, table + ".dmp")
            file = open(file_path, "wb")
            try: self.dump_data(file, data)
            finally: file.close()

            index += 1

    def dump_data(self, file, data):
        for item in data:
            is_first = True
            for value in item:
                if is_first: is_first = False
                else: file.write(",")
                value_t = type(value)
                value_f = CONVERSION.get(value_t, str)
                value_s = value_f(value)
                file.write(value_s)
            file.write("\n")

    def compress(self, target = None):
        target = target or self.base_path + ".zip"
        zip = zipfile.ZipFile(target, "w", zipfile.ZIP_DEFLATED)
        try:
            root_l = len(self.base_path) + 1
            for base, _dirs, files in os.walk(self.base_path):
                for file in files:
                    path = os.path.join(base, file)
                    zip.write(path, path[root_l:])
        finally:
            zip.close()

    def fetch_o(self, query):
        self.ensure()
        cursor = self.connection.cursor()
        cursor.execute(query)
        try: data = cursor.fetchone()
        finally: cursor.close()
        return data

    def fetch_a(self, query):
        self.ensure()
        cursor = self.connection.cursor()
        cursor.execute(query)
        try: data = cursor.fetchall()
        finally: cursor.close()
        return data

    def fetch_s(self, query):
        data = self.fetch_a(query)
        elements = [item[0] for item in data]
        return elements

def dump(database, host = None, user = None, password = None):
    exporter = Exporter(
        database,
        host = host,
        user = user,
        password = password
    )
    exporter.dump()

def information():
    # print the branding information text and then displays
    # the python specific information in the screen
    print(BRANDING_TEXT % (VERSION, RELEASE, BUILD, RELEASE_DATE))
    print(VERSION_PRE_TEXT + sys.version)

def _escape(value):
    return value.replace("'", "''")

def main():
    #dump(
    #    "test",
    #    host = "hole1.hive",
    #    user = "root",
    #    password = "root"
    #)

    #dump(
    #    "wordpress",
    #    host = "db.hive",
    #    user = "root",
    #    password = "root"
    #)

    information()
    dump(
        "ldj_omni_release",
        host = "servidor5.hive",
        user = "root",
        password = "root"
    )    

if __name__ == "__main__":
    main()
