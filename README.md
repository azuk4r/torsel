# Torsel: Tor and Selenium Automation
**Torsel** is a Python module designed to manage multiple Tor instances and automate web tasks using Selenium. It is particularly useful for web automation and web scraping tasks that require IP rotation to enhance anonymity.

## Key Features
- **Automated IP Rotation**: Seamlessly rotate IP addresses using multiple Tor instances.
- **Web Scraping and Automation**: Ideal for tasks that require anonymity.
- **Easy Configuration**: Automatically sets up, configures, and manages Tor instances.
- **Integration with Selenium**: Run your Selenium scripts with the added anonymity of Tor.
- **Flexible Cookie Management**: Load and manage custom cookies across multiple instances.  
## Cybersecurity Considerations
- **Bypassing IP-Based Restrictions**: Torsel can help bypass some IP-based restrictions by rotating IP addresses through Tor nodes.
- **Tor Exit Node Blocking**: Be aware that some websites actively block traffic from Tor exit nodes, which may limit the effectiveness of this approach.

## Installation
You can install Torsel directly from PyPI:

```bash
pip install torsel
```

## Prerequisites

Ensure your machine has the required packages installed by running the following command:
```bash
sudo apt install tor chromium psmisc
```

This command installs **Tor**, **Chromium**, and **psmisc** (required for the `killall` command).

## Usage

### Simple example
This simple example scrapes the IP address 10 times, demonstrating IP rotation using Tor:
```python
from torsel import Torsel

# Selenium function to invoke in the Torsel object
def collect_ip(driver, wait, EC, By):
    driver.get("http://icanhazip.com")
    wait.until(EC.text_to_be_present_in_element((By.TAG_NAME, "body"), "."))
    ip_address = driver.find_element(By.TAG_NAME, "body").text.strip()
    print(f"[+] Current Tor IP: {ip_address}")

# Invoke Torsel in headless mode and run
torsel = Torsel(headless=True)
torsel.run(10, collect_ip)
```

For detailed examples on how to use Torsel, please refer to the [examples directory](https://github.com/azuk4r/torsel/tree/main/examples).

### List of examples:
* [Detailed simple example (Single thread IP rotation)](https://github.com/azuk4r/torsel/blob/main/examples/simple_ip_rotation.py)
* [Verify Tor IP rotation with multithreading](https://github.com/azuk4r/torsel/blob/main/examples/multithread_ip_rotation.py)
* [Script to analyze the frequency of IP usage](https://github.com/azuk4r/torsel/blob/main/examples/tor_ip_usage_analyzer.py)
* [Load and verify session cookies automatically](https://github.com/azuk4r/torsel/blob/main/examples/loading_cookies_example.py)

### Advanced Configuration
Torsel is highly configurable to suit various use cases:
* **total_instances**: Number of instances to create.
* **max_threads**: Maximum number of concurrent threads.
* **tor_base_port**: Starting port for Tor SOCKS connections.
* **tor_control_base_port:** Starting port for Tor control connections.
* **headless:** Run Selenium in headless mode.
* **verbose:** Enable detailed logging.

Additionally, within the Selenium-related configurations, Torsel automatically handles the following:
* **driver:** Managed by Torsel and passed automatically to your function. No need to instantiate or manage it yourself.
* **wait:** An instance of WebDriverWait configured with a 10-second timeout, provided by Torsel.
* **By:** The By module from Selenium, used for locating elements (e.g., by ID, class name).
* **EC** (ExpectedConditions): The ExpectedConditions module from Selenium, used to define conditions like element visibility or text presence.

## System Requirements
* **Operating System:** Development and testing conducted on WSL Kali Linux, but it may work on other Linux distributions.
* **Python Version:** Python 3.8 or higher.
* **Dependencies:** Selenium, Stem (for managing Tor).

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/azuk4r/torsel/blob/main/LICENSE) file for details.
