import os
import config
import google_utils
import github_utils
import logger
from proxy_manager import ProxyManager
from captcha_solver import CaptchaSolver
from dotenv import load_dotenv

load_dotenv()

logger = logger.getLogger(__name__)

def main():
    print("Welcome to the automated account creation and repository starring script!")

    # Initialize Proxy Manager and Captcha Solver
    proxy_manager = ProxyManager(config.PROXY_API_URL)
    captcha_solver = CaptchaSolver(config.CAPTCHA_SOLVER_API_KEY)

    use_existing_google = input("Do you want to use existing Google accounts? (yes/no): ").lower() == "yes"

    if use_existing_google:
        google_email, google_password = google_utils.get_google_account_credentials()
    else:
        # Attempt to create a Google account
        if config.GOOGLE_ACCOUNT_CREATION_ENABLED:
            print("Attempting to create a Google account...")
            google_credentials = google_utils.create_google_account(proxy_manager, captcha_solver)
            if google_credentials:
                google_email, google_password = google_credentials
                print(f"Google account created successfully: {google_email}")
            else:
                print("Failed to create Google account. Please provide existing credentials.")
                google_email, google_password = google_utils.get_google_account_credentials()
        else:
            print("Google account creation is disabled in config.py. Please enable it or use existing accounts.")
            google_email, google_password = google_utils.get_google_account_credentials()

    # Create a GitHub account (or attempt to)
    print("Creating a GitHub account...")
    github_credentials = github_utils.create_github_account(google_email, google_password, proxy_manager, captcha_solver)

    if github_credentials:
        github_username, github_password = github_credentials
        print(f"GitHub account created successfully: {github_username}")
    else:
        print("Failed to create GitHub account. Please provide existing credentials.")
        github_username = input("Enter your GitHub username: ")
        github_password = input("Enter your GitHub password: ")

    # Star the repository
    print(f"Starring the repository: {config.GITHUB_REPO_URL}")
    github_utils.star_github_repo(github_username, github_password, config.GITHUB_REPO_URL)

if __name__ == "__main__":
    main()
