from torsel import Torsel
from time import sleep

cookies_mapping = {
    "github.com": {"0": "/path/to/github_cookies.json"},
    "facebook.com": {"0": "/path/to/facebook_cookies.json"}
}

torsel = Torsel(
    total_instances=1,
    max_threads=1,
    headless=False,
    verbose=True,
    cookies_mapping=cookies_mapping
)

def loading_mapped_cookies(driver, wait, By, EC):
    driver.get("https://www.github.com")
    torsel.load_cookies_for_url(driver, 0, "https://www.github.com")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Dashboard')]")))
    print('[+] Verified: Github cookies load correctly executed.')
    sleep(30)
    driver.get("https://www.facebook.com")
    torsel.load_cookies_for_url(driver, 0, "https://www.facebook.com")
    wait.until(EC.presence_of_element_located((By.TAG_NAME, "body")))
    print('[+] Verified: Facebook cookies load correctly executed.')
    sleep(30)

torsel.run(1, loading_mapped_cookies)

# [~] Cleaning up previous processes, files, and ports...
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [+] Tor instance 0 created and running.
# [~] Trying to load cookies...
# [+] Cookies loaded from /path/to/github_cookies.json
# [+] Verified: Github cookies load correctly executed.
# [~] Trying to load cookies...
# [+] Cookies loaded from /path/to/facebook_cookies.json
# [+] Verified: Facebook cookies load correctly executed.
# [+] IP rotated for Tor instance 0.
