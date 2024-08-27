from torsel import Torsel
from time import sleep

# Declare the initial URL for the session (used to load the correct cookies)
initial_url = "https://www.facebook.com"

def fb_login():
    print('[~] The driver is now automatically navigating to the initial_url to load cookies.')
    sleep(5)
    print('[+] Verified: Successfully logged into FB using loaded cookies.')
    sleep(15)

# Set up the Torsel instance with specified settings
torsel = Torsel(
    total_instances=3,
    max_threads=1,
    headless=False,
    verbose=True,
    cookies_dir='//your/directory/path/cookies_dir'  # Specify the directory where the cookies are stored
)

# Run the task to log into Facebook using the loaded cookies
torsel.run(1, fb_login)

# [~] Cleaning up previous processes, files, and ports...
# [+] Cleanup completed.
# [~] Creating Tor instance 0...
# [+] Tor instance 0 created and running.
# [~] Loading cookies from fb_cookies.json for instance 0
# [+] Cookies loaded from fb_cookies.json
# [~] The driver is now automatically navigating to the initial_url to load cookies.
# [+] Verified: Successfully logged into FB using loaded cookies.
# [+] IP rotated for Tor instance 0.
