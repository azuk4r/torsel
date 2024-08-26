"""
Example: Multithreading with Torsel and Selenium for Anonymous IP Collection

This script demonstrates how to use the Torsel module to manage multiple Tor instances
and collect IP addresses using multithreading. The script configures Selenium to use
Tor proxies, visits the `dnsleaktest.com` website to collect IP addresses, and saves the
cookies generated for the session. This approach ensures that each instance of Selenium
has a fresh set of cookies for better anonymity.

Key points:
- The `example_function` is passed to Torsel and executed concurrently across multiple threads.
- The `driver`, `wait`, `EC`, and `By` parameters are managed and passed automatically by Torsel.
- `action_num` is used to track the specific action being performed, allowing for easy monitoring.
- Each instance of Tor operates independently, ensuring that IP rotation and cookie management
  are handled seamlessly across all threads.
- This example uses 5 Tor instances and runs 5 concurrent threads for optimal performance.

Output:
- The IP addresses collected by each instance are printed alongside the action number, indicating
  which instance retrieved which IP address.
"""

from torsel import Torsel

# Function to visit a website and collect the current IP address
def example_function(driver, wait, EC, By, action_num, instance_num):
    driver.get('https://dnsleaktest.com')
    ip_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.hello')))
    ip_address = ip_element.text.split(' ')[1]
    print(f"[+] Action {action_num} - Instance {instance_num} - Current IP: {ip_address}")

# Configuring Torsel with 5 Tor instances and 5 concurrent threads
# Configure Torsel with cookies_manager=True to enable automatic cookie handling.
torsel = Torsel(total_instances=5, max_threads=5, headless=True, verbose=True, cookies_manager=True)

# Running the example function across 5 actions
torsel.run(5, example_function)

# Results:
# [~] Cleaning up previous processes, files, and ports...
# [~] Cleaning old cookies...
# [+] Cookie cleanup done.
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [~] Creating Tor instance 1...
# [~] Creating Tor instance 2...
# [~] Creating Tor instance 3...
# [~] Creating Tor instance 4...
# [+] Tor instance 0 created and running.
# [+] Tor instance 2 created and running.
# [+] Tor instance 1 created and running.
# [+] Tor instance 4 created and running.
# [+] Tor instance 3 created and running.
# [+] Cookies saved for instance 0 (https://dnsleaktest.com)
# [+] Cookies saved for instance 4 (https://dnsleaktest.com)
# [+] Cookies saved for instance 2 (https://dnsleaktest.com)
# [+] Current IP: 192.42.116.173 - Action 0 - Instance 0 done.
# [+] Cookies saved for instance 3 (https://dnsleaktest.com)
# [+] Current IP: 185.220.101.107 - Action 2 - Instance 2 done.
# [+] Current IP: 51.81.254.14 - Action 4 - Instance 4 done.
# [+] Current IP: 185.220.101.66 - Action 3 - Instance 3 done.
# [+] Cookies saved for instance 1 (https://dnsleaktest.com)
# [+] Current IP: 185.220.101.54 - Action 1 - Instance 1 done.
# [+] IP rotated for Tor instance 0.
# [+] IP rotated for Tor instance 2.
# [+] IP rotated for Tor instance 4.
# [+] IP rotated for Tor instance 3.
# [+] IP rotated for Tor instance 1.
