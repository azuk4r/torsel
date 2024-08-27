import os
import json

class CookiesManager:
    """
    CookiesManager: A class to handle loading cookies into a Selenium WebDriver instance.

    This class manages cookies stored in JSON files, allowing them to be loaded
    into a Selenium WebDriver session to maintain session state across different browser instances.
    """

    def __init__(self, base_dir='/tmp/torsel_cookies', verbose=False):
        """
        Initializes the CookiesManager object with the specified parameters.

        Args:
            base_dir (str): The base directory where cookie files are stored.
            verbose (bool): If True, print logs to the console.
        """
        self.base_dir = base_dir
        self.verbose = verbose
        if not os.path.exists(self.base_dir):
            os.makedirs(self.base_dir)

    def log(self, message):
        """
        Logs a message to the console if verbose mode is enabled.

        Args:
            message (str): The message to log.
        """
        if self.verbose:
            print(message)

    def load_cookies(self, driver, cookie_file, initial_url):
        """
        Loads cookies from a specified JSON file into the Selenium WebDriver.

        This method navigates to the initial URL to ensure the domain matches, then loads the cookies from the JSON file.
        If the cookie file exists, the cookies are added to the WebDriver session.

        Args:
            driver (WebDriver): The Selenium WebDriver instance where cookies will be loaded.
            cookie_file (str): The name of the JSON file containing the cookies.
            initial_url (str): The initial URL to ensure the correct domain for cookie loading.

        Raises:
            Exception: If there is an error adding any of the cookies to the WebDriver.
        """
        driver.get(initial_url)  # Ensure the domain matches the cookies
        file_path = os.path.join(self.base_dir, cookie_file)
        if os.path.exists(file_path):
            with open(file_path, 'r') as f:
                cookies = json.load(f)
                for cookie in cookies:
                    # Adjust the 'sameSite' attribute if necessary
                    if 'sameSite' in cookie:
                        if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                            del cookie['sameSite']
                    try:
                        driver.add_cookie(cookie)
                    except Exception as e:
                        self.log(f"[-] Failed to add cookie: {e}")
            self.log(f"[+] Cookies loaded from {cookie_file}")
        else:
            self.log(f"[-] Cookie file {cookie_file} not found.")
