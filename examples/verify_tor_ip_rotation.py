"""
Example: Verifying IP rotation using Tor with the Torsel module.

This script demonstrates how to use the Torsel module to create multiple Tor instances
and verify that the IP address changes for each instance using Selenium.

Important:
- The `driver` is managed internally by Torsel. You do not need to instantiate or manage it.
- The `collect_ip` function is passed to Torsel and automatically executed for each Tor instance.
- Both `action_num` and `instance_num` are passed to the function to indicate the specific action and instance being used.
"""

from torsel import Torsel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep

def collect_ip(driver, action_num, instance_num, log, max_retries=5):
    """
    Collect the IP address using a Tor instance managed by Torsel.

    Args:
        driver: Selenium WebDriver instance, passed automatically by Torsel.
        action_num: The action number being performed.
        instance_num: The index of the Tor instance being used.
        log: The log function to use for logging messages.
        max_retries: Maximum number of retries if IP retrieval fails.

    Notes:
    - The `driver` is pre-configured with the Tor proxy for the given instance.
    - Torsel manages the WebDriver lifecycle, so no need to initialize or close it manually.
    """
    attempts = 0
    ip_address = None

    while attempts < max_retries:
        try:
            driver.get("http://icanhazip.com")
            WebDriverWait(driver, 10).until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "."))
            sleep(0.5)
            ip_address = driver.find_element(By.TAG_NAME, "body").text.strip()
            break
        except Exception as e:
            attempts += 1

    print(f"[+] Action {action_num}, Instance {instance_num}, Current Tor IP: {ip_address}")

    if ip_address is None:
        # This log will not be displayed unless it is set to True
        log(f"[-] Action {action_num}, Instance {instance_num} - Unable to retrieve IP after {max_retries} attempts.")

# Configure Torsel
torsel = Torsel(
    total_instances=30,       # Number of Tor instances to create
    max_threads=15,           # Max concurrent threads allowed
    tor_base_port=9050,       # Starting port for Tor SOCKS connections
    tor_control_base_port=9151, # Starting port for Tor control connections
    tor_path="/usr/bin/tor",  # Path to the Tor executable
    tor_data_dir="/tmp/tor_profiles", # Directory for storing Tor profiles
    headless=True,            # Run Selenium in headless mode
    verbose=False             # If set to True, detailed logs will be shown
)

# Run the IP collection across multiple Tor instances
torsel.run(
    1000,         # Number of actions to perform (1000 IP retrievals)
    collect_ip,  # Function to execute for each action
)
