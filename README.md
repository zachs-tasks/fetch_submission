

# Assumptions:
    1. User ids are unique.
    2. App versions have a mapping to an app version table.
    3. DB is normalized to some degree...
    4. 

# Production Deployment:
    1. Add way better data validations and handle errors appropriately
    2. Dockerize the app so it can be deployed anywhere
    3. I would use a strongly typed language (e.g. Rust, etc.)

# Additional Components:


# Scale the Application:
    1. I would maybe deploy this to a Docker Swarm or use Kubernetes.
    2. I would want to optimize the db update frequency. 
    3. 

# PII Recovery:


# If I had more time I would....:
    1. Ensure db credentials were stored and loaded in a secure manner
    2. Since there's a lot of network i/o, I'd want to make this async
    3. Make sure things aren't so tightly coupled