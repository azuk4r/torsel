from torsel import Torsel
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from time import sleep
from collections import defaultdict

# Dictionary to store the frequency of each IP
ip_usage_count = defaultdict(int)

def collect_and_track_ip(driver, action_num, instance_num, log, max_retries=5):
    """
    Collect and track the IP address using a Tor instance managed by Torsel.

    Args:
        driver: Selenium WebDriver instance, passed automatically by Torsel.
        action_num: The action number being performed.
        instance_num: The index of the Tor instance being used.
        log: The log function to use for logging messages.
        max_retries: Maximum number of retries if IP retrieval fails.
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

    if ip_address is not None:
        ip_usage_count[ip_address] += 1
        print(f"[+] Action {action_num}, Instance {instance_num}, Current Tor IP: {ip_address}")
    else:
        log(f"[-] Action {action_num}, Instance {instance_num} - Unable to retrieve IP after {max_retries} attempts.")

def print_ip_statistics():
    """
    Print the statistics of IP usage after all actions are completed.
    """
    print("\n[+] IP Usage Summary:")
    unique_ips = len(ip_usage_count)
    non_repeated_ips = sum(1 for count in ip_usage_count.values() if count == 1)

    for ip, count in ip_usage_count.items():
        print(f"IP utilizada: {ip} {count} veces")

    print(f"\nSe han utilizado en total: {unique_ips} número de IPs.")
    print(f"No se han reutilizado: {non_repeated_ips} número de IPs.")

# Configure Torsel
torsel = Torsel(
    total_instances=70,       # Number of Tor instances to create
    max_threads=15,           # Max concurrent threads allowed
    tor_base_port=9050,       # Starting port for Tor SOCKS connections
    tor_control_base_port=9151, # Starting port for Tor control connections
    tor_path="/usr/bin/tor",  # Path to the Tor executable
    tor_data_dir="/tmp/tor_profiles", # Directory for storing Tor profiles
    headless=True,            # Run Selenium in headless mode
    verbose=True              # If set to True, detailed logs will be shown
)

# Run the IP collection and tracking across multiple Tor instances
torsel.run(
    300000, # Number of actions to perform (300k IP retrievals)
    collect_and_track_ip, # Function to execute for each action
)

# Print IP statistics after all actions are completed
print_ip_statistics()
