# Automated Account Creation and Repository Starring Script

**Warning:** This script is for educational purposes only. Automating account creation and manipulating repository statistics is unethical and violates the terms of service of Google and GitHub. Use at your own risk.

## Prerequisites

*   Python 3.6+
*   pip
*   A Google Cloud Project with the reCAPTCHA Enterprise API enabled (for CAPTCHA solving)
*   A GitHub Personal Access Token with `public_repo` scope

## Installation

1.  Clone the repository:
    ```bash
    git clone <repository_url>
    cd project_root
    ```
2.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```
3.  Configure the `.env` file (see Configuration below).

## Configuration

Create a `.env` file in the project root directory with the following variables:
```
GOOGLE_ACCOUNT_CREATION_ENABLED=False

GITHUB_REPO_URL=https://github.com/owner/repo

GITHUB_TOKEN=<your_github_token>

CAPTCHA_SOLVER_API_KEY=<your_captcha_solver_api_key>  # e.g., 2Captcha API key

GOOGLE_CLOUD_PROJECT_ID=<your_google_cloud_project_id>

PROXY_API_URL=<your_proxy_api_url> #URL Endpoint to obtain Proxy
```

## Usage

Run the script:

```bash
python main.py
