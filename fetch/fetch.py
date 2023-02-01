from __future__ import annotations, print_function

import db
import json
import user_login

import logging
"""
Since we're running it ~locally~, I'm just using the subprocess api
Theoretically we should be able to use boto3 (if given credentials) or use the requests module.

Note: I would like to do this async for production
"""
import subprocess

# global variable not ideal. Using just to log output for this...
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def get_next_message():
    process_state = subprocess.run("awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue", shell=True, capture_output=True)
    if process_state.returncode != 0:
        logger.error(f"Process did not complete succesfully: {process_state}")
    return json.loads(process_state.stdout.decode("utf-8"))


def run():
    sesh_manager = db.ServiceSessionManager()
    # run forever... like a microservice :)
    data = get_next_message()
    print(data)
    for msg in data["Messages"]:
        user = user_login.fetch_next_user(msg["Body"])
        logger.info(user)
        sesh_manager.save_users([user])
    return

if __name__ == "__main__":
    run()