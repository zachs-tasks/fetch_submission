from __future__ import annotations, print_function
from argparse import ArgumentParser
from typing import Optional

import asyncio
import db
import json
import user_login

import logging

# global variable not ideal. Using just to log output for this...
logger = logging.getLogger(__name__)
handler = logging.StreamHandler()
formatter = logging.Formatter("%(asctime)s %(name)-12s %(levelname)-8s %(message)s")
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

def get_argparser() -> ArgumentParser:
    parser = ArgumentParser(description="Log user logins")
    parser.add_argument("-n", "--number-msgs", help="Number of messages to process", type=int, default=10)

    parser.add_argument("-i", "--iterations", 
                help="Number of times to aws batches to process. Used for test code graceful shutdown bug.",
                type = int,
                default = 3
    )
    return parser


# create a basic asyncio subprocess shell
# credit to asyncio library docs
async def run(cmd: str) -> Optional[str]:
    proc = await asyncio.create_subprocess_shell(
        cmd,
        stdout=asyncio.subprocess.PIPE,
        stderr = asyncio.subprocess.PIPE
    )

    stdout, _ = await proc.communicate()

    if stdout:
        return json.loads(stdout.decode("utf-8"))

    return None

async def main():
    args = get_argparser().parse_args()

    # This shouldn't be hardcoded. We should be able to pass in a queue-url that we validate
    AWS_CMD = "awslocal sqs receive-message --queue-url http://localhost:4566/000000000000/login-queue"
    sesh_manager = db.ServiceSessionManager("postgresql+psycopg2://postgres:postgres@localhost:5432/")

    # micro-microservice?
    # need to add a graceful shutdown method
    for _ in range(args.iterations):
        tasks = [run(AWS_CMD) for _ in range(args.number_msgs)]

        MESSAGES = await asyncio.gather(*tasks)

        for returned_message in filter(None, MESSAGES):
            users = [user_login.fetch_next_user(msg["Body"]) for msg in returned_message["Messages"]]

            # should only log errors for "None" users, but alas
            logger.info(users)

            sesh_manager.save_users(filter(None, users))


        # we could run this full blast, but let's be green
        await asyncio.sleep(0.5)
    return

if __name__ == "__main__":
    try:
        asyncio.run(main())
    except:
        """
        I'VE BEEN STARING AT THIS FOREVER.

        Apparently there was a bug with handling shutdown procedures in asyncio. I'm seeing this behavior: https://github.com/python/cpython/issues/96827

        The general thought:
            1. gather all pending tasks
            2. send pending users to the sql db
            3. end
        """
        print("Shutdown...")