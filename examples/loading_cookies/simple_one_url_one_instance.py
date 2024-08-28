from torsel import Torsel
from time import sleep

torsel = Torsel(
    total_instances=1,
    max_threads=1,
    headless=False,
    verbose=True,
    cookies_dir='/path/to/cookies_github'
)

def loading_cookies(driver, wait, By, EC):
    driver.get("https://www.github.com")
    torsel.load_cookies_for_url(driver, 0, "https://www.github.com")
    wait.until(EC.presence_of_element_located((By.XPATH, "//span[contains(text(), 'Dashboard')]")))
    print('[+] Verified: Cookies load correctly executed.')
    sleep(60)

torsel.run(1, loading_cookies)

# Results:

# [~] Cleaning up previous processes, files, and ports...
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [+] Tor instance 0 created and running.
# [~] Trying to load cookies...
# [+] Cookies loaded from github_cookies1.json
# [+] Verified: Cookies load correctly executed.
# [+] IP rotated for Tor instance 0.
