'''Example: IP collection and tracking using Tor with the Torsel module.
This script demonstrates how to use the Torsel module to create multiple Tor instances,
collect IP addresses, and track their usage frequency across many actions using Selenium.
Important:
- The `collect_and_track_ip` function is passed to Torsel and automatically executed for each Tor instance.
- The `driver` is managed internally by Torsel. You do not need to instantiate or manage it manually.
- The `wait`, `EC`, and `By` parameters are pre-imported and configured by Torsel.
- The `action_num` and `instance_num` parameters are provided by Torsel to track the specific action and instance being used.
- The `log` function is provided by Torsel for conditional logging.'''
from torsel import Torsel
from collections import defaultdict
# Dictionary to store the frequency of each IP
ip_usage_count = defaultdict(int)

def collect_and_track_ip(driver, wait, By, EC, action_num, instance_num, log, max_retries=5):
    '''Collect and track the IP address using a Tor instance managed by Torsel.
    Args:
        driver: Selenium WebDriver instance, passed automatically by Torsel.
        wait: WebDriverWait instance for handling explicit waits.
        By: Selenium By module used for locating elements.
        EC: Expected Conditions module from Selenium to handle conditions.
        action_num: The action number being performed.
        instance_num: The index of the Tor instance being used.
        log: The log function to use for logging messages.
        max_retries: Maximum number of retries if IP retrieval fails.
    Notes:
    - The `driver` is pre-configured with the Tor proxy for the given instance.
    - Torsel manages the WebDriver lifecycle, so no need to initialize or close it manually.'''
    attempts = 0
    ip_address = None
    while attempts < max_retries:
        try:
            driver.get('http://icanhazip.com')
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), '.'))
            ip_address = driver.find_element(By.TAG_NAME, 'body').text.strip()
            break
        except Exception as e:
            attempts += 1
    if ip_address is not None:
        ip_usage_count[ip_address] += 1
        print(f'[+] Action {action_num}, Instance {instance_num}, Current Tor IP: {ip_address}')
    else:
        log(f'[-] Action {action_num}, Instance {instance_num} - Unable to retrieve IP after {max_retries} attempts.')

def print_ip_statistics():
    '''Print the statistics of IP usage after all actions are completed.'''
    print('\n[+] IP Usage Summary:')
    unique_ips = len(ip_usage_count)
    non_repeated_ips = sum(1 for count in ip_usage_count.values() if count == 1)
    for ip, count in ip_usage_count.items():
        print(f'IP used: {ip} {count} times')
    print(f'\nTotal used: {unique_ips} IPs.')
    print(f'Not reused: {non_repeated_ips} IPs.')
# Configure Torsel
torsel = Torsel(
    total_instances=70,       # Number of Tor instances to create
    max_threads=15,           # Max concurrent threads allowed
    tor_path='C:/Tor/tor/tor.exe', # windows test
    tor_data_dir='C:/tor_profiles', # windows test
    headless=True,            # Run Selenium in headless mode
    verbose=True              # If set to True, detailed logs will be shown
)
# Run the IP collection and tracking across multiple Tor instances
torsel.run(
    10000,                    # Number of actions to perform (10k IP retrievals)
    collect_and_track_ip,     # Function to execute for each action
)
# Print IP statistics after all actions are completed
print_ip_statistics()
# Results comparison:
# ------------------
# 10k actions results:
# -------------------
# Total used: 1009 IPs
# Not reused: 176 IPs
#         VS
# 100k actions results:
# --------------------
# Total used: 1176 IPs
# Not reused: 21 IPs
# by azuk4r