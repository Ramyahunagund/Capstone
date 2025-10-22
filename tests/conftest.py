# # tests/conftest.py
# import pytest
# import time
# from drivers.driver_factory import DriverFactory
# from pages.login_page import LoginPage
#
# # @pytest.fixture(scope="session", params=["chrome", "edge", "firefox"])
# @pytest.fixture(scope="session", params=["chrome"])  # keep only chrome for CI
# def logged_in_driver(request):
#     browser_name = request.param
#     driver = DriverFactory.get_driver(browser_name=browser_name, headless=False)
#     driver.get("https://www.demoblaze.com")
#     login_page = LoginPage(driver)
#     login_page.open_login_modal()
#     login_page.enter_username("Ramya Hunagund")
#     login_page.enter_password("ramya123")
#     login_page.click_login()
#     time.sleep(2)  # wait for login to complete
#     yield driver
#     driver.quit()
# tests/conftest.py
import pytest
import time
import os
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage

@pytest.fixture(scope="session", params=["chrome"])  # CI-friendly
def logged_in_driver(request):
    browser_name = request.param

    # ✅ Use headless mode in CI
    is_ci = os.getenv("CI", "false").lower() == "true"
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=is_ci)

    # Open the website and login
    driver.get("https://www.demoblaze.com")
    login_page = LoginPage(driver)
    login_page.open_login_modal()
    login_page.enter_username("Ramya Hunagund")
    login_page.enter_password("ramya123")
    login_page.click_login()
    time.sleep(2)  # wait for login to complete

    yield driver
    driver.quit()
