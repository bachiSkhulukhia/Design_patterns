# import sqlite3
# from dataclasses import dataclass
# from sqlite3 import Connection
# from typing import Any, Protocol
#
#
# class IDatabaseAccess(Protocol):
#     def get_access_object(self) -> Any:
#         pass
#
#
# class IDatabaseFactory(Protocol):
#     def create_database(self) -> IDatabaseAccess:
#         pass
#
#
# class SQLiteDatabaseAccess(IDatabaseAccess):
#     conn: Connection
#
#     def get_access_object(self) -> Any:
#         return self.conn
#
#
# @dataclass
# class SqlLiteDatabaseFactory(IDatabaseFactory):
#     database_name: str
#
#     def create_database(self) -> SQLiteDatabaseAccess:
#         datasource = sqlite3.connect(self.database_name)
#         return SQLiteDatabaseAccess(datasource)
