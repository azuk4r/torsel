'''Example: Simple IP rotation using Tor with the Torsel module.
This script demonstrates how to use the Torsel module to create multiple Tor instances
and verify that the IP address changes for each instance using Selenium.
Important:
- The `collect_ip` function is passed to Torsel and automatically executed for each Tor instance.
- The `driver` is managed internally by Torsel. You do not need to instantiate or manage it manually.
- The `wait`, `EC`, and `By` parameters are pre-imported and configured by Torsel.'''
from torsel import Torsel
# Selenium function to invoke in the Torsel object
def collect_ip(driver, wait, EC, By):
    '''Collect the IP address using a Tor instance managed by Torsel.
    Args:
        driver: Selenium WebDriver instance, passed automatically by Torsel.
        wait: WebDriverWait instance for handling explicit waits.
        EC: Expected Conditions module from Selenium to handle conditions.
        By: Selenium By module used for locating elements.
    Notes:
    - The `driver` is pre-configured with the Tor proxy for the given instance.
    - Torsel manages the WebDriver lifecycle, so no need to initialize or close it manually.'''
    driver.get('http://icanhazip.com')
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, 'body'), '.'))
    ip_address = driver.find_element(By.TAG_NAME, 'body').text.strip()
    print(f'[+] Current Tor IP: {ip_address}')
# Invoke Torsel in headless mode
torsel = Torsel(headless=True,
                tor_path='C:/Tor/tor/tor.exe', # windows test
                tor_data_dir='C:/tor_profiles' # windows test
)
# Run Torsel
# 10: Number of actions to perform
# collect_ip: Function to execute for each action
torsel.run(10, collect_ip)
# Results:
# [+] Current Tor IP: 185.220.100.252
# [+] Current Tor IP: 185.220.101.102
# [+] Current Tor IP: 109.70.100.5
# [+] Current Tor IP: 45.138.16.142
# [+] Current Tor IP: 185.220.101.1
# [+] Current Tor IP: 107.189.8.70
# [+] Current Tor IP: 185.220.101.147
# [+] Current Tor IP: 185.220.101.30
# [+] Current Tor IP: 109.70.100.66
# [+] Current Tor IP: 192.42.116.183
# by azuk4r