import pytest
import csv
import os
import time
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from drivers.driver_factory import DriverFactory
from pages.signup_page import SignupPage


# -------------------- Data Setup --------------------
def ensure_signup_data():
    folder = os.path.join(os.getcwd(), "testdata")
    os.makedirs(folder, exist_ok=True)
    file_path = os.path.join(folder, "signup_data.csv")

    # overwrite with Ramya’s credentials
    with open(file_path, "w", newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["username", "password"])
        writer.writerow(["Ramya Hunagund", "ramya123"])
    return file_path


def read_signup_data():
    file_path = ensure_signup_data()
    with open(file_path, newline='') as csvfile:
        reader = csv.DictReader(csvfile)
        data = [(row['username'], row['password']) for row in reader]
    return data


# -------------------- Utility Demos --------------------
def webdriver_methods_demo(driver):
    """Basic WebDriver methods"""
    print("\n[Demo] WebDriver Methods:")
    print("Title:", driver.title)
    print("Current URL:", driver.current_url)
    print("Window Handle:", driver.current_window_handle)


def javascript_executor_demo(driver):
    """JavaScript executor demo"""
    print("\n[Demo] JavaScript Executor:")
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("→ Scrolled to bottom via JS")
    time.sleep(1)
    driver.execute_script("window.scrollTo(0, 0);")
    print("→ Scrolled back to top")


def mouse_hover_demo(driver):
    """Mouse hover demo"""
    print("\n[Demo] Mouse Hover on Categories:")
    actions = ActionChains(driver)
    categories = driver.find_elements(By.CSS_SELECTOR, ".list-group-item")
    for cat in categories:
        actions.move_to_element(cat).perform()
        print("Hovered on:", cat.text)
        time.sleep(0.4)


def window_handling_demo(driver):
    """Demonstrate window handling"""
    print("\n[Demo] Window Handling:")
    parent = driver.current_window_handle
    driver.execute_script("window.open('https://www.google.com');")
    time.sleep(1)
    all_windows = driver.window_handles
    for win in all_windows:
        if win != parent:
            driver.switch_to.window(win)
            print("Switched to new window:", driver.title)
            driver.close()
    driver.switch_to.window(parent)
    print("Returned to parent window.")


def alert_handling_demo(driver, wait):
    """Handle alerts if present"""
    try:
        alert = wait.until(EC.alert_is_present())
        print("Alert Text:", alert.text)
        alert.accept()
        print("Alert accepted.")
    except TimeoutException:
        print("No alert appeared.")


def screenshot_demo(driver, name="default_screenshot"):
    """Take and store screenshots in /screenshots folder"""
    folder = os.path.join(os.getcwd(), "screenshots")
    os.makedirs(folder, exist_ok=True)
    path = os.path.join(folder, f"{name}.png")
    driver.save_screenshot(path)
    print(f"Screenshot saved at: {path}")


# -------------------- Test Case --------------------
@pytest.mark.order(1)
@pytest.mark.parametrize("browser_name", ["chrome", "edge", "firefox"])
@pytest.mark.parametrize("username,password", read_signup_data())
def test_signup(browser_name, username, password):
    print(f"\n=== Starting signup test for user: {username} ===")
    driver = DriverFactory.get_driver(browser_name=browser_name, headless=True)
    driver.get("https://www.demoblaze.com")
    driver.maximize_window()
    wait = WebDriverWait(driver, 10)

    # --- Demo + Functional Flow ---
    webdriver_methods_demo(driver)
    mouse_hover_demo(driver)
    javascript_executor_demo(driver)

    print("\n[Feature] Opening signup modal...")
    signup_page = SignupPage(driver)
    signup_page.open_signup_modal()
    wait.until(EC.visibility_of_element_located((By.ID, "signInModal")))

    print(f"[Action] Entering signup details for user: {username}")
    signup_page.enter_signup_details(username, password)
    signup_page.submit_signup()
    time.sleep(3)

    alert_handling_demo(driver, wait)
    window_handling_demo(driver)
    screenshot_demo(driver, f"signup_{username.replace(' ', '_')}")

    driver.quit()
    print(f"=== Signup test completed for user: {username} ===\n")
