import os
import time
import logging
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException, WebDriverException
from fake_useragent import UserAgent
from undetected_chromedriver import Chrome, ChromeOptions
import config
from captcha_solver import CaptchaSolver
from proxy_manager import ProxyManager

logger = logging.getLogger(__name__)

def create_undetected_chrome_driver(proxy=None):
    """Creates an undetected ChromeDriver instance."""
    chrome_options = ChromeOptions()
    ua = UserAgent()
    user_agent = ua.random
    chrome_options.add_argument(f"user-agent={user_agent}")
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    chrome_options.add_argument("--disable-gpu")
    chrome_options.add_argument("--no-sandbox")
    chrome_options.add_argument("--disable-dev-shm-usage")

    if proxy:
        chrome_options.add_argument(f"--proxy-server={proxy['http']}")

    try:
        driver = Chrome(options=chrome_options)
        return driver
    except Exception as e:
        logger.exception(f"Failed to create undetected ChromeDriver: {e}")
        return None


def create_google_account(proxy_manager, captcha_solver):
    """Automates Google account creation with proxy and CAPTCHA solving."""

    driver = None
    try:
        proxy = proxy_manager.rotate_proxy()
        if not proxy:
            logger.error("No proxy available, cannot create Google account.")
            return None

        driver = create_undetected_chrome_driver(proxy)
        if not driver:
            logger.error("Failed to create undetected ChromeDriver.")
            return None

        driver.get("https://accounts.google.com/signup")

        # 1. Fill out the form
        driver.find_element(By.ID, "firstName").send_keys("John")  # Replace with realistic name generation
        driver.find_element(By.ID, "lastName").send_keys("Doe") # Replace with realistic name generation
        username = f"testuser{int(time.time())}" # Replace with unique username generation
        driver.find_element(By.ID, "username").send_keys(username)
        driver.find_element(By.NAME, "Passwd").send_keys("P@$$wOrd") # Replace with strong password generation
        driver.find_element(By.NAME, "ConfirmPasswd").send_keys("P@$$wOrd")

        driver.find_element(By.XPATH, "//span[text()='Next']").click()
        time.sleep(5)  # Wait for page to load

         # 2. Handle CAPTCHA
        try:
            captcha_iframe = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.XPATH, "//iframe[@title='reCAPTCHA']"))
            )
            driver.switch_to.frame(captcha_iframe)
            site_key = driver.find_element(By.ID, "recaptcha-anchor").get_attribute("data-sitekey")
            driver.switch_to.default_content()

            captcha_solution = captcha_solver.solve_captcha(site_key, driver.current_url)

            if captcha_solution:
                # Inject CAPTCHA solution into the page
                driver.execute_script(f"""
                    document.querySelector('#g-recaptcha-response').value = '{captcha_solution}';
                """)
                time.sleep(1)
                driver.find_element(By.XPATH, "//span[text()='Next']").click()
                time.sleep(10)

            else:
                logger.error("Failed to solve CAPTCHA.")
                return None

        except (TimeoutException, NoSuchElementException) as e:
            logger.info("No CAPTCHA found.")
            # Continue if no CAPTCHA is present

        #3. Post Captcha Pages
        try:
            driver.find_element(By.XPATH, "//span[text()='Next']").click()
            time.sleep(5)  # Wait for page to load
        except (TimeoutException, NoSuchElementException) as e:
            logger.info("No Post Captcha Page found.")

        #4. Phone Verification Page
        try:
            # Phone number input element
            phone_number_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'phoneNumberId'))
            )
            phone_number_input.send_keys('5555555555')
            driver.find_element(By.XPATH, "//span[text()='Verify']").click()
            time.sleep(5)

            # Enter the verification code
            verification_code = input("Enter the verification code sent to your phone: ")
            verification_code_input = WebDriverWait(driver, 10).until(
                EC.presence_of_element_located((By.ID, 'verificationCodeId'))
            )
            verification_code_input.send_keys(verification_code)
            driver.find_element(By.XPATH, "//span[text()='Verify']").click()
            time.sleep(5)  # Wait for page to load

        except (TimeoutException, NoSuchElementException) as e:
            logger.info("No Phone Verification Page found.")

        # Handle any further steps, like phone verification (which is almost always required)
        # This part is highly variable and depends on Google's requirements.
        # You would need extensive error handling and retry logic to make this even remotely reliable

        print("Google account creation attempted.  Check the browser for status.")
        return username, "P@$$wOrd"

    except WebDriverException as e:
        logger.exception(f"WebDriverException during Google account creation: {e}")
        return None
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {e}")
        return None
    finally:
        if driver:
            driver.quit()

def get_google_account_credentials():
  """Prompts the user for their Google account email and password."""
  email = input("Enter your Google email address: ")
  password = input("Enter your Google password: ")
  return email, password
