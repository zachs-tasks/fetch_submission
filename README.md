

# To run:
    1. Working directory is Assignment
    2. docker compose up
    3. docker build --tag fetch:latest .
    4. docker run -it -d --network host --name fetch fetch:latest bash
    5. Doesn't work from docker compose, so you'll need to attach:
        - docker exec -it fetch bash
        - python ./fetch/fetch.py [-i NUMBER OF BATCHES TO PROCESS] [-n NUMBER OF MESSAGES PER BATCH]
            - both parameters optional



# Assumptions:
    1. User ids are unique.
    2. App versions have a mapping to an app version table. Assumes we don't have a crazy number of app versions.
        - I probably should have used a trie for the implementation.
    3. All user ips are IPV4. The masking function would need to change if IPV6 ips are included.
    4. All device ids are strings in the format ###-##-####.
        - Both 3. and 4. are based on what is visible in the returned message types.
    5. Assumes we don't want to add half-baked records. It's all the data or none of it. We could theoretically accept partial data...

# Production Deployment:
    1. Add way better data validations and handle errors appropriately.
    ~~2. Dockerize the app so it can be deployed anywhere~~
    3. I would use a strongly typed language (e.g. Rust, etc.)
    4. Improve logging. Useful for more than just investigating crashes. Can be used to replay what happened to the system and helps in disaster recovery.
    5. Production would need to automate service recovery. 
    6. Should probably use the actual Boto3 api. I just couldn't get the code / Windows environment variables to work with test credentials.

# Additional Components:
    1. More tests--especially for PII
    2. Actual trie interface to work with.
    3. Probably want a better configuration setup.

# Scale the Application:
    1. I would maybe deploy this to a Docker Swarm or use Kubernetes. You can make the service only visible to the other components it needs (or that need it). You can also automate service recovery with these tools.
    2. Shard the database.
    3. Normalize the database.
    4. Add lookup table for app versions.

# PII Recovery:
    1. IP: The way it's currently setup, you can trivially search the key,value pairs of the ip masking dictionary to recover the original value.
    2. Device ID: Random device id is stored in a trie which we can then search for when trying to recover the actual device id.
        - We could theoretically use a more cryptographically secure method? Hopefully these aren't social security numbers.


# If I had more time I would....:
    1. Ensure db credentials were stored and loaded in a secure manner
    ~~2. Since there's a lot of network i/o, I'd want to make this async.~~ Done
    3. Make sure things aren't so tightly coupled.
    4. Make this run forever. For now, it just runs the number of iterations we give it because of the graceful shutdown bug.
    5. Handle ipv6
    6. There should definitely be more tests to ensure we're handling everything appropriately.
    7. Optimize the db update frequency.
    8. The code needs more error handling. We'd need to make sure that the service doesn't just go down when it receives unexpected input.
    9. Sprinkle in easter egg comments for future explorers to find.
    10. Add masked data recovery methods.
    11. Could make this a library so other services could use it.