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

