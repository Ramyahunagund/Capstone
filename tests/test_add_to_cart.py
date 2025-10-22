import pytest
import time
from selenium.webdriver import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from pages.product_page import ProductPage
from pages.login_page import LoginPage

@pytest.mark.order(3)
def test_add_to_cart_advanced(logged_in_driver):
    driver = logged_in_driver
    wait = WebDriverWait(driver, 10)
    actions = ActionChains(driver)

    print("\n=== Starting Add to Cart Test (Advanced) ===")
    driver.get("https://www.demoblaze.com")
    driver.set_window_size(1366, 768)  # New: Set browser window size
    time.sleep(1)

    # 🔹 FEATURE 1: Navigation commands
    driver.refresh()
    print("[Navigation] Page refreshed")
    driver.get("https://www.demoblaze.com")
    driver.back()
    print("[Navigation] Back navigation")
    driver.forward()
    print("[Navigation] Forward navigation")
    time.sleep(1)

    # 🔹 FEATURE 2: List first 5 products using multiple_elements
    print("[Feature] Loading products...")
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, "#tbodyid .hrefch")))
    items = driver.find_elements(By.CSS_SELECTOR, "#tbodyid .hrefch")
    for i, item in enumerate(items[:5], start=1):
        print(f"  Product {i}: {item.text} | Displayed: {item.is_displayed()} | Enabled: {item.is_enabled()}")

    # 🔹 FEATURE 3: Open first product and use javascript_executor_demo for scrolling
    product_page = ProductPage(driver)
    product_page.open_product()
    driver.execute_script("window.scrollBy(0, 400);")
    print("[JS Executor] Scrolled 400px using JS")

    # 🔹 FEATURE 4: Add to Cart using alerts_demo
    product_page.add_to_cart()
    try:
        alert = wait.until(EC.alert_is_present())
        print(f"[Alert] Alert text: {alert.text}")
        alert.accept()
        print("[Alert] Accepted successfully")
    except:
        print("[Alert] No alert appeared")

    # 🔹 FEATURE 5: Mouse hover demo
    try:
        logo = driver.find_element(By.ID, "nava")
        actions.move_to_element(logo).perform()
        print("[Mouse Hover] Hovered over logo")
    except Exception as e:
        print("[Mouse Hover] Failed:", e)

    # 🔹 FEATURE 6: Double click demo
    try:
        actions.double_click(logo).perform()
        print("[Double Click] Performed on logo")
    except Exception as e:
        print("[Double Click] Failed:", e)

    # 🔹 FEATURE 7: Drag & drop demo
    try:
        actions.drag_and_drop_by_offset(logo, 30, 0).perform()
        print("[Drag & Drop] Drag performed on logo")
    except Exception as e:
        print("[Drag & Drop] Skipped:", e)

    # 🔹 FEATURE 8: Right click demo
    try:
        actions.context_click(logo).perform()
        print("[Right Click] Context click performed on logo")
    except Exception as e:
        print("[Right Click] Failed:", e)

    # 🔹 FEATURE 9: Window handling demo
    main_window = driver.current_window_handle
    driver.execute_script("window.open('https://www.demoblaze.com/about.html','_blank');")
    time.sleep(1)
    for win in driver.window_handles:
        if win != main_window:
            driver.switch_to.window(win)
            print("[Window Handling] Switched to About page")
            time.sleep(1)
            driver.close()
            print("[Window Handling] Closed About page window")
            break
    driver.switch_to.window(main_window)
    print("[Window Handling] Back to main window")

    # 🔹 FEATURE 10: Screenshot demo
    driver.save_screenshot("cart_page_screenshot.png")
    print("[Screenshot] Captured screenshot of main page")

    # 🔹 FEATURE 11: Scroll demo
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    print("[Scroll Demo] Scrolled to bottom of page")

    # 🔹 FEATURE 12: Go to Cart page
    cart_link = wait.until(EC.element_to_be_clickable((By.ID, "cartur")))
    cart_link.click()
    print("[Feature] Navigated to Cart page")

    print("✅ Add to Cart test executed with additional Selenium functions")
    print("=== Test Completed ===\n")
