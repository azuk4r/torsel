from torsel import Torsel
from time import sleep

cookies_mapping = {
    'github.com': {'0': r'C:\path\to\cookies.json', '1': r'C:\path\to\cookies.json'},
    'facebook.com': {'0': r'C:\path\to\cookies.json', '1': r'C:\path\to\cookies.json'}
}

def loading_mapped_cookies(driver, wait, By, EC, instance_num):
    driver.get('https://www.facebook.com')
    torsel.load_cookies_for_url(driver, instance_num, 'https://www.facebook.com')
    wait.until(EC.presence_of_element_located((By.TAG_NAME, 'body')))
    print('[+] Verified: Facebook cookies load correctly executed.')
    sleep(10)
    driver.get('https://www.github.com')
    torsel.load_cookies_for_url(driver, instance_num, 'https://www.github.com')
    wait.until(EC.presence_of_element_located((By.XPATH, '//span[contains(text(), "Dashboard")]')))
    print('[+] Verified: Github cookies load correctly executed.')
    sleep(10)

torsel = Torsel(
    total_instances=2,
    max_threads=2,
    tor_path='C:/Tor/tor/tor.exe', # windows test
    tor_data_dir='C:/tor_profiles', # windows test
    headless=False,
    verbose=True,
    cookies_mapping=cookies_mapping
)

torsel.run(2, loading_mapped_cookies)
# Results:
# [~] Cleaning up previous processes, files, and ports...
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [~] Creating Tor instance 1...
# [+] Tor instance 0 created and running.
# [+] Tor instance 1 created and running.
# [~] Trying to load cookies...
# [~] Trying to load cookies...
# [+] Cookies loaded from /path/to/facebook_cookies.json
# [+] Cookies loaded from /path/to/facebook_cookies1.json
# [+] Verified: Facebook cookies load correctly executed.
# [+] Verified: Facebook cookies load correctly executed.
# [~] Trying to load cookies...
# [~] Trying to load cookies...
# [+] Cookies loaded from /path/to/github_cookies1.json
# [+] Cookies loaded from /path/to/github_cookies.json
# [+] Verified: Github cookies load correctly executed.
# [+] Verified: Github cookies load correctly executed.
# [+] IP rotated for Tor instance 1.
# [+] IP rotated for Tor instance 0.
# by azuk4r