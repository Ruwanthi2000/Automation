import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

# Setup WebDriver
driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
driver.maximize_window()

# Test execution report
test_report = []

# Helper function to log results
def log_result(test_name, result, details=""):
    test_report.append({"Test Name": test_name, "Result": result, "Details": details})

# Open the form
driver.get("https://demoqa.com/automation-practice-form")
time.sleep(2)

# Close cookie banner (if present)
try:
    driver.find_element(By.ID, "close-fixedban").click()
except:
    pass

# Test Scenarios
try:
    # Test 1: Valid form submission
    try:
        driver.find_element(By.ID, "firstName").send_keys("Ruwanthi")
        driver.find_element(By.ID, "lastName").send_keys("Wathsala")
        driver.find_element(By.ID, "userEmail").send_keys("wathsala22dasanayaka@gmail.com")
        driver.find_element(By.CSS_SELECTOR, "label[for='gender-radio-1']").click()
        driver.find_element(By.ID, "userNumber").send_keys("0781866758")

        # Scroll into view and select hobbies
        element = driver.find_element(By.CSS_SELECTOR, "label[for='hobbies-checkbox-1']")
        driver.execute_script("arguments[0].scrollIntoView();", element)
        ActionChains(driver).move_to_element(element).click().perform()

        driver.find_element(By.ID, "submit").click()

        # Verify success modal
        success_message = driver.find_element(By.ID, "example-modal-sizes-title-lg").text
        assert "Thanks for submitting the form" in success_message
        log_result("Valid Form Submission", "PASS")
    except Exception as e:
        log_result("Valid Form Submission", "FAIL", str(e))

    time.sleep(2)
    driver.refresh()

    # Test 2: Submission with mandatory fields blank
    try:
        driver.find_element(By.ID, "submit").click()

        # Verify validation
        error_message = driver.find_element(By.CSS_SELECTOR, ".was-validated").is_displayed()
        assert error_message, "Validation error message not shown"
        log_result("Mandatory Fields Blank", "PASS")
    except Exception as e:
        log_result("Mandatory Fields Blank", "FAIL", str(e))

    time.sleep(2)
    driver.refresh()

    # Test 3: Invalid email format validation
    try:
        driver.find_element(By.ID, "firstName").send_keys("Ruwanthi")
        driver.find_element(By.ID, "lastName").send_keys("Wathsala")
        driver.find_element(By.ID, "userEmail").send_keys("invalid-email")
        driver.find_element(By.ID, "userNumber").send_keys("0781866758")
        driver.find_element(By.ID, "submit").click()

        # Verify email validation
        time.sleep(1)  # Allow time for validation to appear
        error_message = driver.find_element(By.XPATH, "//input[@id='userEmail']/following-sibling::div").text
        assert "Please enter a valid email" in error_message, "Email validation error message not shown"
        log_result("Invalid Email Format", "PASS")
    except Exception as e:
        log_result("Invalid Email Format", "FAIL", str(e))

finally:
    driver.quit()

# Generate Test Execution Report
print("\nTest Execution Report:")
for test in test_report:
    print(f"Test Name: {test['Test Name']}")
    print(f"Result: {test['Result']}")
    print(f"Details: {test['Details']}\n")
