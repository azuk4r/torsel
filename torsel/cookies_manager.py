import os
import json
import shutil

class CookiesManager:
    """
    CookiesManager: A class to manage cookies for Selenium sessions.

    This class provides functionality to clean up old cookies, save new cookies generated
    during a browsing session, and manage the loading of custom cookies if provided.
    """

    def __init__(self, base_dir='/tmp/torsel_cookies', verbose=False):
        """
        Initializes the CookiesManager with the given parameters.

        Args:
            base_dir (str): Directory where cookies will be stored.
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

    def clean_cookies(self):
        """
        Cleans up old cookies by deleting the cookie storage directory and recreating it.
        This ensures that no stale cookies remain from previous sessions.
        """
        self.log("[~] Cleaning old cookies...")
        if os.path.exists(self.base_dir):
            shutil.rmtree(self.base_dir)
        os.makedirs(self.base_dir)
        self.log("[+] Cookie cleanup done.")

    def save_cookies(self, driver, instance_num, url):
        """
        Saves the cookies from the current Selenium session to a JSON file.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            instance_num (int): The index of the Tor instance being used.
            url (str): The URL for which cookies are being saved.

        The cookies are saved in a file named based on the instance number and the URL.
        """
        cookies = driver.get_cookies()
        file_name = f'instance_{instance_num}_cookies_{url.replace("https://", "").replace(".", "_")}.json'
        file_path = os.path.join(self.base_dir, file_name)
        with open(file_path, 'w') as f:
            json.dump(cookies, f)
        self.log(f"[+] Cookies saved for instance {instance_num} ({url})")

    def manage_cookies(self, driver, instance_num, url, custom_cookies=None):
        """
        Manages the loading and saving of cookies for a specific URL.

        Args:
            driver (WebDriver): The Selenium WebDriver instance.
            instance_num (int): The index of the Tor instance being used.
            url (str): The URL for which cookies are being managed.
            custom_cookies (list, optional): A list of custom cookies to load before browsing.

        If custom cookies are provided, they are loaded into the browser session.
        Otherwise, the browser navigates to the URL, and the cookies generated during
        the session are saved.
        """
        if custom_cookies:
            for cookie in custom_cookies:
                driver.add_cookie(cookie)
            self.log(f"[+] Custom cookies loaded for instance {instance_num} ({url})")
        driver.get(url)
        self.save_cookies(driver, instance_num, url)
