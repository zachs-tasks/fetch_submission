from __future__ import annotations, print_function

from fetch import db, user_login


import unittest

class TestDB(unittest.TestCase):
    def setUp(self):
        self.engine = db.create_engine()
        return


    """
    Make sure we can actually connect to the POSTGRES db
    """
    def test_engine_connects(self):
        return


    """
    Test data integrity
    """
    def test_orm_data(self):
        return


    """
    Test db actually updates
    """
    def test_db_updates(self):
        return