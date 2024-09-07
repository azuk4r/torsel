from torsel import Torsel

# Selenium function to invoke in the Torsel object
def collect_ip(driver, wait, EC, By, action_num, instance_num):
    driver.get("http://icanhazip.com")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "."))
    ip_address = driver.find_element(By.TAG_NAME, "body").text.strip()
    print(f"[+] Action {action_num} | Instance {instance_num} | Current Tor IP: {ip_address}")

# Invoke Torsel in headless mode and run
torsel = Torsel(headless=True, 
                tor_path="C:/Tor/tor/tor.exe",
                tor_data_dir="C:/tor_profiles",
                total_instances=10,
                max_threads=10,
                verbose=True)
torsel.run(100, collect_ip)