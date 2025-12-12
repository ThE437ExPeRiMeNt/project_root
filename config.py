import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_ACCOUNT_CREATION_ENABLED = os.getenv("GOOGLE_ACCOUNT_CREATION_ENABLED", "False").lower() == "true"
GITHUB_REPO_URL = os.getenv("GITHUB_REPO_URL", "https://github.com/example/example-repo")
GITHUB_TOKEN = os.getenv("GITHUB_TOKEN")
CAPTCHA_SOLVER_API_KEY = os.getenv("CAPTCHA_SOLVER_API_KEY")
GOOGLE_CLOUD_PROJECT_ID = os.getenv("GOOGLE_CLOUD_PROJECT_ID")
PROXY_API_URL = os.getenv("PROXY_API_URL")

if not GITHUB_TOKEN:
    raise ValueError("GITHUB_TOKEN environment variable not set.")

if not CAPTCHA_SOLVER_API_KEY:
    raise ValueError("CAPTCHA_SOLVER_API_KEY environment variable not set.")

if not GOOGLE_CLOUD_PROJECT_ID:
     raise ValueError("GOOGLE_CLOUD_PROJECT_ID environment variable not set.")

if not PROXY_API_URL:
     raise ValueError("PROXY_API_URL environment variable not set.")
