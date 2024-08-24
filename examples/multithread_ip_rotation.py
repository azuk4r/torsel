"""
Example: Verifying IP rotation using Tor with the Torsel module.

This script demonstrates how to use the Torsel module to create multiple Tor instances
and verify that the IP address changes for each instance using Selenium.

Important:
- The `collect_ip` function is passed to Torsel and automatically executed for each Tor instance.
- The `driver` is managed internally by Torsel. You do not need to instantiate or manage it.
- The `wait`, `EC`, and `By` parameters are pre-imported and configured by Torsel to simplify interactions with Selenium.
- Both `action_num` and `instance_num` are passed to the function to indicate the specific action and instance being used.
- The `log` function is provided by Torsel for internal logging; you can use it for conditional logging within your function.
- The `max_retries` parameter is used to define how many attempts should be made to retrieve the IP address if the initial attempts fail.
"""

from torsel import Torsel

def collect_ip(driver, wait, EC, By, action_num, instance_num, log, max_retries=5):
    """
    Collect the IP address using a Tor instance managed by Torsel.

    Args:
        driver: Selenium WebDriver instance, passed automatically by Torsel.
        wait: WebDriverWait instance for handling explicit waits.
        EC: Expected Conditions module from Selenium to handle conditions.
        By: Selenium By module used for locating elements.
        action_num: The action number being performed.
        instance_num: The index of the Tor instance being used.
        log: The log function to use for logging messages.
        max_retries: Maximum number of retries if IP retrieval fails (default is 5).

    Notes:
    - The `driver` is pre-configured with the Tor proxy for the given instance.
    - Torsel manages the WebDriver lifecycle, so no need to initialize or close it manually.
    """
    attempts = 0
    ip_address = None

    while attempts < max_retries:
        try:
            driver.get("http://icanhazip.com")
            wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "."))
            ip_address = driver.find_element(By.TAG_NAME, "body").text.strip()
            break
        except Exception as e:
            attempts += 1

    print(f"[+] Action {action_num}, Instance {instance_num}, Current Tor IP: {ip_address}")

    if ip_address is None:
        # This log will not be displayed unless verbose logging is enabled
        log(f"[-] Action {action_num}, Instance {instance_num} - Unable to retrieve IP after {max_retries} attempts.")

# Configure Torsel
torsel = Torsel(
    total_instances=30,       # Number of Tor instances to create
    max_threads=15,           # Max concurrent threads allowed
    headless=True,            # Run Selenium in headless mode
    verbose=False             # If set to True, detailed logs will be shown
)

# Run the IP collection across multiple Tor instances
# 100: Number of actions to perform (100 IP retrievals)
# collect_ip: Function to execute for each action
torsel.run(100, collect_ip)

# Results:
# [+] Action 6, Instance 6, Current Tor IP: 185.220.101.16
# [+] Action 12, Instance 12, Current Tor IP: 192.42.116.208
# [+] Action 4, Instance 4, Current Tor IP: 37.120.190.85
# [+] Action 9, Instance 9, Current Tor IP: 185.220.101.186
# [+] Action 10, Instance 10, Current Tor IP: 192.42.116.211
# [+] Action 13, Instance 13, Current Tor IP: 192.42.116.191
# [+] Action 0, Instance 0, Current Tor IP: 185.241.208.115
# [+] Action 7, Instance 7, Current Tor IP: 192.42.116.181
# [+] Action 2, Instance 2, Current Tor IP: 89.147.111.124
# [+] Action 11, Instance 11, Current Tor IP: 192.42.116.22
# [+] Action 5, Instance 5, Current Tor IP: 185.244.192.184
# [+] Action 14, Instance 14, Current Tor IP: 139.162.249.209
# [+] Action 1, Instance 1, Current Tor IP: 192.42.116.187
# [+] Action 3, Instance 3, Current Tor IP: 51.38.225.46
# [+] Action 8, Instance 8, Current Tor IP: 45.139.122.176
# [+] Action 17, Instance 17, Current Tor IP: 45.138.16.76
# [+] Action 18, Instance 18, Current Tor IP: 192.42.116.186
# [+] Action 15, Instance 15, Current Tor IP: 185.220.101.109
# [+] Action 20, Instance 20, Current Tor IP: 109.70.100.67
# [+] Action 16, Instance 16, Current Tor IP: 192.42.116.191
# [+] Action 21, Instance 21, Current Tor IP: 185.220.101.31
# [+] Action 24, Instance 24, Current Tor IP: 185.220.101.39
# [+] Action 22, Instance 22, Current Tor IP: 54.36.209.253
# [+] Action 19, Instance 19, Current Tor IP: 185.220.101.162
# [+] Action 27, Instance 27, Current Tor IP: 185.220.101.107
# [+] Action 23, Instance 23, Current Tor IP: 80.67.167.81
# [+] Action 31, Instance 1, Current Tor IP: 192.42.116.214
# [+] Action 30, Instance 0, Current Tor IP: 192.42.116.203
# [+] Action 29, Instance 29, Current Tor IP: 185.220.100.255
# [+] Action 26, Instance 26, Current Tor IP: 204.8.96.79
# [+] Action 32, Instance 2, Current Tor IP: 192.42.116.214
# [+] Action 33, Instance 3, Current Tor IP: 192.42.116.193
# [+] Action 34, Instance 4, Current Tor IP: 185.220.101.59
# [+] Action 25, Instance 25, Current Tor IP: 185.107.57.64
# [+] Action 35, Instance 5, Current Tor IP: 204.8.96.110
# [+] Action 36, Instance 6, Current Tor IP: 192.42.116.208
# [+] Action 38, Instance 8, Current Tor IP: 185.220.101.80
# [+] Action 37, Instance 7, Current Tor IP: 185.220.101.83
# [+] Action 40, Instance 10, Current Tor IP: 185.132.53.12
# [+] Action 39, Instance 9, Current Tor IP: 5.255.115.58
# [+] Action 41, Instance 11, Current Tor IP: 185.220.100.253
# [+] Action 42, Instance 12, Current Tor IP: 193.142.147.69
# [+] Action 43, Instance 13, Current Tor IP: 94.16.121.91
# [+] Action 46, Instance 16, Current Tor IP: 193.189.100.197
# [+] Action 44, Instance 14, Current Tor IP: 45.139.122.176
# [+] Action 47, Instance 17, Current Tor IP: 192.42.116.178
# [+] Action 45, Instance 15, Current Tor IP: 80.67.167.81
# [+] Action 48, Instance 18, Current Tor IP: 185.220.101.3
# [+] Action 49, Instance 19, Current Tor IP: 185.220.101.17
# [+] Action 50, Instance 20, Current Tor IP: 192.42.116.194
# [+] Action 51, Instance 21, Current Tor IP: 198.98.51.52
# [+] Action 52, Instance 22, Current Tor IP: 185.220.100.254
# [+] Action 54, Instance 24, Current Tor IP: 185.220.101.57
# [+] Action 53, Instance 23, Current Tor IP: 199.195.251.119
# [+] Action 56, Instance 26, Current Tor IP: 192.42.116.196
# [+] Action 57, Instance 27, Current Tor IP: 23.129.64.213
# [+] Action 59, Instance 29, Current Tor IP: 185.220.101.109
# [+] Action 60, Instance 0, Current Tor IP: 204.8.96.165
# [+] Action 28, Instance 28, Current Tor IP: 51.89.153.112
# [+] Action 58, Instance 28, Current Tor IP: 51.89.153.112
# [+] Action 61, Instance 1, Current Tor IP: 104.244.73.43
# [+] Action 62, Instance 2, Current Tor IP: 198.98.54.49
# [+] Action 63, Instance 3, Current Tor IP: 109.70.100.3
# [+] Action 55, Instance 25, Current Tor IP: 37.46.211.24
# [+] Action 64, Instance 4, Current Tor IP: 185.220.101.83
# [+] Action 65, Instance 5, Current Tor IP: 23.154.177.14
# [+] Action 66, Instance 6, Current Tor IP: 212.95.50.77
# [+] Action 67, Instance 7, Current Tor IP: 185.193.52.180
# [+] Action 68, Instance 8, Current Tor IP: 192.42.116.177
# [+] Action 70, Instance 10, Current Tor IP: 5.45.104.176
# [+] Action 74, Instance 14, Current Tor IP: 185.107.57.66
# [+] Action 71, Instance 11, Current Tor IP: 185.220.101.30
# [+] Action 73, Instance 13, Current Tor IP: 109.70.100.4
# [+] Action 72, Instance 12, Current Tor IP: 23.154.177.12
# [+] Action 75, Instance 15, Current Tor IP: 194.26.192.77
# [+] Action 76, Instance 16, Current Tor IP: 104.244.79.61
# [+] Action 77, Instance 17, Current Tor IP: 176.114.248.225
# [+] Action 69, Instance 9, Current Tor IP: 185.220.101.108
# [+] Action 78, Instance 18, Current Tor IP: 185.243.218.110
# [+] Action 79, Instance 19, Current Tor IP: 185.220.101.102
# [+] Action 80, Instance 20, Current Tor IP: 171.25.193.80
# [+] Action 81, Instance 21, Current Tor IP: 192.42.116.214
# [+] Action 82, Instance 22, Current Tor IP: 204.8.96.114
# [+] Action 83, Instance 23, Current Tor IP: 185.220.101.13
# [+] Action 84, Instance 24, Current Tor IP: 185.220.101.37
# [+] Action 86, Instance 26, Current Tor IP: 188.68.49.235
# [+] Action 87, Instance 27, Current Tor IP: 185.100.85.24
# [+] Action 90, Instance 0, Current Tor IP: 45.9.148.113
# [+] Action 88, Instance 28, Current Tor IP: 45.139.122.176
# [+] Action 89, Instance 29, Current Tor IP: 185.220.101.30
# [+] Action 91, Instance 1, Current Tor IP: 192.42.116.179
# [+] Action 85, Instance 25, Current Tor IP: 192.42.116.184
# [+] Action 92, Instance 2, Current Tor IP: 107.189.5.121
# [+] Action 93, Instance 3, Current Tor IP: 45.138.16.42
# [+] Action 94, Instance 4, Current Tor IP: 173.249.57.253
# [+] Action 95, Instance 5, Current Tor IP: 51.89.153.112
# [+] Action 96, Instance 6, Current Tor IP: 23.137.253.108
# [+] Action 97, Instance 7, Current Tor IP: 185.220.101.1
# [+] Action 98, Instance 8, Current Tor IP: 109.70.100.3
# [+] Action 99, Instance 9, Current Tor IP: 107.189.8.65
