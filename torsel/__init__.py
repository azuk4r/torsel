"""
Torsel - A Python module for managing Tor instances with Selenium, including optional cookie management.
"""

from .torsel import Torsel
from .cookies_manager import CookiesManager

__all__ = ["Torsel", "CookiesManager"]
__version__ = "0.3.3"
