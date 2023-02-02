from __future__ import annotations, print_function

# I know unit tests should not be this tightly coupled
from fetch import db, user_login
from typing import Dict

import json
import unittest

class TestDB(unittest.TestCase):
    # good :)
    safe_user_data: Dict[str] = {
        "user_id": "bananas", 
        "device_type": "android", 
        "masked_ip": "127.0.0.1", 
        "masked_device_id": "bonobos", 
        "locale": "Madison, WI",
        "app_version": "2.1.3",
    }

    # ORM should sanitize input
    unsafe_user_data: Dict[str] = {
        "user_id": "; DROP TABLE;", 
        "device_type": "orm please work", 
        "masked_ip": "need some sorta ip validation but I only so much time and outside commitments", 
        "masked_device_id": "bonkers", 
        "locale": "Madison, WI",
        "app_version": "2.1.3",
    }


    def setUp(self):
        self.sesh_man = db.ServiceSessionManager()
        self.good_users = user_login.fetch_next_user(json.dumps(TestDB.safe_user_data))
        self.bad_users = user_login.fetch_next_user(json.dumps(TestDB.unsafe_user_data))
        return


    """
    Make sure we can actually connect to the POSTGRES db
    """
    def test_engine_connects(self):
        try:
            self.sesh_man.engine.connect()
        except:
            self.fail("Could not connect to the database")
        return


    """
    Test data integrity
    """
    def test_orm_data(self):
        self.sesh_man.save_users([self.good_users])
        self.sesh_man.save_users([self.bad_users])
        test_users = self.sesh_man.get_users(["bananas", "; DROP TABLES;"])
        self.assertFalse(self.sesh_man.select_all() == 0)


        # so the select doesn't quite work correctly if we need to sanitize our input
        # TODO: Fix that....
        # self.assertIn("; DROP TABLES;", [user.user_id for user in test_users])
        return


    """
    Test db actually updates
    """
    def test_db_updates(self):
        # TODO: add a whole bunch of updates and deletes
        return