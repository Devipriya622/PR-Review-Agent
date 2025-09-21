# src/config.py
import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    GITHUB_TOKEN = os.getenv("GITHUB_TOKEN", "")
    GITLAB_TOKEN = os.getenv("GITLAB_TOKEN", "")
    BITBUCKET_USERNAME = os.getenv("BITBUCKET_USERNAME", "")
    BITBUCKET_APP_PASSWORD = os.getenv("BITBUCKET_APP_PASSWORD", "")
    REQUEST_TIMEOUT = int(os.getenv("REQUEST_TIMEOUT", "10"))
    MAX_FILE_SIZE_BYTES = int(os.getenv("MAX_FILE_SIZE_BYTES", str(2 * 1024 * 1024)))
