import requests
import logging
import config

logger = logging.getLogger(__name__)

class ProxyManager:
    def __init__(self, api_url):
        self.api_url = api_url
        self.current_proxy = None

    def get_proxy(self):
        """Gets a new proxy from the API."""
        try:
            response = requests.get(self.api_url, timeout=5)
            response.raise_for_status()  # Raise HTTPError for bad responses (4xx or 5xx)
            data = response.json()
            if "proxy" in data:
                self.current_proxy = {"http": data["proxy"], "https": data["proxy"]}
                logger.info(f"Retrieved new proxy: {self.current_proxy}")
                return self.current_proxy
            else:
                logger.error(f"Invalid response from proxy API: {data}")
                return None
        except requests.exceptions.RequestException as e:
            logger.error(f"Error fetching proxy from API: {e}")
            return None

    def rotate_proxy(self):
        """Rotates to a new proxy."""
        logger.info("Rotating proxy...")
        self.current_proxy = self.get_proxy()
        return self.current_proxy

    def get_current_proxy(self):
        """Returns the current proxy."""
        return self.current_proxy
