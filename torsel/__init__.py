'''Torsel - A Python module for managing Tor instances with Selenium.'''
from .torsel import Torsel
from .cookies_manager import CookiesManager
__all__ = ['Torsel', 'CookiesManager']
__version__ = '0.4.1'
# by azuk4r