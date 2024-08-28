import os
import json
import time

class CookiesManager:
    """
    CookiesManager: A class to handle loading cookies into a Selenium WebDriver instance.
    """

    def __init__(self, base_dir=None, verbose=False):
        """
        Initializes the CookiesManager object with the specified parameters.

        Args:
            base_dir (str): The base directory where cookie files are stored. If None, expects absolute paths.
            verbose (bool): If True, print logs to the console.
        """
        self.base_dir = base_dir
        self.verbose = verbose
        if self.base_dir and not os.path.isabs(self.base_dir):
            raise ValueError("base_dir must be an absolute path.")
        if self.base_dir and not os.path.exists(self.base_dir):
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

        Args:
            driver (WebDriver): The Selenium WebDriver instance where cookies will be loaded.
            cookie_file (str): The name of the JSON file containing the cookies.
            initial_url (str): The initial URL to ensure the correct domain for cookie loading.

        Raises:
            Exception: If there is an error adding any of the cookies to the WebDriver.
        """
        # Calculate the full path to the cookie file
        if self.base_dir:
            file_path = os.path.join(self.base_dir, cookie_file)
        else:
            file_path = cookie_file  # Expecting an absolute path

        if not os.path.isabs(file_path):
            raise ValueError("cookie_file path must be absolute.")

        driver.get(initial_url)
        self.log('[~] Trying to load cookies...')
        time.sleep(5)

        if os.path.exists(file_path):
            try:
                with open(file_path, 'r') as file:
                    cookies = json.load(file)
                    for cookie in cookies:
                        if 'sameSite' in cookie:
                            if cookie['sameSite'] not in ["Strict", "Lax", "None"]:
                                del cookie['sameSite']
                        try:
                            driver.add_cookie(cookie)
                        except Exception as e:
                            pass  # Silently handle the error without logging it
                self.log(f"[+] Cookies loaded from {cookie_file}")
                driver.refresh()  # Refresh to apply cookies
                time.sleep(5)
            except Exception as e:
                self.log(f"[-] Error loading cookies from {file_path}: {e}")
        else:
            self.log(f"[-] Cookie file {cookie_file} not found.")

