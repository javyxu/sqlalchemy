# coding: utf-8

from sqlalchemy.testing.assertions import (
    eq_, assert_raises, assert_raises_message, AssertsExecutionResults,
    AssertsCompiledSQL)
from sqlalchemy.testing import engines, fixtures
from sqlalchemy import testing
import datetime
from sqlalchemy import (
    Table, Column, select, MetaData, text, Integer, String, Sequence, Numeric,
    DateTime, BigInteger, func, extract, SmallInteger, TypeDecorator, literal,
    cast, bindparam)
from sqlalchemy import exc, schema
from sqlalchemy.dialects.rasdaman import base as rasdaman
import logging
import logging.handlers
from sqlalchemy.testing.mock import Mock
from sqlalchemy.engine import engine_from_config
from sqlalchemy.engine import url
from sqlalchemy.testing import is_
from sqlalchemy.testing import expect_deprecated
from ...engine import test_execute
from sqlalchemy import dialects


class DialectTest(fixtures.TestBase):
    """python-side dialect tests.  """

    def test_version_parsing(self):

        def mock_conn(res):
            return Mock(
                execute=Mock(return_value=Mock(scalar=Mock(return_value=res))))

        dialect = rasdaman.dialect()

    def test_deprecated_dialect_name_still_loads(self):
        dialects.registry.clear()
        with expect_deprecated(
                "The 'postgres' dialect name "
                "has been renamed to 'postgresql'"):
            dialect = url.URL("postgres").get_dialect()
        is_(dialect, rasdaman.dialect)