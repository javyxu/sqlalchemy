# rasdaman/base.py
# Copyright (C) 2005-2018 the SQLAlchemy authors and contributors
# <see AUTHORS file>
#
# This module is part of SQLAlchemy and is released under
# the MIT License: http://www.opensource.org/licenses/mit-license.php

r"""
.. dialect:: rasdaman
    :name: rasdaman

"""
from ... import exc
from ...engine import default


class RASDialect(default.DefaultDialect):
    name = 'rasdaman'

    isolation_level = None

    def __init__(self, isolation_level=None, **kwargs):
        default.DefaultDialect.__init__(self, **kwargs)
        
    def initialize(self, connection):
        super(RASDialect, self).initialize(connection)

    def on_connect(self):
        if self.isolation_level is not None:
            def connect(conn):
                self.set_isolation_level(conn, self.isolation_level)
            return connect
        else:
            return None

    _isolation_lookup = set(['SERIALIZABLE', 'READ UNCOMMITTED',
                             'READ COMMITTED', 'REPEATABLE READ'])

    def set_isolation_level(self, connection, level):
        level = level.replace('_', ' ')
        if level not in self._isolation_lookup:
            raise exc.ArgumentError(
                "Invalid value '%s' for isolation_level. "
                "Valid isolation levels for %s are %s" %
                (level, self.name, ", ".join(self._isolation_lookup))
            )
        cursor = connection.cursor()
        cursor.execute(
            "SET SESSION CHARACTERISTICS AS TRANSACTION "
            "ISOLATION LEVEL %s" % level)
        cursor.execute("COMMIT")
        cursor.close()