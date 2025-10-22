from selenium import webdriver
from selenium.webdriver.chrome.service import Service as ChromeService
from selenium.webdriver.edge.service import Service as EdgeService
from selenium.webdriver.firefox.service import Service as FirefoxService
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.edge.options import Options as EdgeOptions
from selenium.webdriver.firefox.options import Options as FirefoxOptions
from webdriver_manager.chrome import ChromeDriverManager
from webdriver_manager.microsoft import EdgeChromiumDriverManager
from webdriver_manager.firefox import GeckoDriverManager
import os

class DriverFactory:
    @staticmethod
    def get_driver(browser_name="chrome", headless=False):
        browser_name = browser_name.lower()
        driver = None

        try:
            if browser_name == "chrome":
                options = ChromeOptions()
                if headless:
                    options.add_argument("--headless=new")
                driver = webdriver.Chrome(service=ChromeService(ChromeDriverManager().install()), options=options)

            elif browser_name == "edge":
                options = EdgeOptions()
                if headless:
                    options.add_argument("--headless=new")
                try:
                    driver = webdriver.Edge(service=EdgeService(EdgeChromiumDriverManager().install()), options=options)
                except Exception as e:
                    print(f"[Warning] Edge driver download failed: {e}")
                    local_edge_path = r"C:\WebDrivers\Edge\msedgedriver.exe"
                    if os.path.exists(local_edge_path):
                        print(f"[Fallback] Using local Edge driver from {local_edge_path}")
                        driver = webdriver.Edge(service=EdgeService(local_edge_path), options=options)
                    else:
                        raise FileNotFoundError(
                            f"Edge driver not found at {local_edge_path} and could not be downloaded."
                        )

            elif browser_name == "firefox":
                options = FirefoxOptions()
                if headless:
                    options.add_argument("--headless")
                driver = webdriver.Firefox(service=FirefoxService(GeckoDriverManager().install()), options=options)

            else:
                raise ValueError(f"Unsupported browser: {browser_name}")

            driver.maximize_window()
            return driver

        except Exception as e:
            print(f"[Error] Failed to initialize driver for {browser_name}: {e}")
            raise
