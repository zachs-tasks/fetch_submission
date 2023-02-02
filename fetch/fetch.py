from __future__ import annotations, print_function
from argparse import ArgumentParser
from typing import Dict, Optional

import asyncio
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

def get_next_message() -> Optional[Dict[str]]:
    process_state = subprocess.run("awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue", shell=True, capture_output=True)
    if process_state.returncode != 0:
        logger.error(f"Process did not complete succesfully: {process_state}")
        return None
    return json.loads(process_state.stdout.decode("utf-8"))

def get_argparser() -> ArgumentParser:
    parser = ArgumentParser(description="Log user logins")
    parser.add_argument("-n", "--number-msgs", help="Number of messages to process", type=int, default=10)
    return parser


# create a basic asyncio subprocess shell
# credit to asyncio library docs
async def run(cmd: str) -> Optional[str]:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE
    )

    stdout, stderr = await proc.communicate()

    if stdout:
        return json.loads(stdout.decode("utf-8"))

    return None

async def main():
    args = get_argparser().parse_args()

    # This shouldn't be hardcoded. We should be able to pass in a queue-url that we validate
    AWS_CMD = "awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue"

    sesh_manager = db.ServiceSessionManager()

    # run forever... like a microservice :)
    # need to add a graceful shutdown method
    while True:
        tasks = [run(AWS_CMD) for _ in range(args.number_msgs)]

        MESSAGES = await asyncio.gather(*tasks)

        for returned_message in filter(None, MESSAGES):
            users = [user_login.fetch_next_user(msg["Body"]) for msg in returned_message["Messages"]]
            logger.info(users)
            sesh_manager.save_users(filter(None, users))


        # we could run this full blast, but let's be green about this
        await asyncio.sleep(0.5)
    return

if __name__ == "__main__":
    asyncio.run(main())