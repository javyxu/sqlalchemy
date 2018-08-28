# postgresql/pyrasdaman.py
# Copyright (C) 2005-2018 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

r"""
.. dialect:: rasdaman+pyrasdaman
    :name: pyrasdaman
    :dbapi: rasdapy
    :connectstring: rasdaman+pyrasdaman://user:password@host:port/dbname[?key=value&key=value...]
    :url: http://pypi.python.org/pypi/rasdapy/

"""

from __future__ import absolute_import

import re

from ... import util, exc
from .base import RASDialect

class RASDialect_pyrasdaman(RASDialect):
    driver = 'pyrasdaman'

    pyrasdaman_version = (0, 0)

    def __init__(self, **kwargs):
        RASDialect.__init__(self, **kwargs)
        if self.dbapi and hasattr(self.dbapi, '__version__'):
            m = re.match(r'(\d+)\.(\d+)(?:\.(\d+))?',
                         self.dbapi.__version__)
            if m:
                self.pyrasdaman_version = tuple(
                    int(x)
                    for x in m.group(1, 2, 3)
                    if x is not None)

    def initialize(self, connection):
        super(RASDialect_pyrasdaman, self).initialize(connection)

    @classmethod
    def dbapi(cls):
        import rasdapy
        return rasdapy

    @classmethod
    def _pyrasdaman_core(cls):
        from rasdapy.cores import core
        return core

    # @classmethod
    # def _psycopg2_extras(cls):
    #     from psycopg2 import extras
    #     return extras

    def set_isolation_level(self, connection, level):
        try:
            level = 'AUTOCOMMIT'
        except KeyError:
            raise exc.ArgumentError(
                "Invalid value '%s' for isolation_level. "
                "Valid isolation levels for %s are %s" %
                (level, self.name, ", ".join(self._isolation_lookup))
            )

        connection.set_isolation_level(level)

    # def on_connect(self):

    #     return None
        
    
    def create_connect_args(self, url):
        opts = url.translate_connect_args(username='user')
        if 'port' in opts:
            opts['port'] = int(opts['port'])
        else:
            opts['port'] = 7001
        opts.update(url.query)
        return ([], opts)

    def is_disconnect(self, e, connection, cursor):
        if isinstance(e, self.dbapi.Error):
            # check the "closed" flag.  this might not be
            # present on old psycopg2 versions.   Also,
            # this flag doesn't actually help in a lot of disconnect
            # situations, so don't rely on it.
            if getattr(connection, 'closed', False):
                return True
        return False

dialect = RASDialect_pyrasdaman