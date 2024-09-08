from os.path import exists, isabs, join
from time import sleep
from json import load

class CookiesManager:
	'''CookiesManager: 
	A class to handle loading cookies into a Selenium WebDriver instance.'''
	def __init__(self, base_dir=None, verbose=False):
		'''Initializes the CookiesManager object with the specified parameters.
		Args:
			base_dir (str): The base directory where cookie files are stored. If None, expects absolute paths.
			verbose (bool): If True, print logs to the console.'''
		self.base_dir = base_dir
		self.verbose = verbose
		if self.base_dir and not isabs(self.base_dir):
			raise ValueError('base_dir must be an absolute path.')
		
	def log(self, message):
		'''Logs a message to the console if verbose mode is enabled.
		Args:
			message (str): The message to log.'''
		if self.verbose:
			print(message)

	def load_cookies(self, driver, cookie_file, initial_url):
		'''Loads cookies from a specified JSON file into the Selenium WebDriver.
		Args:
			driver (WebDriver): The Selenium WebDriver instance where cookies will be loaded.
			cookie_file (str): The path to the JSON file containing the cookies.
			initial_url (str): The initial URL to ensure the correct domain for cookie loading.
		Raises:
			Exception: If there is an error adding any of the cookies to the WebDriver.'''
		file_path = cookie_file if isabs(cookie_file) else join(self.base_dir, cookie_file)
		if not isabs(file_path):
			raise ValueError('cookie_file path must be absolute.')
		driver.get(initial_url)
		self.log('[~] Trying to load cookies...')
		sleep(5)
		if exists(file_path):
			try:
				with open(file_path, 'r') as file:
					cookies = load(file)
					for cookie in cookies:
						if 'sameSite' in cookie:
							if cookie['sameSite'] not in ['Strict', 'Lax', 'None']:
								del cookie['sameSite']
						try:
							driver.add_cookie(cookie)
						except Exception as e:
							pass
				self.log(f'[+] Cookies loaded from {file_path}')
				driver.refresh()  # Refresh to apply cookies
				sleep(5)
			except Exception as e:
				pass
		else:
			self.log(f'[-] Cookie file {file_path} not found.')
# by azuk4r