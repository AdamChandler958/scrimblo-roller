import os

def get_secret(secret_name):
    # Try to read the secret from the Docker secrets path
    try:
        with open(f'/run/secrets/{secret_name}', 'r') as secret_file:
            return secret_file.read().strip()
    except IOError:
        # Fallback to environment variable for local development
        return os.getenv(secret_name.upper())