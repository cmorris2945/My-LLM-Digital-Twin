"""
Base Crawler Classes

This module provides base classes for all web crawlers:
- BaseCrawler: Abstract base for all crawlers
- BaseSeleniumCrawler: Base for crawlers that need browser automation
"""

import time
from abc import ABC, abstractmethod
from tempfile import mkdtemp

import chromedriver_autoinstaller
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from llm_engineering.domain.documents import NoSQLBaseDocument


# Automatically install the correct ChromeDriver version
chromedriver_autoinstaller.install()


class BaseCrawler(ABC):
    """
    Abstract base class for all crawlers.
    
    Each crawler must:
    1. Define a model (document type) for storing data
    2. Implement the extract method
    """
    model: type[NoSQLBaseDocument]

    @abstractmethod
    def extract(self, link: str, **kwargs) -> None:
        """
        Extract data from a given link.
        
        Args:
            link: URL to extract data from
            **kwargs: Additional parameters (e.g., user object)
        """
        ...


class BaseSeleniumCrawler(BaseCrawler, ABC):
    """
    Base class for crawlers that need browser automation.
    
    Used for sites that:
    - Require JavaScript rendering
    - Need login/authentication
    - Have infinite scroll or dynamic content
    """
    
    def __init__(self, scroll_limit: int = 5) -> None:
        """
        Initialize Selenium crawler with Chrome browser.
        
        Args:
            scroll_limit: Maximum number of page scrolls (for infinite scroll sites)
        """
        # Configure Chrome options for headless browsing
        options = webdriver.ChromeOptions()

        # Core options for stability
        options.add_argument("--no-sandbox")                # Bypass OS security model
        options.add_argument("--headless=new")              # Run without GUI
        options.add_argument("--disable-dev-shm-usage")     # Overcome limited resource problems
        options.add_argument("--log-level=3")               # Suppress logs
        
        # Disable popups and notifications
        options.add_argument("--disable-popup-blocking")
        options.add_argument("--disable-notifications")
        options.add_argument("--disable-extensions")
        
        # Performance and security options
        options.add_argument("--disable-background-networking")
        options.add_argument("--ignore-certificate-errors")  
        
        # Use temporary directories for user data
        options.add_argument(f"--user-data-dir={mkdtemp()}") 
        options.add_argument(f"--data-path={mkdtemp()}")      
        options.add_argument(f"--disk-cache-dir={mkdtemp()}")  
        options.add_argument("--remote-debugging-port=9226")   

        # Allow subclasses to add their own options
        self.set_extra_driver_options(options)

        self.scroll_limit = scroll_limit  
        
        # Initialize Chrome driver with options
        self.driver = webdriver.Chrome(  
            options=options,
        )

    def set_extra_driver_options(self, options: Options) -> None:
        """
        Hook for subclasses to add additional Chrome options.
        
        Args:
            options: Chrome options object to modify
        """
        pass

    def login(self) -> None:
        """
        Hook for subclasses to implement login logic.
        
        Override this in crawlers that need authentication.
        """
        pass

    def scroll_page(self) -> None:
        """
        Scroll the page to load dynamic content.
        
        Used for sites with infinite scroll or lazy loading.
        Scrolls until no new content loads or scroll_limit is reached.
        """
        current_scroll = 0
        last_height = self.driver.execute_script("return document.body.scrollHeight")  # Fixed: scrollingHeight -> scrollHeight
        
        while True:
            # Scroll to bottom of page
            self.driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
            time.sleep(5)  # Wait for content to load
            
            # Check if new content loaded
            new_height = self.driver.execute_script("return document.body.scrollHeight")
            
            # Stop if no new content or reached scroll limit
            if new_height == last_height or (self.scroll_limit and current_scroll >= self.scroll_limit):
                break
                
            last_height = new_height  # Fixed: last_night -> last_height
            current_scroll += 1
    
    def __del__(self):
        """
        Cleanup: Close the browser when crawler is destroyed.
        """
        if hasattr(self, 'driver'):
            try:
                self.driver.quit()
            except:
                pass  # Ignore errors during cleanup
