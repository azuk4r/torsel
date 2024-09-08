from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from os.path import join, abspath, exists, isabs
from socket import socket, AF_INET, SOCK_STREAM
from selenium.webdriver.common.by import By
from .cookies_manager import CookiesManager
from subprocess import Popen, DEVNULL
from selenium.webdriver import Chrome
from stem.control import Controller
from threading import Thread
from shutil import rmtree
from random import choice
from os import makedirs
from queue import Queue
from stem import Signal
from time import sleep
from psutil import (
	process_iter, 
    NoSuchProcess, 
    TimeoutExpired, 
    AccessDenied, 
    net_connections, 
    Process
)

class Torsel:
	'''Torsel:
	A Python module for managing Tor instances with Selenium.
	This class provides functionality to create, manage, and rotate multiple Tor instances,
	as well as configure Selenium WebDriver to use these instances for web automation.'''
	def __init__(self, 
			  total_instances=1, 
			  max_threads=1, 
			  tor_base_port=9050, 
			  tor_control_base_port=9151, 
			  tor_path=None, 
			  tor_data_dir=None, 
			  user_agent=None,
			  headless=False, 
			  verbose=False, 
			  cookies_dir=None, 
			  cookies_mapping=None
			  ): # sad feelings
		'''Initializes the Torsel object with the given parameters.
		Args:
			total_instances (int): Number of Tor instances to create.
			max_threads (int): Maximum number of concurrent threads.
			tor_base_port (int): Base port number for Tor SOCKS connections.
			tor_control_base_port (int): Base port number for Tor control connections.
			tor_path (str): Path to the Tor executable.
			tor_data_dir (str): Directory to store Tor profiles.
			user_agent (str): Specifies the user_agent, if None a random one is selected.
			headless (bool): Run Selenium in headless mode if True.
			verbose (bool): If True, print logs to the console.
			cookies_dir (str): Directory to store and load cookies.
			cookies_mapping (dict): Mapping of domains to specific cookie files based on instance number.'''
		self.total_instances = total_instances
		self.max_threads = max_threads
		self.tor_base_port = self.find_available_port(tor_base_port)
		self.tor_control_base_port = self.find_available_port(tor_control_base_port)
		self.tor_path = abspath(tor_path)
		self.tor_data_dir = abspath(tor_data_dir)
		self.user_agent = user_agent
		self.headless = headless
		self.verbose = verbose
		self.cookies_dir = abspath(cookies_dir) if cookies_dir else None
		self.cookies_mapping = cookies_mapping
		self.tor_processes = {}
		# Initialize the CookiesManager if either cookies_dir or cookies_mapping is provided
		if cookies_dir or cookies_mapping:
			self.cookies_manager = CookiesManager(base_dir=cookies_dir, verbose=verbose)
		else:
			self.cookies_manager = None

	def log(self, message):
		'''Logs a message to the console if verbose mode is enabled.
		Args:
			message (str): The message to log.'''
		if self.verbose:
			print(message)

	def find_available_port(self, start_port):
		'''Finds the next available port, starting from the given start_port.
		Args:
			start_port (int): The port number to start the search from.	
		Returns:
			int: The next available port number.'''
		while True:
			if not self.is_port_open(start_port):
				return start_port
			start_port += 1

	def clean_up(self):
		'''Cleans up any previous Tor processes, files, and ports.
		Kills any running Tor processes, frees up occupied ports, and removes old Tor profile directories.'''
		self.log('[~] Cleaning up previous processes, files, and ports...')
		for proc in process_iter(['name']):
			try:
				if proc.name() == 'tor':
					proc.terminate()
					proc.wait(timeout=5)
			except NoSuchProcess:
				pass
			except TimeoutExpired:
				proc.kill()
		sleep(1)
		for port in range(self.tor_base_port, self.tor_base_port + self.total_instances * 10, 10):
			try:
				self.close_port(port)
				self.close_port(port + 101)
			except Exception as e:
				self.log(f'[-] Error closing port {port}: {str(e)}')
		if exists(self.tor_data_dir):
			rmtree(self.tor_data_dir, ignore_errors=True)
		self.log('[+] Cleanup completed.')
		sleep(3)

	def close_port(self, port):
		'''Closes the specified port by terminating the associated process.
		Args:
			port (int): The port number to close.'''
		for conn in net_connections():
			if conn.laddr.port == port:
				try:
					process = Process(conn.pid)
					process.terminate()
					process.wait(timeout=5)
				except NoSuchProcess:
					pass
				except AccessDenied:
					self.log(f'[-] Access denied when trying to close port {port}')
				except TimeoutExpired:
					process.kill()

	def create_tor_instance(self, instance_num):
		'''Creates and configures a Tor instance with the specified instance number.
		Args:
			instance_num (int): The index of the Tor instance.'''
		self.log(f'[~] Creating Tor instance {instance_num}...')
		instance_dir = join(self.tor_data_dir, f'tor{instance_num}')
		makedirs(instance_dir, exist_ok=True)
		torrc_content = f'''SocksPort {self.tor_base_port + instance_num * 10}
		ControlPort {self.tor_control_base_port + instance_num * 10}
		DataDirectory {instance_dir}'''
		torrc_path = join(instance_dir, 'torrc')
		with open(torrc_path, 'w') as torrc_file:
			torrc_file.write(torrc_content)
		tor_process = Popen([self.tor_path, '-f', torrc_path], stdout=DEVNULL, stderr=DEVNULL)
		self.tor_processes[instance_num] = tor_process
		sleep(10)
		self.log(f'[+] Tor instance {instance_num} created and running.')
		self.rotate_tor_ip(instance_num)

	def configure_selenium_with_tor(self, instance_num):
		'''Configures Selenium WebDriver to use a Tor instance as a proxy.
		Args:
			instance_num (int): The index of the Tor instance.	
		Returns:
			WebDriver, WebDriverWait, By, EC: Configured Selenium WebDriver instance and related utilities.'''
		if not self.user_agent:
			user_agents = [
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/114.0.5735.199 Safari/537.36',
                'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:102.0) Gecko/20100101 Firefox/102.0',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/15.1 Safari/605.1.15',
                'Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:89.0) Gecko/20100101 Firefox/89.0',
                'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36',
                'Mozilla/5.0 (Macintosh; Intel Mac OS X 11_2_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36']
			user_agent = choice(user_agents)
			chrome_options = Options()
			chrome_options.add_argument(f'--user-agent={user_agent}')
		else:
			chrome_options = Options()
			chrome_options.add_argument(f'--user-agent={self.user_agent}')
		if self.headless:
			chrome_options.add_argument('--headless')
		chrome_options.add_argument(f'--proxy-server=socks5://127.0.0.1:{self.tor_base_port + instance_num * 10}')
		chrome_options.add_argument('--no-sandbox')
		chrome_options.add_experimental_option('excludeSwitches', ['enable-logging'])
		service = Service(log_path=DEVNULL)
		driver = Chrome(service=service, options=chrome_options)
		wait = WebDriverWait(driver, 10)
		return driver, wait, By, EC

	def rotate_tor_ip(self, instance_num):
		'''Rotates the IP address of a Tor instance by sending the NEWNYM signal.
		Args:
			instance_num (int): The index of the Tor instance.
		Returns:
			bool: True if the IP was successfully rotated, False otherwise.'''
		control_port = self.tor_control_base_port + instance_num * 10
		if self.is_port_open(control_port):
			try:
				with Controller.from_port(port=control_port) as controller:
					controller.authenticate()
					controller.signal(Signal.NEWNYM)
				sleep(10)
				self.log(f'[+] IP rotated for Tor instance {instance_num}.')
				return True
			except Exception as e:
				self.log(f'[-] Failed to rotate IP for instance {instance_num}: {e}')
				return False
		else:
			self.log(f'[-] Control port {control_port} not accessible for instance {instance_num}.')
			return False

	def is_port_open(self, port):
		'''Checks if a specific port is open.
		Args:
			port (int): The port number to check.
		Returns:
			bool: True if the port is open, False otherwise.'''
		with socket(AF_INET, SOCK_STREAM) as sock:
			result = sock.connect_ex(('127.0.0.1', port))
			return result == 0
		
	def load_cookies_for_url(self, driver, instance_num, current_url):
		'''Load cookies for a specific URL based on the instance number.
		This method loads cookies from the mapping based on the current URL and instance number.
		It also ensures the cookies are correctly applied by refreshing the page after loading.
		Args:
			driver (WebDriver): The Selenium WebDriver instance where cookies will be loaded.
			instance_num (int): The index of the Tor instance.
			current_url (str): The current URL being accessed by the WebDriver.'''
		if self.cookies_mapping:
			for domain, cookies in self.cookies_mapping.items():
				if domain in current_url:
					cookie_file = cookies.get(str(instance_num % len(cookies)))
					if cookie_file:
						self.cookies_manager.load_cookies(driver, cookie_file, current_url)
					break
		elif self.cookies_dir:
			self.cookies_manager.load_cookies(driver, self.cookies_dir, current_url)

	def execute_function(self, action_num, instance_num, user_function):
		'''Executes the user-provided function with the specified Tor instance.
		Args:
			action_num (int): The action number being performed.
			instance_num (int): The index of the Tor instance.
			user_function (callable): The function to execute, provided by the user.'''
		max_retries = 3
		for attempt in range(max_retries):
			try:
				driver, wait, By, EC = self.configure_selenium_with_tor(instance_num)
				args = {}
				for param in user_function.__code__.co_varnames[:user_function.__code__.co_argcount]:
					if param == 'driver':
						args['driver'] = driver
					elif param == 'wait':
						args['wait'] = wait
					elif param == 'By':
						args['By'] = By
					elif param == 'EC':
						args['EC'] = EC
					elif param == 'instance_num':
						args['instance_num'] = instance_num
					elif param == 'log':
						args['log'] = self.log
				user_function(**args)
				break
			except Exception as e:
				self.log(f'[-] Function error: {e}')
				if attempt < max_retries - 1:
					self.log(f'Retrying... (Attempt {attempt + 2}/{max_retries})')
					self.rotate_tor_ip(instance_num)
				else:
					self.log(f'Max retries reached for action {action_num}, instance {instance_num}')
			finally:
				driver.quit()

	def thread_manager(self, queue, user_function, check_stop_func=None):
		'''Manages the execution of threads, ensuring that actions are processed concurrently.
		Args:
			queue (Queue): The queue containing action numbers.
			user_function (callable): The function to execute for each action.
			check_stop_func (callable, optional): A function to check if execution should stop.'''
		while not queue.empty():
			action_num = queue.get()
			instance_num = action_num % self.total_instances
			if instance_num not in self.tor_processes:
				self.create_tor_instance(instance_num)
			self.execute_function(action_num, instance_num, user_function)
			if not self.rotate_tor_ip(instance_num):
				self.log(f'[-] Failed to rotate IP for instance {instance_num}. Recreating Tor instance.')
				self.create_tor_instance(instance_num)
			queue.task_done()
			if check_stop_func and check_stop_func():
				while not queue.empty():
					queue.get_nowait()
					queue.task_done()
				break

	def run(self, num_actions, user_function, check_stop_func=None):
		'''Runs the specified number of actions concurrently across the available Tor instances.
		This method is the main entry point for executing tasks across multiple Tor instances. It handles
		the initialization, threading, and cleanup process to ensure smooth operation.
		Args:
			num_actions (int): The number of actions to perform.
			user_function (callable): The function to execute for each action.
			check_stop_func (callable, optional): A function to check if execution should stop.'''
		self.clean_up()
		queue = Queue()
		for i in range(num_actions):
			queue.put(i)
		threads = []
		for _ in range(min(num_actions, self.max_threads)):
			t = Thread(target=self.thread_manager, args=(queue, user_function, check_stop_func))
			t.start()
			threads.append(t)
		for t in threads:
			t.join()
		self.clean_up()
# by azuk4r