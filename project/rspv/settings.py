import os
import yaml
import logging
import logging.config

from pathlib import Path

# DEBUG Flag
DEBUG = bool(os.getenv("DEBUG", False))


# Paths Setup
SETTINGS_FILE_PATH = Path(__file__)
ROOT_DIR = SETTINGS_FILE_PATH.parent
LOGS_DIR = ROOT_DIR.parent

# Proxy Configuration
PROXY_SEVER_NAME = os.getenv("PROXY_SEVER_NAME")
PROXY_PORT = int(os.getenv("HTTP_PORT", 8000))
PROXY_HOST_NAME = os.getenv("HTTP_HOSTNAME")

# JWT Configuration
# User identifier in POST requests
JWT_USER_IDENTIFIER = os.getenv("JWT_USER_IDENTIFIER")

# JWT Hash method, chose from supported pyJWT documentation
JWT_HASH_METHOD = os.getenv("JWT_HASH_METHOD")

# JWT Secret
JWT_SECRET = os.getenv("JWT_SECRET")

# Should HTTP Requests be dropped if no user is specified in post requests?
DROP_JWT_ERROR = bool(os.getenv("DROP_JWT_ERROR", True))

# Database Configuration
DB_HOST_NAME = os.getenv("DB_HOST_NAME")
DB_DATABASE_NAME = os.getenv("DB_DATABASE_NAME")
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")



# Logging
logfile = "logger.yml"

with open(ROOT_DIR / logfile, "rt") as file:
    config = yaml.safe_load(file.read())
    logging.config.dictConfig(config)
