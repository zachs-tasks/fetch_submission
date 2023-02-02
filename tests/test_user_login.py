from __future__ import annotations, print_function

from typing import Dict

import json
import unittest

from fetch import user_login

class TestUserLogin(unittest.TestCase):

    user_data_dict: Dict = {
        "user_id": "bananas", 
        "device_type": "android", 
        "masked_ip": "127.0.0.1", 
        "masked_device_id": "bonobos", 
        "locale": "Madison, WI",
        "app_version": "2.1.3",
    }

    bad_user_data_dict: Dict = {
        "Bob": "Loblaw",
        "Miguel": "Angel Felix Gallardo",
        "Arrested": "Development",
        "Task": "Master", # silly British TV
        "Cunk": "On Earth", # silly British TV
        "foo": "barred", 
    }

    def setUp(self):
        self.user_data_str: str = json.dumps(TestUserLogin.user_data_dict)
        self.bad_user_data: str = json.dumps(TestUserLogin.bad_user_data_dict)
        return
    
    def test_create_user(self):
        user = user_login.fetch_next_user(self.user_data_str)
        self.assertIsNotNone(user)
        self.assertEqual(user.user_id, TestUserLogin.user_data_dict["user_id"])
        self.assertEqual(user.device_type, TestUserLogin.user_data_dict["device_type"])
        self.assertEqual(user.masked_ip, TestUserLogin.user_data_dict["masked_ip"])
        self.assertEqual(user.masked_device_id, TestUserLogin.user_data_dict["masked_device_id"])
        self.assertEqual(user.locale, TestUserLogin.user_data_dict["locale"])
        self.assertEqual(user.app_version, TestUserLogin.user_data_dict["app_version"].split(".")[0])
        return

    def test_user_creation_fails(self):
        user = user_login.fetch_next_user(self.bad_user_data)
        self.assertEqual(user, None)
        return


if __name__ == "__main__":
    unittest.main()