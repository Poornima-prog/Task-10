# test_saucedemo.py

import pytest
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

@pytest.fixture
def driver():
    # Set up Chrome options for the browser (without headless mode for debugging)
    options = Options()
    # options.add_argument("--headless=new")  # Uncomment for headless mode
    driver = webdriver.Chrome(options=options)
    yield driver
    driver.quit()

# Positive Test Case: Valid Login
def test_valid_login(driver):
    # Test valid login credentials
    driver.get("https://www.saucedemo.com/")

    # Wait for the login page to load completely
    WebDriverWait(driver, 25).until(EC.presence_of_element_located((By.ID, "login-button")))

    # Enter username and password
    driver.find_element(By.ID, "user-name").send_keys("standard_user")
    driver.find_element(By.ID, "password").send_keys("secret_sauce")
    driver.find_element(By.ID, "login-button").click()

    # Wait for the inventory page to load and ensure we're redirected
    WebDriverWait(driver, 25).until(EC.url_contains("inventory"))

    # Assert the title and URL for successful login
    assert driver.title == "Swag Labs"
    assert "inventory" in driver.current_url

# Negative Test Case: Invalid Login
def test_invalid_login(driver):
    # Test invalid login credentials
    driver.get("https://www.saucedemo.com/")

    # Wait for the login page to load
    WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.ID, "login-button")))

    # Enter invalid credentials
    driver.find_element(By.ID, "user-name").send_keys("invalid_user")
    driver.find_element(By.ID, "password").send_keys("invalid_pass")
    driver.find_element(By.ID, "login-button").click()

    # Wait for the error message to appear
    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "error-message-container")))

    # Assert that the error message is displayed
    error_element = driver.find_element(By.CLASS_NAME, "error-message-container")
    assert error_element.is_displayed(), "Error message should be displayed for invalid login."
