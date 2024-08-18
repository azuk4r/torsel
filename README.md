# Torsel: Tor and Selenium Automation

**Torsel** is a Python module designed to manage multiple Tor instances and automate web tasks using Selenium. It is particularly useful for web automation and web scraping tasks that require IP rotation to bypass security systems.

## Key Features
- **Automated IP Rotation**: Seamlessly rotate IP addresses using multiple Tor instances.
- **Web Scraping and Automation**: Ideal for tasks that require anonymity and need to bypass IP-based restrictions.
- **Easy Configuration**: Automatically sets up, configures, and manages Tor instances.
- **Integration with Selenium**: Run your Selenium scripts with the added anonymity of Tor.

## Installation
You can install Torsel directly from PyPI:

```
pip install torsel
```

## Usage
For detailed examples on how to use Torsel, please refer to the examples directory. These examples demonstrate how to:
* Verify Tor IP rotation as an example mode of operation:<br>https://github.com/azuk4r/torsel/blob/main/examples/verify_tor_ip_rotation.py
  
### Advanced Configuration
Torsel is highly configurable to suit various use cases:
* **total_instances**: Number of instances to create.
* **max_threads**: Maximum number of concurrent threads.
* **tor_base_port**: Starting port for Tor SOCKS connections.
* **tor_control_base_port:** Starting port for Tor control connections.
* **headless:** Run Selenium in headless mode.
* **verbose:** Enable detailed logging.

## System Requirements
* **Operating System:** Kali Linux (Development and testing conducted on Kali Linux, but it may work on other Linux distributions).
* **Python Version:** Python 3.8 or higher.
* **Dependencies:** Selenium, Stem (for managing Tor).

## Contributing
Contributions are welcome! If you have suggestions or improvements, please feel free to submit a pull request or open an issue on GitHub.

## License
This project is licensed under the MIT License - see the [LICENSE](https://github.com/azuk4r/torsel/blob/main/LICENSE) file for details.
