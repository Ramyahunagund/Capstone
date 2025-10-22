import pytest
import csv
import os
import time
import requests
from drivers.driver_factory import DriverFactory
from pages.login_page import LoginPage
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


# --------------------------- Data Handling ---------------------------
def ensure_login_data():
    folder = os.path.join(os.getcwd(), "testdata")
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "login_data.csv")

    if not os.path.exists(file_path):
        with open(file_path, "w", newline='') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(["username", "password"])
            writer.writerow(["varshitha reddy", "varshi123"])
    return file_path


def read_login_data():
    file_path = ensure_login_data()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        return [(row['username'], row['password']) for row in reader]


# --------------------------- Demo / Helper Functions ---------------------------
def broken_links_check(driver):
    print("\n[Demo] Checking for broken links...")
    links = driver.find_elements(By.TAG_NAME, "a")
    print(f"Total links found: {len(links)}")
    for link in links:
        href = link.get_attribute("href")
        if href and href.startswith("http"):
            try:
                response = requests.head(href, timeout=5)
                assert response.status_code < 400, f"Broken link detected: {href}"
            except Exception as e:
                print(f"Error checking link: {href} -> {e}")
    print("[Demo] Broken links check completed.")


def navigation_commands_demo(driver):
    print("\n[Demo] Browser navigation commands...")
    driver.back()
    print("Navigated back.")
    time.sleep(1)
    driver.forward()
    print("Navigated forward.")
    time.sleep(1)
    driver.refresh()
    print("Refreshed page.")
    time.sleep(1)


def wait_for_element(driver, by, locator, timeout=10):
    wait = WebDriverWait(driver, timeout)
    return wait.until(EC.visibility_of_element_located((by, locator)))


# --------------------------- Test: Login ---------------------------
@pytest.mark.order(2)
@pytest.mark.parametrize("browser_name", ["chrome", "edge", "firefox"])
@pytest.mark.parametrize("username,password", read_login_data())
def test_login(browser_name, username, password):
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=False)
    driver.get("https://www.demoblaze.com")
    driver.maximize_window()
    print(f"\n=== Starting login test for {username} on {browser_name} ===")

    # 🔹 FEATURE 1: Broken Links Detection
    broken_links_check(driver)

    # 🔹 FEATURE 2: Navigation Commands
    driver.find_element(By.ID, "login2").click()
    print("Clicked on login button.")
    time.sleep(2)
    navigation_commands_demo(driver)

    # 🔹 FEATURE 3: Actual Login
    login_page = LoginPage(driver)
    login_page.open_login_modal()
    print("Opened login modal.")
    login_page.enter_username(username)
    print(f"Entered username: {username}")
    login_page.enter_password(password)
    print("Entered password.")
    login_page.click_login()
    print("Clicked login button.")

    # Wait for login success indicator
    try:
        wait_for_element(driver, By.ID, "nameofuser", 10)
        print("[Login] Login successful.")
    except:
        print("[Login] Login may have failed.")

    time.sleep(2)

    # 🔹 FEATURE 4: Refresh and verify
    driver.refresh()
    print("[Feature] Page refreshed post-login.")
    current_url = driver.current_url
    assert "demoblaze" in current_url, "Unexpected page after refresh."
    print("User is on expected page after refresh.")

    # 🔹 FEATURE 5: Logout
    if login_page.is_logged_in():
        driver.find_element(By.ID, "logout2").click()
        time.sleep(2)
        assert not login_page.is_logged_in(), "[Assertion] Logout failed!"
        print("User logged out successfully.")
    else:
        print("User was not logged in; skipping logout.")

    print(f"\n=== Login test executed successfully for user: {username} ===")
    driver.quit()
