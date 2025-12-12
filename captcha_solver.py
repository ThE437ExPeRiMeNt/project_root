import requests
import logging
import config
import time

logger = logging.getLogger(__name__)

class CaptchaSolver:
    def __init__(self, api_key):
        self.api_key = api_key
        self.api_url = "http://2captcha.com/in.php"  # Example: 2Captcha API
        self.result_url = "http://2captcha.com/res.php"

    def solve_captcha(self, site_key, page_url):
        """Solves a CAPTCHA using the 2Captcha API."""
        try:
            # Step 1: Submit the CAPTCHA to the solving service
            params = {
                "key": self.api_key,
                "method": "userrecaptcha",
                "googlekey": site_key,
                "pageurl": page_url,
                "json": 1  # Request JSON response
            }
            response = requests.get(self.api_url, params=params, timeout=30)
            response.raise_for_status()
            data = response.json()

            if data["status"] == 1:
                captcha_id = data["request"]
                logger.info(f"Captcha submitted, ID: {captcha_id}")

                # Step 2: Poll for the result
                for i in range(60):  # Try for up to 5 minutes (60 * 5 seconds)
                    result_params = {
                        "key": self.api_key,
                        "action": "get",
                        "id": captcha_id,
                        "json": 1
                    }
                    result_response = requests.get(self.result_url, params=result_params, timeout=5)
                    result_response.raise_for_status()
                    result_data = result_response.json()

                    if result_data["status"] == 1:
                        captcha_solution = result_data["request"]
                        logger.info("Captcha solved successfully.")
                        return captcha_solution
                    elif result_data["request"] == "CAPCHA_NOT_READY":
                        logger.info("Captcha not ready, waiting...")
                        time.sleep(5)
                    else:
                        logger.error(f"Captcha solving failed: {result_data}")
                        return None

                logger.error("Captcha solving timed out.")
                return None
            else:
                logger.error(f"Captcha submission failed: {data}")
                return None

        except requests.exceptions.RequestException as e:
            logger.error(f"Error during CAPTCHA solving: {e}")
            return None
        except Exception as e:
            logger.exception("An unexpected error occurred during CAPTCHA solving.")
            return None
