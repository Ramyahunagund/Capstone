# tests/conftest.py
import pytest
import time
import os
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage

# Check if running in CI
CI = os.environ.get("CI")  # GitHub Actions sets this automatically

# You can adjust browsers for CI environment
browsers = ["chrome", "firefox"]
if not CI:
    browsers.append("edge")  # Edge only locally


@pytest.fixture(scope="session", params=browsers)
def logged_in_driver(request):
    browser_name = request.param
    # Headless mode in CI
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=True if CI else False)
    driver.get("https://www.demoblaze.com")

    login_page = LoginPage(driver)
    login_page.open_login_modal()
    login_page.enter_username("Ramya Hunagund")
    login_page.enter_password("ramya123")
    login_page.click_login()
    time.sleep(2)  # wait for login to complete

    yield driver
    driver.quit()
