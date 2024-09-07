# Torsel: Tor and Selenium Automation
**Torsel** is a Python module designed to manage multiple Tor instances and automate web tasks using Selenium. It is particularly useful for web automation and web scraping tasks that require IP rotation to enhance anonymity.

## Disclaimer
This project is currently under development and subject to ongoing updates and enhancements. Please note that features and functionality may change as the project evolves.
It hasn't been tested on MacOS, I welcome feedback and if you wanna collab, see [Contributing](#contributing) 👇

## Key Features
- **Cross-Platform Support**: Compatible with Linux, Windows and macOS.
- **Automated IP Rotation**: Seamlessly rotate IP addresses using multiple Tor instances.
- **Web Scraping and Automation**: Ideal for tasks that require anonymity.
- **Easy Configuration**: Automatically sets up, configures, and manages Tor instances.
- **Integration with Selenium**: Run your Selenium scripts with the added anonymity of Tor.
- **Flexible and Advanced Cookie Management**: Load and manage custom cookies across multiple instances with support for both simple and advanced mapping configurations.
- **Bypassing IP-Based Restrictions**: Torsel can help bypass some IP-based restrictions by rotating IP addresses through Tor nodes.

## Considerations
- **Tor Exit Node Blocking**: Be aware that some websites actively block traffic from Tor exit nodes, which may limit the effectiveness of this approach.
- **Cookie Loading Limitations**: Some sites may have restrictions that prevent successful cookie loading, loading cookies will not always work.

## Installation
You can install Torsel directly from PyPI:
```
pip install torsel
```

## Prerequisites

You need to have Tor installed to invoke the path pointing to the executable inside the Torsel object. On Linux machines make sure you have chromium installed with the following command:
```
sudo apt install chromium
```
You need to run it with elevated permissions to be able to configure the instances, remember to use sudo or run as administrator if you are on Windows.

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

# Torsel object
torsel = Torsel(headless=True, # Invoke Torsel in headless mode and run
                tor_path="/usr/bin/tor", # path to executable
                tor_data_dir="/tmp/tor_profiles") # tor profiles path dest
torsel.run(10, collect_ip)
```

For detailed examples on how to use Torsel, please refer to the [examples directory](https://github.com/azuk4r/torsel/tree/main/examples).

### List of examples:
* [Detailed simple example (Single thread IP rotation)](https://github.com/azuk4r/torsel/blob/main/examples/simple_ip_rotation.py)
* [Verify Tor IP rotation with multithreading](https://github.com/azuk4r/torsel/blob/main/examples/multithread_ip_rotation.py)
* [Script to analyze the frequency of IP usage](https://github.com/azuk4r/torsel/blob/main/examples/tor_ip_usage_analyzer.py)
* [Simple session cookie loading with a single instance and single URL](https://github.com/azuk4r/torsel/blob/main/examples/loading_cookies/simple_one_url_one_instance.py)
* [Simple session cookie loading with multiple instances across the same URL](https://github.com/azuk4r/torsel/blob/main/examples/loading_cookies/simple_one_url_multi_instance.py)
* [Load and verify session cookies for two different URLs with a single instance](https://github.com/azuk4r/torsel/blob/main/examples/loading_cookies/advanced_mapping_two_url_one_instance.py)
* [Load and verify different session cookies for two URLs across multiple instances](https://github.com/azuk4r/torsel/blob/main/examples/loading_cookies/advanced_mapping_two_url_multi_instance.py)

### Advanced Configuration
Torsel is highly configurable to suit various use cases:
* **total_instances**: Number of Tor instances to create.
* **max_threads**: Maximum number of concurrent threads.
* **tor_base_port**: Starting port for Tor SOCKS connections.
* **tor_control_base_port:** Starting port for Tor control connections.
* **tor_path**: Path to the Tor executable.
* **tor_data_dir**: Directory to store Tor profile data.
* **user_agent**: Specifies the user_agent, if None a random one is selected.
* **headless**: Run Selenium in headless mode if `True`.
* **verbose**: Enable detailed logging if `True`.
* **cookies_dir**: Directory to store and load cookies (optional).
* **cookies_mapping**: A mapping of URLs to specific cookie files, allowing for advanced session management across multiple instances (optional).

Additionally, within the Selenium-related configurations, Torsel automatically handles the following parameters for functions declared within it:
* **driver**: Managed by Torsel and passed automatically to your function. No need to instantiate or manage it yourself.
* **wait**: An instance of WebDriverWait configured with a 10-second timeout, provided by Torsel.
* **By**: The By module from Selenium, used for locating elements (e.g., by ID, class name).
* **EC** (ExpectedConditions): The ExpectedConditions module from Selenium, used to define conditions like element visibility or text presence.
* **action_num**: The number of the current action being executed, provided automatically by Torsel.
* **instance_num**: The instance number of the Tor connection in use, passed automatically to your function.
* **log**: A logging function provided by Torsel to output messages during execution.

## Contributing
Hey! 👋 Any kind of contribution is welcome. Send PR if you have improvements or examples of use to contribute!

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/azuk4r/torsel/blob/main/LICENSE) file for details.
