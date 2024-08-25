"""
Example: Using the cookies_manager=True option in Torsel.

This script demonstrates how to use the Torsel module to automatically manage cookies 
for each website visited within the `example_function` when `cookies_manager=True` is set.

Key Points:
- When `cookies_manager=True`, the module automatically detects and stores cookies for each URL visited using `driver.get`.
- Cookies are saved per instance and URL, ensuring consistency across multiple actions within the same session.
- On each action, cookies are loaded for the corresponding URL before performing any operations on that page.
- The function focuses on demonstrating this behavior by visiting a test website, retrieving the IP address, and printing it.

How it works:
1. `Torsel` identifies URLs in `driver.get` statements within the provided function.
2. If `cookies_manager=True`, cookies are generated and saved before any action is performed on the URLs.
3. For subsequent actions, the stored cookies for each URL are loaded, ensuring consistency in user sessions across multiple actions.

This example is simplified to show the basic functionality of `cookies_manager=True`.
"""

from torsel import Torsel

def example_function(driver, wait, EC, By, action_num, instance_num):
    # Visiting a test website to retrieve and display the current IP address.
    driver.get('https://dnsleaktest.com')
    ip_element = wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'p.hello')))
    ip_address = ip_element.text.split(' ')[1]
    print(f"[+] Action {action_num} - Instance {instance_num} - Current IP: {ip_address}")

# Configure Torsel with cookies_manager=True to enable automatic cookie handling.
torsel = Torsel(headless=True, verbose=True, cookies_manager=True)

# Run the function across 3 actions, demonstrating the cookies_manager behavior.
torsel.run(3, example_function)

# Expected output:
# [~] Cleaning up previous processes, files, and ports...
# [~] Cleaning old cookies...
# [+] Cookie cleanup done.
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [+] Tor instance 0 created and running.
# [+] Cookies saved for instance 0 (https://dnsleaktest.com)
# [+] Action 0 - Instance 0 - Current IP: 45.138.16.107
# [+] IP rotated for Tor instance 0.
# [+] Cookies saved for instance 0 (https://dnsleaktest.com)
# [+] Action 1 - Instance 0 - Current IP: 185.220.101.24
# [+] IP rotated for Tor instance 0.
# [+] Cookies saved for instance 0 (https://dnsleaktest.com)
# [+] Action 2 - Instance 0 - Current IP: 54.36.209.253
# [+] IP rotated for Tor instance 0.
