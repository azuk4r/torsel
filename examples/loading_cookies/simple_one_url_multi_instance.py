from torsel import Torsel
from time import sleep

torsel = Torsel(
    total_instances=3,
    max_threads=3,
    headless=False,
    verbose=True,
    cookies_dir='/path/to/cookies_github'
)

def loading_cookies(driver, wait, By, EC, instance_num):
    driver.get("https://www.github.com")
    torsel.load_cookies_for_url(driver, instance_num, "https://www.github.com")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Dashboard')]")))
    print('[+] Verified: Github cookies load correctly executed.')
    sleep(60)

torsel.run(3, loading_cookies)

# Results:

# [~] Cleaning up previous processes, files, and ports...
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [~] Creating Tor instance 1...
# [~] Creating Tor instance 2...
# [+] Tor instance 1 created and running.
# [+] Tor instance 2 created and running.
# [+] Tor instance 0 created and running.
# [~] Trying to load cookies...
# [~] Trying to load cookies...
# [~] Trying to load cookies...
# [+] Cookies loaded from github_cookies1.json
# [+] Cookies loaded from github_cookies.json
# [+] Cookies loaded from github_cookies1.json
# [+] Verified: Github cookies load correctly executed.
# [+] Verified: Github cookies load correctly executed.
# [+] Verified: Github cookies load correctly executed.
# [+] IP rotated for Tor instance 2.
# [+] IP rotated for Tor instance 1.
# [+] IP rotated for Tor instance 0.
