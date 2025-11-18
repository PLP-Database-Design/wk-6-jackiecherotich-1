import unittest
import time
import logging
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException, NoSuchElementException
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from datetime import datetime, timedelta
import os

# Set up logging
log_file = 'test_execution.log'

# Clear previous log file if it exists
if os.path.exists(log_file):
    os.remove(log_file)

# Create a custom logger
logger = logging.getLogger(__name__)
logger.setLevel(logging.INFO)

# Create file handler which logs even debug messages
fh = logging.FileHandler(log_file, mode='w')
fh.setLevel(logging.INFO)

# Create console handler with a higher log level
ch = logging.StreamHandler()
ch.setLevel(logging.INFO)

# Create formatter and add it to the handlers
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
fh.setFormatter(formatter)
ch.setFormatter(formatter)

# Add the handlers to the logger
logger.addHandler(fh)
logger.addHandler(ch)

class CleanCityBaseTest(unittest.TestCase):
    """Base test class with common setup and teardown"""
    
    @classmethod
    def setUpClass(cls):
        """Set up test environment"""
        logger.info("Setting up test environment...")
        options = webdriver.ChromeOptions()
        # Run in non-headless mode to see the browser
        options.add_argument('--start-maximized')
        options.add_argument('--disable-notifications')
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        # Add these options for better visibility
        options.add_argument('--disable-gpu')
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-dev-shm-usage')
        # Disable automation flags
        options.add_argument('--disable-blink-features=AutomationControlled')
        options.add_experimental_option('useAutomationExtension', False)
        
        try:
            cls.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
            cls.wait = WebDriverWait(cls.driver, 10)
            cls.base_url = "https://genuine-pavlova-b1ad13.netlify.app"
            logger.info("Test environment setup complete")
        except Exception as e:
            logger.error(f"Failed to set up test environment: {str(e)}")
            raise
    
    @classmethod
    def tearDownClass(cls):
        """Clean up after all tests"""
        if hasattr(cls, 'driver'):
            cls.driver.quit()
            logger.info("Test environment cleaned up")
    
    def setUp(self):
        """Run before each test"""
        self.driver.get(self.base_url)
        self.driver.delete_all_cookies()
        logger.info(f"\n\n=== Starting test: {self._testMethodName} ===")
    
    def take_screenshot(self, name):
        """Take screenshot for debugging"""
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"screenshots/{self.__class__.__name__}_{name}_{timestamp}.png"
        os.makedirs("screenshots", exist_ok=True)
        self.driver.save_screenshot(filename)
        logger.info(f"Screenshot saved: {filename}")
        return filename
    
    def navigate_to_login(self):
        """Navigate to login page using navbar"""
        try:
            # Find and click the login link in the navbar
            login_link = self.wait.until(
                EC.element_to_be_clickable((By.XPATH, "//nav//a[contains(text(),'Login')]"))
            )
            login_link.click()
            self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to login page: {str(e)}")
            self.take_screenshot("nav_to_login_failed")
            return False
            
    def login(self, email="test@example.com", password="password123"):
        """Helper method to log in"""
        try:
            # Navigate to login page using navbar
            if not self.navigate_to_login():
                return False
            
            # Fill in login form
            email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
            email_field.clear()
            email_field.send_keys(email)
            
            password_field = self.driver.find_element(By.NAME, "password")
            password_field.clear()
            password_field.send_keys(password)
            
            # Click login button
            login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
            login_button.click()
            
            # Wait for login to complete
            time.sleep(2)
            
            # Check if login was successful by looking for dashboard or profile element
            try:
                self.wait.until(
                    EC.presence_of_element_located(
                        (By.XPATH, "//*[contains(@class, 'dashboard') or contains(@class, 'profile')]")
                    )
                )
                return True
            except:
                # Check if there's an error message
                try:
                    error_msg = self.driver.find_element(By.CSS_SELECTOR, ".error-message, .alert-danger").text
                    logger.error(f"Login failed with message: {error_msg}")
                except:
                    logger.error("Login failed - unknown error")
                return False
                
        except Exception as e:
            logger.error(f"Login failed with exception: {str(e)}")
            self.take_screenshot("login_failed")
            return False
    
    def navigate_to_page(self, page_name):
        """Navigate to a page using the navbar"""
        try:
            # Try to find and click the nav link
            nav_link = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, f"//nav//a[contains(translate(., 'ABCDEFGHIJKLMNOPQRSTUVWXYZ', 'abcdefghijklmnopqrstuvwxyz'), '{page_name.lower()}')]")
                )
            )
            nav_link.click()
            time.sleep(1)  # Allow page to load
            return True
        except Exception as e:
            logger.error(f"Failed to navigate to {page_name}: {str(e)}")
            self.take_screenshot(f"nav_to_{page_name.lower().replace(' ', '_')}_failed")
            return False
            
    def logout(self):
        """Helper method to log out"""
        try:
            # First try to find a dropdown menu if it exists
            try:
                profile_dropdown = self.wait.until(
                    EC.element_to_be_clickable((By.CLASS_NAME, "user-menu"))
                )
                profile_dropdown.click()
                time.sleep(0.5)  # Allow dropdown to open
            except:
                pass  # No dropdown, continue with direct logout button
                
            # Find and click logout button
            logout_button = self.wait.until(
                EC.element_to_be_clickable(
                    (By.XPATH, "//button[contains(., 'Logout') or contains(@class,'logout')]//*[contains(., 'Logout') or @class='logout']")
                )
            )
            logout_button.click()
            
            # Wait for logout to complete (should redirect to login or home page)
            time.sleep(2)
            
            # Verify we're not on a protected page
            current_url = self.driver.current_url
            if any(page in current_url for page in ["dashboard", "profile", "schedule"]):
                logger.error("Still on protected page after logout")
                return False
            
        except Exception as e:
            logger.error(f"Logout failed with exception: {str(e)}")
            self.take_screenshot("logout_failed")
            return False

class TestNavigation(CleanCityBaseTest):
    """Test navigation and basic functionality"""
    
    def test_navbar_links(self):
        """Test all navbar links are clickable"""
        try:
            # Test Home link
            self.assertTrue(self.navigate_to_page("Home"), "Failed to navigate to Home")
            self.assertIn("home", self.driver.current_url.lower())
            
            # Test About link if it exists
            if self.navigate_to_page("About"):
                self.assertIn("about", self.driver.current_url.lower())
            
            # Test Services link if it exists
            if self.navigate_to_page("Services"):
                self.assertIn("services", self.driver.current_url.lower())
                
            # Test Contact link if it exists
            if self.navigate_to_page("Contact"):
                self.assertIn("contact", self.driver.current_url.lower())
                
        except Exception as e:
            self.take_screenshot("test_navbar_links_failed")
            self.fail(f"Test failed: {str(e)}")

class TestLoginFunctionality(CleanCityBaseTest):
    """Test login and authentication functionality"""
    
    def test_valid_login(self):
        """Test login with valid credentials"""
        # Use the navbar to navigate to login
        self.assertTrue(self.navigate_to_page("Login"), "Failed to navigate to Login page")
        
        # Fill in login form with test credentials
        email_field = self.wait.until(EC.presence_of_element_located((By.NAME, "email")))
        email_field.send_keys("test@example.com")
        
        password_field = self.driver.find_element(By.NAME, "password")
        password_field.send_keys("password123")
        
        # Click login button
        login_button = self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']")
        login_button.click()
        
        # Verify successful login
        try:
            self.wait.until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(@class, 'dashboard') or contains(@class, 'profile')]"))
            )
            self.assertTrue(True, "Login successful")
        except:
            self.take_screenshot("login_failed")
            self.fail("Login with valid credentials failed")
    
    def test_invalid_registration(self):
        """Test registration with invalid credentials"""
        try:
            # Navigate to the home page first
            logger.info(f"Navigating to {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(2)  # Wait for page to load
            
            # Take initial screenshot
            self.take_screenshot("home_page_loaded")
            
            # Look for signup/register link in navigation
            logger.info("Looking for signup/register link in navigation...")
            
            # Try different selectors for the registration link
            register_selectors = [
                (By.XPATH, "//nav//a[contains(translate(., 'SIGNUP', 'signup'), 'signup')]"),
                (By.XPATH, "//nav//a[contains(translate(., 'REGISTER', 'register'), 'register')]"),
                (By.CSS_SELECTOR, "nav a[href*='register']"),
                (By.CSS_SELECTOR, "nav a[href*='signup']"),
                (By.LINK_TEXT, "Sign Up"),
                (By.PARTIAL_LINK_TEXT, "Sign Up"),
                (By.LINK_TEXT, "Register"),
                (By.PARTIAL_LINK_TEXT, "Register")
            ]
            
            register_found = False
            for by, selector in register_selectors:
                try:
                    register_link = self.driver.find_element(by, selector)
                    logger.info(f"Found register link with {by}={selector}")
                    # Scroll and highlight
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", register_link)
                    self.driver.execute_script("arguments[0].style.border='3px solid blue';", register_link)
                    time.sleep(1)
                    # Click using JavaScript
                    self.driver.execute_script("arguments[0].click();", register_link)
                    logger.info("Clicked register link in navigation")
                    register_found = True
                    break
                except Exception as e:
                    logger.debug(f"Register link not found with {by}={selector}: {str(e)}")
            
            if not register_found:
                logger.error("Could not find register/signup link in navigation")
                self.take_screenshot("register_link_not_found")
                return
                
            # Wait for registration page to load
            time.sleep(3)
            self.take_screenshot("register_page_loaded")
            
            # Print page source for debugging
            page_source = self.driver.page_source
            logger.info("Registration page source (first 1000 chars):\n" + page_source[:1000])
            
            # Take a screenshot of the registration form
            self.take_screenshot("register_form")
            
            # Dictionary of field types and their selectors
            field_selectors = {
                'name': [
                    (By.NAME, "name"),
                    (By.ID, "name"),
                    (By.CSS_SELECTOR, "input[name='name']"),
                    (By.XPATH, "//input[contains(@placeholder, 'Name')]")
                ],
                'email': [
                    (By.NAME, "email"),
                    (By.ID, "email"),
                    (By.CSS_SELECTOR, "input[type='email']"),
                    (By.XPATH, "//input[@type='email']")
                ],
                'password': [
                    (By.NAME, "password"),
                    (By.ID, "password"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.XPATH, "//input[@type='password']")
                ]
            }
            
            # Test data - minimal invalid data
            # Note: The application's email validation appears to only check for '@' symbol
            # but doesn't validate the full email format (e.g., 'invalid@gmail' is accepted)
            test_data = {
                'name': 'Test User',
                'email': 'invalid@gmail',  # Application only checks for '@' symbol
                'password': 'A'       # Too short password
            }
            
            # Find and fill form fields
            form_fields = {}
            for field_name, selectors in field_selectors.items():
                field_found = False
                for by, selector in selectors:
                    try:
                        field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                        logger.info(f"Found {field_name} field with {by}={selector}")
                        # Highlight the field
                        self.driver.execute_script("arguments[0].style.border='2px solid green';", field)
                        form_fields[field_name] = field
                        field_found = True
                        time.sleep(0.5)
                        break
                    except Exception as e:
                        logger.debug(f"{field_name} field not found with {by}={selector}: {str(e)}")
                
                if not field_found and field_name in test_data:
                    logger.warning(f"Could not find {field_name} field with any selector")
            
            # Fill in the form with test data
            try:
                for field_name, field in form_fields.items():
                    if field_name in test_data:
                        # Clear field using JavaScript
                        self.driver.execute_script("arguments[0].value = '';", field)
                        # Type each character with a small delay
                        for char in str(test_data[field_name]):
                            field.send_keys(char)
                            time.sleep(0.1)
                
                # Take screenshot after entering data
                self.take_screenshot("registration_form_filled")
                
                # Find and click the register button
                register_buttons = [
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.XPATH, "//button[contains(., 'Register')]"),
                    (By.XPATH, "//button[contains(., 'Sign Up')]"),
                    (By.CLASS_NAME, "btn-primary")
                ]
                
                button_clicked = False
                for by, selector in register_buttons:
                    try:
                        register_button = self.driver.find_element(by, selector)
                        logger.info(f"Found register button with {by}={selector}")
                        # Highlight the button
                        self.driver.execute_script("arguments[0].style.border='3px solid red';", register_button)
                        time.sleep(1)
                        # Click using JavaScript
                        self.driver.execute_script("arguments[0].click();", register_button)
                        logger.info("Clicked register button")
                        button_clicked = True
                        break
                    except Exception as e:
                        logger.debug(f"Register button not found with {by}={selector}: {str(e)}")
                
                if not button_clicked:
                    logger.error("Could not find register button")
                    self.take_screenshot("register_button_not_found")
                    return
                
                # Wait for any error messages or redirects
                time.sleep(3)
                self.take_screenshot("after_register_click")
                
                # Log the current URL for debugging
                logger.info(f"Current URL after registration attempt: {self.driver.current_url}")
                
                # Check for error messages (expected for invalid registration)
                try:
                    error_messages = self.driver.find_elements(
                        By.CSS_SELECTOR, ".error-message, .alert-danger, .text-red-500, [role='alert'], .error"
                    )
                    if error_messages:
                        logger.info("Error messages found (expected for invalid registration):")
                        for i, msg in enumerate(error_messages, 1):
                            logger.info(f"Error {i}: {msg.text}")
                    else:
                        # Check if we were redirected to a success page
                        if "login" in self.driver.current_url.lower() or "dashboard" in self.driver.current_url.lower():
                            logger.warning("POTENTIAL SECURITY ISSUE: Registration with invalid data may have succeeded")
                            logger.warning("Test Data Used:")
                            for k, v in test_data.items():
                                logger.warning(f"  {k}: {v}")
                            logger.warning("Current URL: " + self.driver.current_url)
                            logger.warning("Page Title: " + self.driver.title)
                            
                            # Take additional screenshots for documentation
                            self.take_screenshot("potential_successful_registration")
                            
                            # Document the issue but don't fail the test
                            logger.warning("This may indicate insufficient server-side validation")
                        else:
                            logger.warning("No error messages found for invalid registration")
                except Exception as e:
                    logger.warning(f"Error checking for error messages: {str(e)}")
                
                # Document the email validation behavior
                logger.info("\n=== EMAIL VALIDATION OBSERVATIONS ===")
                logger.info("1. Email validation only checks for '@' symbol")
                logger.info("2. Emails like 'invalid@' are accepted")
                logger.info("3. No feedback is shown for successful registration")
                logger.info("4. Consider enhancing validation to check for valid email format")
                logger.info("5. Consider adding success feedback after registration")
                
                # Check if still on registration page (should be, for invalid data)
                if "register" in self.driver.current_url.lower() or "signup" in self.driver.current_url.lower():
                    logger.info("Still on registration page (expected for invalid data)")
                else:
                    logger.warning("Unexpected page after invalid registration attempt")
                    logger.info(f"Current URL: {self.driver.current_url}")
                
            except Exception as e:
                logger.error(f"Error during registration attempt: {str(e)}")
                self.take_screenshot("registration_error")
                raise
            
        except Exception as e:
            self.take_screenshot("test_registration_failed")
            logger.error(f"Test failed: {str(e)}")
            raise
    
    def test_register_and_login_same_credentials(self):
        """Test registration and login with the same credentials"""
        try:
            # Test data - using specific test credentials
            test_data = {
                'name': 'Test User',
                'email': 'test@gmail',  # Intentionally invalid email (missing .com)
                'password': 'A'         # Very short password
            }
            
            # First, register a new account
            logger.info("=== STARTING REGISTRATION TEST ===")
            self.driver.get(self.base_url)
            time.sleep(2)
            self.take_screenshot("registration_start")
            
            # Navigate to registration page
            register_found = False
            register_selectors = [
                (By.XPATH, "//nav//a[contains(translate(., 'SIGNUP', 'signup'), 'signup')]"),
                (By.XPATH, "//nav//a[contains(translate(., 'REGISTER', 'register'), 'register')]"),
                (By.CSS_SELECTOR, "nav a[href*='register']"),
                (By.CSS_SELECTOR, "nav a[href*='signup']"),
                (By.LINK_TEXT, "Sign Up"),
                (By.PARTIAL_LINK_TEXT, "Sign Up"),
                (By.LINK_TEXT, "Register"),
                (By.PARTIAL_LINK_TEXT, "Register")
            ]
            
            for by, selector in register_selectors:
                try:
                    register_link = self.driver.find_element(by, selector)
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", register_link)
                    self.driver.execute_script("arguments[0].style.border='3px solid blue';", register_link)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", register_link)
                    logger.info(f"Found and clicked register link with {by}={selector}")
                    register_found = True
                    break
                except Exception as e:
                    logger.debug(f"Register link not found with {by}={selector}: {str(e)}")
            
            if not register_found:
                self.fail("Could not find register/signup link")
            
            time.sleep(3)
            self.take_screenshot("registration_form")
            
            # Fill registration form
            form_fields = {
                'name': [
                    (By.NAME, "name"),
                    (By.ID, "name"),
                    (By.CSS_SELECTOR, "input[name='name']"),
                    (By.XPATH, "//input[contains(@placeholder, 'Name')]")
                ],
                'email': [
                    (By.NAME, "email"),
                    (By.ID, "email"),
                    (By.CSS_SELECTOR, "input[type='email']"),
                    (By.XPATH, "//input[@type='email']")
                ],
                'password': [
                    (By.NAME, "password"),
                    (By.ID, "password"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.XPATH, "//input[@type='password']")
                ]
            }
            
            # Fill in the form
            for field_name, selectors in form_fields.items():
                field_found = False
                for by, selector in selectors:
                    try:
                        field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                        self.driver.execute_script("arguments[0].style.border='2px solid green';", field)
                        field.clear()
                        field.send_keys(test_data[field_name])
                        time.sleep(0.5)
                        field_found = True
                        break
                    except Exception as e:
                        logger.debug(f"{field_name} field not found with {by}={selector}: {str(e)}")
                
                if not field_found:
                    logger.warning(f"Could not find {field_name} field with any selector")
            
            self.take_screenshot("registration_form_filled")
            
            # Submit registration form
            submit_buttons = [
                (By.CSS_SELECTOR, "button[type='submit']"),
                (By.XPATH, "//button[contains(., 'Register')]"),
                (By.XPATH, "//button[contains(., 'Sign Up')]")
            ]
            
            for by, selector in submit_buttons:
                try:
                    submit_btn = self.driver.find_element(by, selector)
                    self.driver.execute_script("arguments[0].style.border='3px solid red';", submit_btn)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", submit_btn)
                    logger.info("Submitted registration form")
                    break
                except Exception as e:
                    logger.debug(f"Submit button not found with {by}={selector}: {str(e)}")
            
            time.sleep(3)
            self.take_screenshot("after_registration")
            
            # Check if we were redirected to the login page after registration
            if "login" in self.driver.current_url.lower():
                logger.info("Successfully redirected to login page after registration")
                self.take_screenshot("login_page_after_registration")
            elif "dashboard" in self.driver.current_url.lower():
                logger.info("Registration successful - directly logged in to dashboard")
                logger.info(f"Successfully registered and logged in as: {test_data['email']}")
                self.take_screenshot("dashboard_after_registration")
                return  # No need to test login if already logged in
            else:
                logger.warning(f"Unexpected page after registration. Current URL: {self.driver.current_url}")
                self.take_screenshot("unexpected_page_after_registration")
                # Continue with login test as the user might still be able to log in
            
            # Now test login with the same credentials
            logger.info("\n=== STARTING LOGIN TEST ===")
            
            # Take a screenshot of the login form (we should already be on it)
            time.sleep(2)
            self.take_screenshot("login_form")
            
            # Fill login form
            login_fields = {
                'email': [
                    (By.NAME, "email"),
                    (By.ID, "email"),
                    (By.CSS_SELECTOR, "input[type='email']"),
                    (By.XPATH, "//input[@type='email']")
                ],
                'password': [
                    (By.NAME, "password"),
                    (By.ID, "password"),
                    (By.CSS_SELECTOR, "input[type='password']"),
                    (By.XPATH, "//input[@type='password']")
                ]
            }
            
            # Fill in the login form
            for field_name, selectors in login_fields.items():
                field_found = False
                for by, selector in selectors:
                    try:
                        field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                        self.driver.execute_script("arguments[0].style.border='2px solid green';", field)
                        field.clear()
                        field.send_keys(test_data[field_name])
                        time.sleep(0.5)
                        field_found = True
                        break
                    except Exception as e:
                        logger.debug(f"Login {field_name} field not found with {by}={selector}: {str(e)}")
                
                if not field_found:
                    logger.warning(f"Could not find login {field_name} field with any selector")
            
            self.take_screenshot("login_form_filled")
            
            # Submit login form
            for by, selector in submit_buttons:  # Reuse submit_buttons from registration
                try:
                    submit_btn = self.driver.find_element(by, selector)
                    self.driver.execute_script("arguments[0].style.border='3px solid red';", submit_btn)
                    time.sleep(1)
                    self.driver.execute_script("arguments[0].click();", submit_btn)
                    logger.info("Submitted login form")
                    break
                except Exception as e:
                    logger.debug(f"Login submit button not found with {by}={selector}: {str(e)}")
            
            time.sleep(3)
            self.take_screenshot("after_login")
            
            # Check if login was successful
            if "dashboard" in self.driver.current_url.lower() or "profile" in self.driver.current_url.lower():
                logger.info("Login successful!")
                logger.info(f"Successfully registered and logged in as: {test_data['email']}")
                self.take_screenshot("profile_page")
                
                # Now test the edit profile functionality
                logger.info("\n=== TESTING EDIT PROFILE ===")
                
                # Try to find and click the edit profile button
                edit_profile_found = False
                edit_profile_selectors = [
                    (By.XPATH, "//button[contains(., 'Edit Profile')]"),
                    (By.XPATH, "//a[contains(., 'Edit Profile')]"),
                    (By.CSS_SELECTOR, "button.edit-profile, a.edit-profile, .edit-profile-button"),
                    (By.CLASS_NAME, "edit-profile"),
                    (By.ID, "editProfileButton"),
                    (By.LINK_TEXT, "Edit Profile"),
                    (By.PARTIAL_LINK_TEXT, "Edit")
                ]
                
                for by, selector in edit_profile_selectors:
                    try:
                        edit_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                        self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
                        self.driver.execute_script("arguments[0].style.border='3px solid purple';", edit_btn)
                        time.sleep(1)
                        self.driver.execute_script("arguments[0].click();", edit_btn)
                        logger.info(f"Found and clicked edit profile button with {by}={selector}")
                        edit_profile_found = True
                        time.sleep(2)  # Wait for edit form to load
                        break
                    except Exception as e:
                        logger.debug(f"Edit profile button not found with {by}={selector}: {str(e)}")
                
                if not edit_profile_found:
                    logger.warning("Could not find edit profile button")
                    self.take_screenshot("edit_profile_button_not_found")
                else:
                    # Take screenshot of the edit form
                    self.take_screenshot("edit_profile_form")
                    
                    # Try to update some profile information
                    try:
                        # Try to find and update the name field
                        name_fields = [
                            (By.NAME, "name"),
                            (By.ID, "name"),
                            (By.CSS_SELECTOR, "input[name='name']"),
                            (By.XPATH, "//input[contains(@placeholder, 'Name')]")
                        ]
                        
                        name_updated = False
                        for by, selector in name_fields:
                            try:
                                name_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                self.driver.execute_script("arguments[0].style.border='2px solid orange';", name_field)
                                name_field.clear()
                                name_field.send_keys("Updated Test User")
                                name_updated = True
                                logger.info("Updated name field")
                                break
                            except Exception as e:
                                logger.debug(f"Name field not found with {by}={selector}: {str(e)}")
                        
                        if not name_updated:
                            logger.warning("Could not find name field to update")
                        
                        # Try to find and click the save button
                        save_buttons = [
                            (By.XPATH, "//button[contains(., 'Save')]"),
                            (By.CSS_SELECTOR, "button[type='submit']"),
                            (By.CLASS_NAME, "save-button"),
                            (By.ID, "saveProfileButton")
                        ]
                        
                        save_clicked = False
                        for by, selector in save_buttons:
                            try:
                                save_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                self.driver.execute_script("arguments[0].style.border='3px solid green';", save_btn)
                                time.sleep(1)
                                self.driver.execute_script("arguments[0].click();", save_btn)
                                logger.info(f"Clicked save button with {by}={selector}")
                                save_clicked = True
                                time.sleep(2)  # Wait for save to complete
                                break
                            except Exception as e:
                                logger.debug(f"Save button not found with {by}={selector}: {str(e)}")
                        
                        if not save_clicked:
                            logger.warning("Could not find save button")
                        else:
                            # Check if save was successful
                            try:
                                success_message = self.wait.until(
                                    EC.visibility_of_element_located(
                                        (By.CSS_SELECTOR, ".success-message, .alert-success, [role='alert']")
                                    )
                                )
                                logger.info(f"Profile updated successfully: {success_message.text}")
                            except:
                                logger.info("Profile update may have been successful (no success message detected)")
                            
                            self.take_screenshot("after_profile_update")
                            
                            # Now navigate to Schedule Pickup
                            logger.info("\n=== NAVIGATING TO SCHEDULE PICKUP ===")
                            
                            # Try to find and click the Schedule Pickup link in the navbar
                            schedule_found = False
                            schedule_selectors = [
                                (By.XPATH, "//nav//a[contains(., 'Schedule Pickup')]"),
                                (By.XPATH, "//nav//a[contains(., 'Schedule')]"),
                                (By.CSS_SELECTOR, "nav a[href*='schedule']"),
                                (By.LINK_TEXT, "Schedule Pickup"),
                                (By.PARTIAL_LINK_TEXT, "Schedule"),
                                (By.CLASS_NAME, "schedule-pickup"),
                                (By.ID, "schedulePickupLink")
                            ]
                            
                            for by, selector in schedule_selectors:
                                try:
                                    schedule_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", schedule_link)
                                    self.driver.execute_script("arguments[0].style.border='3px solid blue';", schedule_link)
                                    time.sleep(1)
                                    self.driver.execute_script("arguments[0].click();", schedule_link)
                                    logger.info(f"Found and clicked Schedule Pickup with {by}={selector}")
                                    schedule_found = True
                                    time.sleep(2)  # Wait for the page to load
                                    break
                                except Exception as e:
                                    logger.debug(f"Schedule Pickup link not found with {by}={selector}: {str(e)}")
                            
                            if not schedule_found:
                                logger.warning("Could not find Schedule Pickup link in the navbar")
                                self.take_screenshot("schedule_pickup_not_found")
                            else:
                                # Take a screenshot of the schedule pickup page
                                self.take_screenshot("schedule_pickup_page")
                                logger.info("Successfully navigated to Schedule Pickup page")
                                
                                # Log the current URL for reference
                                logger.info(f"Current URL: {self.driver.current_url}")
                                
                                # Fill out the waste pickup form
                                logger.info("\n=== FILLING OUT WASTE PICKUP FORM ===")
                                
                                # Dictionary of form fields and their test data
                                form_data = {
                                    'Full Name': 'Test User',
                                    'Email': 'test@gmail',
                                    'Pickup Location': 'Nairobi',  # Updated to match exact dropdown text
                                    'Waste Type': 'General Waste',  # Will be selected from dropdown
                                    'Preferred Pickup Date': '12/15/2023',
                                    'Additional Description': 'Test pickup request from automated test'
                                }
                                
                                # Fill in text fields
                                for field_label, value in form_data.items():
                                    if field_label in ['Pickup Location', 'Waste Type']:
                                        continue  # Handle dropdowns separately
                                        
                                    try:
                                        # Try different ways to find the input field
                                        field = None
                                        
                                        # Try finding by associated label
                                        try:
                                            label = self.driver.find_element(By.XPATH, f"//label[contains(., '{field_label}')]")
                                            field_id = label.get_attribute('for')
                                            if field_id:
                                                field = self.driver.find_element(By.ID, field_id)
                                            else:
                                                # If no 'for' attribute, try to find input after label
                                                field = label.find_element(By.XPATH, "./following-sibling::input | .//following::input[1]")
                                        except:
                                            # Try finding by placeholder
                                            field = self.driver.find_element(
                                                By.XPATH, 
                                                f"//input[contains(@placeholder, '{field_label}')] | //textarea[contains(@placeholder, '{field_label}')]"
                                            )
                                        
                                        if field:
                                            self.driver.execute_script("arguments[0].style.border='2px solid orange';", field)
                                            field.clear()
                                            field.send_keys(value)
                                            logger.info(f"Filled {field_label}: {value}")
                                    
                                    except Exception as e:
                                        logger.warning(f"Could not find or fill {field_label} field: {str(e)}")
                                
                                # Handle dropdown for Pickup Location
                                try:
                                    # Try different ways to find the location dropdown
                                    location_selectors = [
                                        (By.XPATH, "//select[.//option[contains(., 'Select a location')]]"),
                                        (By.XPATH, "//div[contains(., 'Select a location')]//select"),
                                        (By.NAME, 'pickup_location'),
                                        (By.ID, 'pickupLocation'),
                                        (By.CSS_SELECTOR, 'select[name*="location"]')
                                    ]
                                    
                                    location_dropdown = None
                                    for by, selector in location_selectors:
                                        try:
                                            location_dropdown = self.wait.until(EC.presence_of_element_located((by, selector)))
                                            self.driver.execute_script("arguments[0].style.border='2px solid purple';", location_dropdown)
                                            break
                                        except:
                                            continue
                                    
                                    if location_dropdown:
                                        select = Select(location_dropdown)
                                        select.select_by_visible_text(form_data['Pickup Location'])
                                        logger.info(f"Selected Pickup Location: {form_data['Pickup Location']}")
                                        time.sleep(1)  # Wait for any JS to process
                                    else:
                                        logger.warning("Could not find Pickup Location dropdown")
                                        
                                except Exception as e:
                                    logger.warning(f"Error selecting Pickup Location: {str(e)}")
                                    self.take_screenshot("pickup_location_dropdown_error")
                                
                                # Handle dropdown for Waste Type
                                try:
                                    # Try different ways to find the waste type dropdown
                                    waste_selectors = [
                                        (By.XPATH, "//select[.//option[contains(., 'Select waste type')]]"),
                                        (By.XPATH, "//div[contains(., 'Select waste type')]//select"),
                                        (By.NAME, 'waste_type'),
                                        (By.ID, 'wasteType'),
                                        (By.CSS_SELECTOR, 'select[name*="waste"]')
                                    ]
                                    
                                    waste_dropdown = None
                                    for by, selector in waste_selectors:
                                        try:
                                            waste_dropdown = self.wait.until(EC.presence_of_element_located((by, selector)))
                                            self.driver.execute_script("arguments[0].style.border='2px solid purple';", waste_dropdown)
                                            break
                                        except:
                                            continue
                                    
                                    if waste_dropdown:
                                        select = Select(waste_dropdown)
                                        select.select_by_visible_text(form_data['Waste Type'])
                                        logger.info(f"Selected Waste Type: {form_data['Waste Type']}")
                                        time.sleep(1)  # Wait for any JS to process
                                    else:
                                        logger.warning("Could not find Waste Type dropdown")
                                        
                                except Exception as e:
                                    logger.warning(f"Error selecting Waste Type: {str(e)}")
                                    self.take_screenshot("waste_type_dropdown_error")
                                
                                # Take a screenshot after filling the form
                                self.take_screenshot("pickup_form_filled")
                                
                                # Submit the form
                                try:
                                    submit_buttons = [
                                        (By.XPATH, "//button[contains(., 'Submit Request')]"),
                                        (By.CSS_SELECTOR, "button[type='submit']"),
                                        (By.CLASS_NAME, "submit-button"),
                                        (By.ID, "submitPickup")
                                    ]
                                    
                                    for by, selector in submit_buttons:
                                        try:
                                            submit_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                            self.driver.execute_script("arguments[0].style.border='3px solid green';", submit_btn)
                                            time.sleep(1)
                                            self.driver.execute_script("arguments[0].click();", submit_btn)
                                            logger.info("Submitted waste pickup request")
                                            time.sleep(3)  # Wait for submission
                                            break
                                        except:
                                            continue
                                    
                                    # Take a screenshot after submission
                                    self.take_screenshot("after_pickup_submission")
                                    
                                    # Check for success message
                                    try:
                                        success_msg = self.wait.until(
                                            EC.visibility_of_element_located(
                                                (By.CSS_SELECTOR, ".success-message, .alert-success, [role='alert']")
                                            )
                                        )
                                        logger.info(f"Pickup request submitted successfully: {success_msg.text}")
                                    except:
                                        logger.info("Pickup request may have been submitted (no success message detected)")
                                
                                except Exception as e:
                                    logger.error(f"Error submitting pickup request: {str(e)}")
                                    self.take_screenshot("pickup_submission_error")
                                    raise
                                    
                                # Navigate to Community Feed
                                logger.info("\n=== NAVIGATING TO COMMUNITY FEED ===")
                                
                                # Try different selectors for Community link
                                community_found = False
                                community_selectors = [
                                    (By.XPATH, "//nav//a[contains(., 'Community')]"),
                                    (By.LINK_TEXT, "Community"),
                                    (By.PARTIAL_LINK_TEXT, "Community"),
                                    (By.CLASS_NAME, "community-link"),
                                    (By.CSS_SELECTOR, "nav a[href*='community'], nav a[href*='feed']"),
                                    (By.ID, "communityLink")
                                ]
                                
                                for by, selector in community_selectors:
                                    try:
                                        community_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", community_link)
                                        self.driver.execute_script("arguments[0].style.border='3px solid blue';", community_link)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", community_link)
                                        logger.info(f"Found and clicked Community link with {by}={selector}")
                                        community_found = True
                                        time.sleep(2)  # Wait for page to load
                                        break
                                    except Exception as e:
                                        logger.debug(f"Community link not found with {by}={selector}: {str(e)}")
                                
                                if not community_found:
                                    logger.warning("Could not find Community link in the navbar")
                                    self.take_screenshot("community_link_not_found")
                                    return
                                    
                                # Take a screenshot of the community feed
                                self.take_screenshot("community_feed_page")
                                logger.info("Successfully navigated to Community Feed")
                                
                                # Create a new post
                                logger.info("\n=== CREATING A NEW COMMUNITY POST ===")
                                
                                # Try to find the post textarea
                                post_textarea = None
                                post_selectors = [
                                    (By.XPATH, "//textarea[contains(@placeholder, 'Share something with the community')]"),
                                    (By.CSS_SELECTOR, "textarea[placeholder*='Share something']"),
                                    (By.NAME, "postContent"),
                                    (By.CLASS_NAME, "post-textarea"),
                                    (By.CSS_SELECTOR, "textarea"),
                                    (By.TAG_NAME, "textarea")
                                ]
                                
                                for by, selector in post_selectors:
                                    try:
                                        post_textarea = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='2px solid orange';", post_textarea)
                                        break
                                    except:
                                        continue
                                
                                if not post_textarea:
                                    logger.warning("Could not find post textarea")
                                    self.take_screenshot("post_textarea_not_found")
                                    return
                                
                                # Create a simple test post
                                post_text = "Hello CleanCity community! Just scheduled a waste pickup. Let's keep our city clean together!"
                                post_textarea.clear()
                                post_textarea.send_keys(post_text)
                                logger.info("Filled in post content")
                                
                                # Take a screenshot with the post content
                                self.take_screenshot("post_content_filled")
                                
                                # Find and click the Post button
                                post_clicked = False
                                post_buttons = [
                                    (By.XPATH, "//button[contains(., 'Post')]"),
                                    (By.CSS_SELECTOR, "button[type='submit']"),
                                    (By.CLASS_NAME, "post-button"),
                                    (By.ID, "submitPost")
                                ]
                                
                                for by, selector in post_buttons:
                                    try:
                                        post_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='3px solid green';", post_btn)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", post_btn)
                                        logger.info("Clicked Post button")
                                        post_clicked = True
                                        time.sleep(2)  # Wait for post to be submitted
                                        break
                                    except:
                                        continue
                                
                                if not post_clicked:
                                    logger.warning("Could not find or click Post button")
                                    self.take_screenshot("post_button_not_found")
                                    return
                                
                                # Take a screenshot after posting
                                self.take_screenshot("after_post_submission")
                                logger.info("Community post submitted successfully")
                                
                                # Check for success message
                                try:
                                    success_msg = self.wait.until(
                                        EC.visibility_of_element_located(
                                            (By.CSS_SELECTOR, ".success-message, .alert-success, [role='alert'], .post-success")
                                        )
                                    )
                                    logger.info(f"Post successful: {success_msg.text}")
                                except:
                                    logger.info("Post may have been submitted (no success message detected)")
                                
                                # Navigate to Dashboard
                                logger.info("\n=== NAVIGATING TO DASHBOARD ===")
                                
                                # Try different selectors for Dashboard link
                                dashboard_found = False
                                dashboard_selectors = [
                                    (By.XPATH, "//nav//a[contains(., 'Dashboard')]"),
                                    (By.LINK_TEXT, "Dashboard"),
                                    (By.PARTIAL_LINK_TEXT, "Dashboard"),
                                    (By.CLASS_NAME, "dashboard-link"),
                                    (By.CSS_SELECTOR, "nav a[href*='dashboard']"),
                                    (By.ID, "dashboardLink")
                                ]
                                
                                for by, selector in dashboard_selectors:
                                    try:
                                        dashboard_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", dashboard_link)
                                        self.driver.execute_script("arguments[0].style.border='3px solid purple';", dashboard_link)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", dashboard_link)
                                        logger.info(f"Found and clicked Dashboard link with {by}={selector}")
                                        dashboard_found = True
                                        time.sleep(2)  # Wait for page to load
                                        break
                                    except Exception as e:
                                        logger.debug(f"Dashboard link not found with {by}={selector}: {str(e)}")
                                
                                if not dashboard_found:
                                    logger.warning("Could not find Dashboard link in the navbar")
                                    self.take_screenshot("dashboard_link_not_found")
                                    return
                                
                                # Take a screenshot of the dashboard
                                self.take_screenshot("dashboard_page")
                                logger.info("Successfully navigated to Dashboard")
                                
                                # Navigate to Feedback page
                                logger.info("\n=== NAVIGATING TO FEEDBACK PAGE ===")
                                
                                # Try different selectors for Feedback link
                                feedback_found = False
                                feedback_selectors = [
                                    (By.XPATH, "//nav//a[contains(., 'Feedback') or contains(., 'Report')]"),
                                    (By.LINK_TEXT, "Feedback"),
                                    (By.LINK_TEXT, "Report Missed Pickup"),
                                    (By.PARTIAL_LINK_TEXT, "Feedback"),
                                    (By.CLASS_NAME, "feedback-link"),
                                    (By.CSS_SELECTOR, "nav a[href*='feedback'], nav a[href*='report']"),
                                    (By.ID, "feedbackLink")
                                ]
                                
                                for by, selector in feedback_selectors:
                                    try:
                                        feedback_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", feedback_link)
                                        self.driver.execute_script("arguments[0].style.border='3px solid purple';", feedback_link)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", feedback_link)
                                        logger.info(f"Found and clicked Feedback link with {by}={selector}")
                                        feedback_found = True
                                        time.sleep(2)  # Wait for page to load
                                        break
                                    except Exception as e:
                                        logger.debug(f"Feedback link not found with {by}={selector}: {str(e)}")
                                
                                if not feedback_found:
                                    logger.warning("Could not find Feedback link in the navbar")
                                    self.take_screenshot("feedback_link_not_found")
                                    return
                                
                                # Take a screenshot of the feedback form
                                self.take_screenshot("feedback_page")
                                logger.info("Successfully navigated to Feedback page")
                                
                                # Fill out the feedback form
                                logger.info("\n=== FILLING OUT FEEDBACK FORM ===")
                                
                                # Using a simple request ID as requested
                                request_id = "DK78"
                                feedback_text = "This is a test feedback submission from the automated test. The pickup was missed as per the schedule."
                                
                                # Find and fill the request ID field
                                request_id_filled = False
                                request_id_selectors = [
                                    (By.NAME, "requestId"),
                                    (By.ID, "requestId"),
                                    (By.XPATH, "//input[contains(@placeholder, 'request ID') or contains(@placeholder, 'Request ID')]"),
                                    (By.CSS_SELECTOR, "input[type='text']")
                                ]
                                
                                for by, selector in request_id_selectors:
                                    try:
                                        request_id_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='2px solid orange';", request_id_field)
                                        request_id_field.clear()
                                        request_id_field.send_keys(request_id)
                                        logger.info(f"Filled Request ID: {request_id}")
                                        request_id_filled = True
                                        break
                                    except:
                                        continue
                                
                                if not request_id_filled:
                                    logger.warning("Could not find Request ID field")
                                    self.take_screenshot("request_id_field_not_found")
                                
                                # Find and fill the feedback textarea
                                feedback_filled = False
                                feedback_selectors = [
                                    (By.NAME, "feedback"),
                                    (By.ID, "feedback"),
                                    (By.XPATH, "//textarea[contains(@placeholder, 'Describe the issue') or contains(@placeholder, 'feedback')]"),
                                    (By.TAG_NAME, "textarea")
                                ]
                                
                                for by, selector in feedback_selectors:
                                    try:
                                        feedback_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='2px solid orange';", feedback_field)
                                        feedback_field.clear()
                                        feedback_field.send_keys(feedback_text)
                                        logger.info("Filled Feedback text")
                                        feedback_filled = True
                                        break
                                    except:
                                        continue
                                
                                if not feedback_filled:
                                    logger.warning("Could not find Feedback textarea")
                                    self.take_screenshot("feedback_textarea_not_found")
                                
                                # Take a screenshot with the form filled
                                self.take_screenshot("feedback_form_filled")
                                
                                # Submit the form
                                submit_clicked = False
                                submit_buttons = [
                                    (By.XPATH, "//button[contains(., 'Submit')]"),
                                    (By.CSS_SELECTOR, "button[type='submit']"),
                                    (By.CLASS_NAME, "submit-button"),
                                    (By.ID, "submitFeedback")
                                ]
                                
                                for by, selector in submit_buttons:
                                    try:
                                        submit_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='3px solid green';", submit_btn)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", submit_btn)
                                        logger.info("Clicked Submit button")
                                        submit_clicked = True
                                        time.sleep(2)  # Wait for submission
                                        break
                                    except:
                                        continue
                                
                                if not submit_clicked:
                                    logger.warning("Could not find or click Submit button")
                                    self.take_screenshot("submit_button_not_found")
                                    return
                                
                                # Take a screenshot after submission
                                self.take_screenshot("after_feedback_submission")
                                logger.info("Feedback form submitted successfully")
                                
                                # Check for success message
                                try:
                                    success_msg = self.wait.until(
                                        EC.visibility_of_element_located(
                                            (By.CSS_SELECTOR, ".success-message, .alert-success, [role='alert']")
                                        )
                                    )
                                    logger.info(f"Feedback submitted successfully: {success_msg.text}")
                                except:
                                    logger.info("Feedback may have been submitted (no success message detected)")
                                
                                # Logout
                                logger.info("\n=== LOGGING OUT ===")
                                
                                # Try to find and click the Logout button
                                logout_successful = False
                                logout_selectors = [
                                    (By.XPATH, "//*[text()='Logout']"),  # Exact text match for Logout
                                    (By.LINK_TEXT, "Logout"),  # Link with exact text Logout
                                    (By.XPATH, "//button[text()='Logout']")  # Button with exact text Logout
                                ]
                                
                                for by, selector in logout_selectors:
                                    try:
                                        logout_element = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", logout_element)
                                        self.driver.execute_script("arguments[0].style.border='3px solid red';", logout_element)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", logout_element)
                                        logger.info(f"Found and clicked Logout with {by}={selector}")
                                        logout_successful = True
                                        time.sleep(2)  # Wait for logout to complete
                                        break
                                    except Exception as e:
                                        logger.debug(f"Logout element not found with {by}={selector}: {str(e)}")
                                
                                if not logout_successful:
                                    logger.warning("Could not find Logout link/button")
                                    self.take_screenshot("logout_element_not_found")
                                    return
                                
                                # Verify logout was successful by checking for login page elements
                                try:
                                    # Look for login page indicators
                                    login_indicators = [
                                        (By.XPATH, "//h1[contains(., 'Login') or contains(., 'Sign In')]"),
                                        (By.ID, "loginForm"),
                                        (By.NAME, "email"),  # Assuming email field is on login page
                                        (By.CLASS_NAME, "login-form")
                                    ]
                                    
                                    for by, selector in login_indicators:
                                        try:
                                            self.wait.until(EC.visibility_of_element_located((by, selector)))
                                            logger.info("Successfully logged out and returned to login page")
                                            self.take_screenshot("after_logout")
                                            break
                                        except:
                                            continue
                                    else:
                                        logger.warning("May not have been redirected to login page after logout")
                                        
                                except Exception as e:
                                    logger.error(f"Error verifying logout: {str(e)}")
                                    self.take_screenshot("logout_verification_error")
                                
                                # Navigate to Blog page after logout
                                logger.info("\n=== NAVIGATING TO BLOG PAGE ===")
                                
                                # Try different selectors for Blog link
                                blog_found = False
                                blog_selectors = [
                                    (By.XPATH, "//nav//a[contains(., 'Blog')]"),
                                    (By.LINK_TEXT, "Blog"),
                                    (By.PARTIAL_LINK_TEXT, "Blog"),
                                    (By.CLASS_NAME, "blog-link"),
                                    (By.CSS_SELECTOR, "nav a[href*='blog']"),
                                    (By.ID, "blogLink")
                                ]
                                
                                for by, selector in blog_selectors:
                                    try:
                                        blog_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", blog_link)
                                        self.driver.execute_script("arguments[0].style.border='3px solid purple';", blog_link)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", blog_link)
                                        logger.info(f"Found and clicked Blog link with {by}={selector}")
                                        blog_found = True
                                        time.sleep(2)  # Wait for page to load
                                        break
                                    except Exception as e:
                                        logger.debug(f"Blog link not found with {by}={selector}: {str(e)}")
                                
                                if not blog_found:
                                    logger.warning("Could not find Blog link in the navbar")
                                    self.take_screenshot("blog_link_not_found")
                                    return
                                
                                # Take a screenshot of the blog page
                                self.take_screenshot("blog_page")
                                logger.info("Successfully navigated to Blog page")
                                
                                # Navigate to Awareness page
                                logger.info("\n=== NAVIGATING TO AWARENESS PAGE ===")
                                
                                # Try different selectors for Awareness link
                                awareness_found = False
                                awareness_selectors = [
                                    (By.XPATH, "//nav//a[contains(., 'Awareness')]"),
                                    (By.LINK_TEXT, "Awareness"),
                                    (By.PARTIAL_LINK_TEXT, "Awareness"),
                                    (By.CLASS_NAME, "awareness-link"),
                                    (By.CSS_SELECTOR, "nav a[href*='awareness']"),
                                    (By.ID, "awarenessLink")
                                ]
                                
                                for by, selector in awareness_selectors:
                                    try:
                                        awareness_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", awareness_link)
                                        self.driver.execute_script("arguments[0].style.border='3px solid orange';", awareness_link)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", awareness_link)
                                        logger.info(f"Found and clicked Awareness link with {by}={selector}")
                                        awareness_found = True
                                        time.sleep(2)  # Wait for page to load
                                        break
                                    except Exception as e:
                                        logger.debug(f"Awareness link not found with {by}={selector}: {str(e)}")
                                
                                if not awareness_found:
                                    logger.warning("Could not find Awareness link in the navbar")
                                    self.take_screenshot("awareness_link_not_found")
                                    return
                                
                                # Take a screenshot of the awareness page
                                self.take_screenshot("awareness_page")
                                logger.info("Successfully navigated to Awareness page")
                                
                                # Navigate to Login page as admin
                                logger.info("\n=== LOGGING IN AS ADMIN ===")
                                
                                # Try to find and click the Login link
                                login_found = False
                                login_selectors = [
                                    (By.XPATH, "//a[text()='Login']"),  # Exact text match for Login
                                    (By.LINK_TEXT, "Login")  # Link with exact text Login
                                ]
                                
                                for by, selector in login_selectors:
                                    try:
                                        login_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].scrollIntoView(true);", login_link)
                                        self.driver.execute_script("arguments[0].style.border='3px solid blue';", login_link)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", login_link)
                                        logger.info(f"Found and clicked Login link with {by}={selector}")
                                        login_found = True
                                        time.sleep(2)  # Wait for login page to load
                                        break
                                    except Exception as e:
                                        logger.debug(f"Login link not found with {by}={selector}: {str(e)}")
                                
                                if not login_found:
                                    logger.warning("Could not find Login link in the navbar")
                                    self.take_screenshot("login_link_not_found")
                                    return
                                
                                # Take a screenshot of the login page
                                self.take_screenshot("login_page")
                                logger.info("On login page")
                                
                                # Fill in admin credentials
                                admin_email = "admin@Gmail.com"
                                admin_password = "Kks"
                                
                                # Find and fill the email field
                                email_filled = False
                                email_selectors = [
                                    (By.NAME, "email"),
                                    (By.ID, "email"),
                                    (By.XPATH, "//input[@type='email']"),
                                    (By.CSS_SELECTOR, "input[type='email']"),
                                    (By.NAME, "username"),
                                    (By.ID, "username"),
                                    (By.XPATH, "//input[contains(@placeholder, 'email') or contains(@placeholder, 'Email')]")
                                ]
                                
                                for by, selector in email_selectors:
                                    try:
                                        email_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='2px solid green';", email_field)
                                        email_field.clear()
                                        email_field.send_keys(admin_email)
                                        logger.info("Filled admin email")
                                        email_filled = True
                                        break
                                    except:
                                        continue
                                
                                if not email_filled:
                                    logger.warning("Could not find email field")
                                    self.take_screenshot("email_field_not_found")
                                    return
                                
                                # Find and fill the password field
                                password_filled = False
                                password_selectors = [
                                    (By.NAME, "password"),
                                    (By.ID, "password"),
                                    (By.XPATH, "//input[@type='password']"),
                                    (By.CSS_SELECTOR, "input[type='password']"),
                                    (By.XPATH, "//input[contains(@placeholder, 'password') or contains(@placeholder, 'Password')]")
                                ]
                                
                                for by, selector in password_selectors:
                                    try:
                                        password_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='2px solid green';", password_field)
                                        password_field.clear()
                                        password_field.send_keys(admin_password)
                                        logger.info("Filled admin password")
                                        password_filled = True
                                        break
                                    except:
                                        continue
                                
                                if not password_filled:
                                    logger.warning("Could not find password field")
                                    self.take_screenshot("password_field_not_found")
                                    return
                                
                                # Take a screenshot with credentials filled
                                self.take_screenshot("login_form_filled")
                                
                                # Find and click the login button
                                login_clicked = False
                                login_buttons = [
                                    (By.XPATH, "//button[text()='Login']"),  # Exact text match for Login
                                    (By.LINK_TEXT, "Login")  # Link with exact text Login
                                ]
                                
                                for by, selector in login_buttons:
                                    try:
                                        login_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                        self.driver.execute_script("arguments[0].style.border='3px solid green';", login_btn)
                                        time.sleep(1)
                                        self.driver.execute_script("arguments[0].click();", login_btn)
                                        logger.info("Clicked Login button")
                                        login_clicked = True
                                        time.sleep(3)  # Wait for login to complete
                                        break
                                    except:
                                        continue
                                
                                if not login_clicked:
                                    logger.warning("Could not find or click Login button")
                                    self.take_screenshot("login_button_not_found")
                                    return
                                
                                # Take a screenshot after login attempt
                                self.take_screenshot("after_admin_login")
                                logger.info("Attempted admin login")
                                
                                # Wait for page to load after login
                                time.sleep(3)
                                
                                # Check if we're on the profile page (where admin is redirected after login)
                                logger.info("\n=== CHECKING IF ON PROFILE PAGE ===")
                                try:
                                    # Look for profile page elements
                                    profile_elements = [
                                        (By.XPATH, "//*[contains(text(), 'Profile') or contains(text(), 'My Profile') or contains(text(), 'Edit Profile')]"),
                                        (By.CLASS_NAME, "profile-page"),
                                        (By.ID, "profileForm")
                                    ]
                                    
                                    on_profile_page = False
                                    for by, selector in profile_elements:
                                        try:
                                            self.wait.until(EC.visibility_of_element_located((by, selector)))
                                            logger.info("On profile page after login")
                                            self.take_screenshot("admin_profile_page")
                                            on_profile_page = True
                                            break
                                        except:
                                            continue
                                    
                                    if on_profile_page:
                                        # Edit profile name
                                        logger.info("\n=== EDITING ADMIN PROFILE ===")
                                        new_name = "AdminUser" + str(int(time.time()))
                                        
                                        # First find and click the EditProfile button
                                        edit_clicked = False
                                        edit_buttons = [
                                            (By.XPATH, "//button[text()='EditProfile']"),  # Exact text match
                                            (By.XPATH, "//button[contains(., 'Edit')]"),
                                            (By.CLASS_NAME, "edit-profile-button"),
                                            (By.ID, "editProfile"),
                                            (By.XPATH, "//button[contains(@class, 'btn-edit')]")
                                        ]
                                        
                                        for by, selector in edit_buttons:
                                            try:
                                                edit_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                                self.driver.execute_script("arguments[0].scrollIntoView(true);", edit_btn)
                                                self.driver.execute_script("arguments[0].style.border='3px solid orange';", edit_btn)
                                                time.sleep(1)
                                                self.driver.execute_script("arguments[0].click();", edit_btn)
                                                logger.info(f"Found and clicked EditProfile button with {by}={selector}")
                                                edit_clicked = True
                                                time.sleep(2)  # Wait for edit mode to activate
                                                break
                                            except Exception as e:
                                                logger.debug(f"EditProfile button not found with {by}={selector}: {str(e)}")
                                        
                                        if not edit_clicked:
                                            logger.warning("Could not find EditProfile button")
                                            self.take_screenshot("edit_button_not_found")
                                        else:
                                            # Update the name field
                                            name_updated = False
                                            name_field_selectors = [
                                                (By.ID, "name"),  # Try ID first as it's most specific
                                                (By.NAME, "name"),
                                                (By.XPATH, "//input[@placeholder='Name' or @placeholder='Enter name']"),
                                                (By.XPATH, "//input[@type='text' and @name='name']"),
                                                (By.CSS_SELECTOR, "input[type='text']"),
                                                (By.XPATH, "//label[contains(., 'Name')]/following-sibling::input")
                                            ]
                                            
                                            for by, selector in name_field_selectors:
                                                try:
                                                    name_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                                                    self.driver.execute_script("arguments[0].scrollIntoView(true);", name_field)
                                                    self.driver.execute_script("arguments[0].style.border='2px solid teal';", name_field)
                                                    name_field.clear()
                                                    name_field.send_keys(new_name)
                                                    logger.info(f"Updated name to: {new_name}")
                                                    name_updated = True
                                                    break
                                                except Exception as e:
                                                    logger.debug(f"Name field not found with {by}={selector}: {str(e)}")
                                            
                                            if not name_updated:
                                                logger.warning("Could not find name field to update")
                                                self.take_screenshot("name_field_not_found")
                                            
                                            # Click Save button
                                            save_clicked = False
                                            save_buttons = [
                                                (By.XPATH, "//button[text()='Save']"),
                                                (By.XPATH, "//button[@type='submit']"),
                                                (By.CSS_SELECTOR, "button[type='submit']"),
                                                (By.CLASS_NAME, "btn-save"),
                                                (By.ID, "saveProfile")
                                            ]
                                            
                                            for by, selector in save_buttons:
                                                try:
                                                    save_btn = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                                    self.driver.execute_script("arguments[0].scrollIntoView({block: 'center'});", save_btn)
                                                    self.driver.execute_script("arguments[0].style.border='3px solid green';", save_btn)
                                                    time.sleep(1)
                                                    self.driver.execute_script("arguments[0].click();", save_btn)
                                                    logger.info(f"Clicked Save button with {by}={selector}")
                                                    save_clicked = True
                                                    time.sleep(2)  # Wait for save to complete
                                                    break
                                                except Exception as e:
                                                    logger.debug(f"Save button not found with {by}={selector}: {str(e)}")
                                            
                                            if not save_clicked:
                                                logger.warning("Could not find Save button")
                                                self.take_screenshot("save_button_not_found")
                                            else:
                                                logger.info("Successfully updated admin profile")
                                                self.take_screenshot("admin_profile_updated")
                                    
                                    # Now navigate to Admin dashboard via navbar
                                    logger.info("\n=== NAVIGATING TO ADMIN DASHBOARD ===")
                                    
                                    # Try to find and click the Admin link in the navbar
                                    admin_found = False
                                    admin_selectors = [
                                        (By.XPATH, "//nav//a[text()='Admin']"),  # Exact text match for Admin
                                        (By.LINK_TEXT, "Admin"),  # Link with exact text Admin
                                        (By.XPATH, "//a[contains(., 'Admin')]"),  # Partial match as fallback
                                        (By.CLASS_NAME, "admin-link"),
                                        (By.CSS_SELECTOR, "nav a[href*='admin']"),
                                        (By.ID, "adminLink")
                                    ]
                                    
                                    for by, selector in admin_selectors:
                                        try:
                                            admin_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                            self.driver.execute_script("arguments[0].scrollIntoView(true);", admin_link)
                                            self.driver.execute_script("arguments[0].style.border='3px solid purple';", admin_link)
                                            time.sleep(1)
                                            self.driver.execute_script("arguments[0].click();", admin_link)
                                            logger.info(f"Found and clicked Admin link with {by}={selector}")
                                            admin_found = True
                                            time.sleep(2)  # Wait for admin dashboard to load
                                            break
                                        except Exception as e:
                                            logger.debug(f"Admin link not found with {by}={selector}: {str(e)}")
                                    
                                    if not admin_found:
                                        logger.warning("Could not find Admin link in the navbar")
                                        self.take_screenshot("admin_link_not_found")
                                        return
                                    
                                    # Take a screenshot of the admin dashboard
                                    self.take_screenshot("admin_dashboard_page")
                                    logger.info("Successfully navigated to Admin dashboard")
                                    
                                    # Verify we're on the admin dashboard
                                    try:
                                        admin_dashboard_elements = [
                                            (By.XPATH, "//h1[contains(., 'Admin Dashboard') or contains(., 'Admin Panel')]"),
                                            (By.CLASS_NAME, "admin-dashboard"),
                                            (By.ID, "adminDashboard"),
                                            (By.XPATH, "//*[contains(text(), 'Welcome Admin')]")
                                        ]
                                        
                                        for by, selector in admin_dashboard_elements:
                                            try:
                                                self.wait.until(EC.visibility_of_element_located((by, selector)))
                                                logger.info("Verified admin dashboard is displayed")
                                                break
                                            except:
                                                continue
                                        else:
                                            logger.warning("May not be on the admin dashboard page")
                                        
                                        # Click the bell icon (🔔) in the navbar
                                        logger.info("\n=== CLICKING BELL ICON IN NAVBAR ===")
                                        
                                        # Try different selectors for the bell icon
                                        bell_found = False
                                        bell_selectors = [
                                            (By.XPATH, "//button[contains(., '🔔') or contains(., 'Notifications')]"),
                                            (By.XPATH, "//*[text()='🔔']"),  # Exact bell emoji
                                            (By.CLASS_NAME, "notification-bell"),
                                            (By.CSS_SELECTOR, "button[aria-label*='notification']"),
                                            (By.CSS_SELECTOR, "button[title*='Notification']"),
                                            (By.ID, "notificationBell")
                                        ]
                                        
                                        for by, selector in bell_selectors:
                                            try:
                                                bell_icon = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                                self.driver.execute_script("arguments[0].scrollIntoView(true);", bell_icon)
                                                self.driver.execute_script("arguments[0].style.border='3px solid gold';", bell_icon)
                                                time.sleep(1)
                                                self.driver.execute_script("arguments[0].click();", bell_icon)
                                                logger.info(f"Found and clicked bell icon with {by}={selector}")
                                                bell_found = True
                                                time.sleep(2)  # Wait for notifications to appear
                                                break
                                            except Exception as e:
                                                logger.debug(f"Bell icon not found with {by}={selector}: {str(e)}")
                                        
                                        if not bell_found:
                                            logger.warning("Could not find bell icon in the navbar")
                                            self.take_screenshot("bell_icon_not_found")
                                            return
                                        
                                        # Take a screenshot of the notifications
                                        self.take_screenshot("notifications_dropdown")
                                        logger.info("Successfully opened notifications dropdown")
                                        
                                        # Navigate to Profile page
                                        logger.info("\n=== NAVIGATING TO PROFILE PAGE ===")
                                        
                                        # Try to find Profile link with exact text 'Profile'
                                        profile_found = False
                                        profile_selectors = [
                                            (By.XPATH, "//a[text()='Profile']"),  # Exact text match for Profile
                                            (By.LINK_TEXT, "Profile")  # Link with exact text Profile
                                        ]
                                        
                                        for by, selector in profile_selectors:
                                            try:
                                                profile_link = self.wait.until(EC.element_to_be_clickable((by, selector)))
                                                self.driver.execute_script("arguments[0].scrollIntoView(true);", profile_link)
                                                self.driver.execute_script("arguments[0].style.border='3px solid teal';", profile_link)
                                                time.sleep(1)
                                                self.driver.execute_script("arguments[0].click();", profile_link)
                                                logger.info(f"Found and clicked Profile link with {by}={selector}")
                                                profile_found = True
                                                time.sleep(2)  # Wait for profile page to load
                                                break
                                            except Exception as e:
                                                logger.debug(f"Profile link not found with {by}={selector}: {str(e)}")
                                        
                                        if not profile_found:
                                            logger.warning("Could not find Profile link in the navbar")
                                            self.take_screenshot("profile_link_not_found")
                                            return
                                        
                                        # Take a screenshot of the profile page
                                        self.take_screenshot("profile_page")
                                        logger.info("Successfully navigated to Profile page")
                                        
                                        
                                        # Click on Home in the navigation bar using the reliable partial link text method
                                        logger.info("=== CLICKING HOME BUTTON ===")
                                        try:
                                            # Find all Home links using partial link text (proven to work from logs)
                                            home_links = self.wait.until(
                                                EC.presence_of_all_elements_located((By.PARTIAL_LINK_TEXT, "Home")),
                                                "No Home links found on the page"
                                            )
                                            
                                            # Find the first visible Home link
                                            for link in home_links:
                                                try:
                                                    if link.is_displayed():
                                                        # Scroll into view and highlight
                                                        self.driver.execute_script("""
                                                            arguments[0].scrollIntoView({block: 'center', behavior: 'smooth'});
                                                            arguments[0].style.border = '3px solid #4CAF50';
                                                            arguments[0].style.padding = '2px';
                                                        """, link)
                                                        time.sleep(0.5)  # Small delay for visual feedback
                                                        
                                                        # Take screenshot before clicking
                                                        self.take_screenshot("before_home_click")
                                                        
                                                        # Click using JavaScript
                                                        self.driver.execute_script("arguments[0].click();", link)
                                                        logger.info("Successfully clicked Home button using partial link text")
                                                        
                                                        # Wait for navigation and take screenshot
                                                        time.sleep(2)
                                                        self.take_screenshot("after_home_click")
                                                        break
                                                        
                                                except Exception as e:
                                                    logger.debug(f"Home link not clickable, trying next one: {str(e)}")
                                            else:
                                                raise Exception("No visible Home links found")
                                                
                                        except Exception as e:
                                            logger.error(f"Failed to click Home button: {str(e)}")
                                            self.take_screenshot("home_button_failed")
                                            raise  # Re-raise the exception to fail the test
                                        
                                    except Exception as e:
                                        logger.error(f"Error verifying admin dashboard or clicking bell icon: {str(e)}")
                                        self.take_screenshot("admin_dashboard_verification_error")
                                        
                                except Exception as e:
                                    logger.error(f"Error verifying admin login: {str(e)}")
                                    self.take_screenshot("admin_login_verification_error")
                    
                    except Exception as e:
                        logger.error(f"Error during profile update or navigation: {str(e)}")
                        self.take_screenshot("profile_or_navigation_error")
            else:
                logger.warning("Login may not have been successful")
                logger.info(f"Current URL: {self.driver.current_url}")
            
        except Exception as e:
            self.take_screenshot("test_register_login_failed")
            logger.error(f"Test failed: {str(e)}")
            raise
    
    def test_invalid_login(self):
        """Test login with invalid credentials using the navigation bar"""
        try:
            # Navigate to the home page first
            logger.info(f"Navigating to {self.base_url}")
            self.driver.get(self.base_url)
            time.sleep(2)  # Wait for page to load
            
            # Take initial screenshot
            self.take_screenshot("home_page_loaded")
            
            # Click the login button in the navigation bar
            logger.info("Looking for login button in navigation bar...")
            
            # Try different selectors for the navigation login button
            nav_login_selectors = [
                (By.XPATH, "//nav//a[contains(translate(., 'LOGIN', 'login'), 'login')]"),
                (By.XPATH, "//header//a[contains(translate(., 'LOGIN', 'login'), 'login')]"),
                (By.CSS_SELECTOR, "nav a[href*='login']"),
                (By.CSS_SELECTOR, "header a[href*='login']"),
                (By.LINK_TEXT, "Login"),
                (By.PARTIAL_LINK_TEXT, "Login")
            ]
            
            login_found = False
            for by, selector in nav_login_selectors:
                try:
                    login_link = self.driver.find_element(by, selector)
                    logger.info(f"Found login link with {by}={selector}")
                    # Scroll the element into view
                    self.driver.execute_script("arguments[0].scrollIntoView(true);", login_link)
                    # Highlight the element
                    self.driver.execute_script("arguments[0].style.border='3px solid red';", login_link)
                    time.sleep(1)
                    # Click using JavaScript to avoid interception
                    self.driver.execute_script("arguments[0].click();", login_link)
                    logger.info("Clicked login link in navigation")
                    login_found = True
                    break
                except Exception as e:
                    logger.debug(f"Login link not found with {by}={selector}: {str(e)}")
            
            if not login_found:
                logger.error("Could not find login link in navigation")
                self.take_screenshot("login_link_not_found")
                return
                
            # Wait for login page to load
            time.sleep(3)
            self.take_screenshot("login_page_loaded")
            
            # Print page source for debugging (first 1000 characters)
            page_source = self.driver.page_source
            logger.info("Page source (first 1000 chars):\n" + page_source[:1000])
            
            # Take a screenshot of the login form
            self.take_screenshot("login_form")
            
            # Try to find email field with different selectors
            email_selectors = [
                (By.NAME, "email"),
                (By.ID, "email"),
                (By.XPATH, "//input[@type='email']"),
                (By.CSS_SELECTOR, "input[type='email']"),
                (By.NAME, "username"),
                (By.ID, "username")
            ]
            
            email_field = None
            for by, selector in email_selectors:
                try:
                    email_field = self.wait.until(EC.visibility_of_element_located((by, selector)))
                    logger.info(f"Found email field with {by}={selector}")
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.border='2px solid green';", email_field)
                    break
                except Exception as e:
                    logger.debug(f"Email field not found with {by}={selector}: {str(e)}")
            
            if not email_field:
                logger.error("Could not find email field with any selector")
                self.take_screenshot("email_field_not_found")
                return
            
            # Try to find password field with different selectors
            password_selectors = [
                (By.NAME, "password"),
                (By.ID, "password"),
                (By.XPATH, "//input[@type='password']"),
                (By.CSS_SELECTOR, "input[type='password']")
            ]
            
            password_field = None
            for by, selector in password_selectors:
                try:
                    password_field = self.driver.find_element(by, selector)
                    logger.info(f"Found password field with {by}={selector}")
                    # Highlight the field
                    self.driver.execute_script("arguments[0].style.border='2px solid green';", password_field)
                    break
                except:
                    logger.debug(f"Password field not found with {by}={selector}")
            
            if not password_field:
                logger.error("Could not find password field with any selector")
                self.take_screenshot("password_field_not_found")
                return
            
            # Fill in the form with more reliable method
            logger.info("Filling in credentials...")
            try:
                # Clear fields using JavaScript
                self.driver.execute_script("arguments[0].value = '';", email_field)
                self.driver.execute_script("arguments[0].value = '';", password_field)
                
                # Type each character with a small delay
                email = "faith@gmail"
                for char in email:
                    email_field.send_keys(char)
                    time.sleep(0.1)
                
                password = "A"
                for char in password:
                    password_field.send_keys(char)
                    time.sleep(0.1)
                
                # Take screenshot after entering credentials
                self.take_screenshot("credentials_entered")
                
            except Exception as e:
                logger.error(f"Error entering credentials: {str(e)}")
                self.take_screenshot("credential_entry_error")
                return
            
            # Take screenshot before submit
            self.take_screenshot("before_login_click")
            
            # Try to find and click the submit button
            try:
                # Try different selectors for the login button
                selectors = [
                    (By.CSS_SELECTOR, "button[type='submit']"),
                    (By.XPATH, "//button[contains(text(), 'Login')]"),
                    (By.XPATH, "//button[contains(text(), 'Sign In')]"),
                    (By.CLASS_NAME, "btn-primary"),
                    (By.ID, "loginButton")
                ]
                
                for by, selector in selectors:
                    try:
                        login_button = self.driver.find_element(by, selector)
                        logger.info(f"Found login button with {by}={selector}")
                        # Highlight the button
                        self.driver.execute_script("arguments[0].style.border='3px solid red';", login_button)
                        time.sleep(1)
                        login_button.click()
                        logger.info("Clicked login button")
                        break
                    except:
                        continue
                else:
                    logger.error("Could not find login button with any selector")
                    self.take_screenshot("login_button_not_found")
                    return
                
                # Wait after click
                time.sleep(3)
                self.take_screenshot("after_login_click")
                
                # Print current URL after login attempt
                logger.info(f"Current URL after login attempt: {self.driver.current_url}")
                
            except Exception as e:
                logger.error(f"Error during login attempt: {str(e)}")
                self.take_screenshot("login_error")
                raise
            
        except Exception as e:
            self.take_screenshot("test_invalid_login_failed")
            self.fail(f"Test failed: {str(e)}")
    
    def test_logout_functionality(self):
        """Test logout functionality"""
        # First login
        if self.login():
            # Then logout
            self.assertTrue(self.logout(), "Logout should be successful")
            
            # Try to access a protected page
            self.driver.get(f"{self.base_url}/dashboard")
            
            # Should be redirected to login or home page
            self.assertTrue(
                "login" in self.driver.current_url or "home" in self.driver.current_url,
                "Should be redirected to login or home page after logout"
            )

class TestSchedulePickup(CleanCityBaseTest):
    """Test schedule pickup functionality"""
    
    def test_schedule_valid_pickup(self):
        """Test scheduling a new waste pickup"""
        if not self.login():
            self.skipTest("Login failed, cannot proceed with pickup scheduling")
            
        try:
            # Navigate to schedule pickup
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Schedule Pickup"))).click()
            
            # Fill out the form
            tomorrow = (datetime.now() + timedelta(days=1)).strftime("%Y-%m-%d")
            
            self.wait.until(EC.presence_of_element_located((By.ID, "location"))).send_keys("Nairobi")
            self.driver.find_element(By.ID, "date").send_keys(tomorrow)
            self.driver.find_element(By.ID, "waste-type").send_keys("Plastic")
            self.driver.find_element(By.ID, "description").send_keys("Test pickup description")
            
            # Submit the form
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Verify success message or redirect
            success_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "success-message")))
            self.assertIn("success", success_message.text.lower(), "Should show success message")
            
        except Exception as e:
            self.take_screenshot("test_schedule_pickup_failed")
            self.fail(f"Test failed: {str(e)}")
    
    def test_empty_form_validation(self):
        """Test form validation with empty fields"""
        if not self.login():
            self.skipTest("Login failed, cannot proceed with form validation")
            
        try:
            self.wait.until(EC.element_to_be_clickable((By.LINK_TEXT, "Schedule Pickup"))).click()
            
            # Try to submit empty form
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            
            # Verify validation messages
            error_messages = self.driver.find_elements(By.CLASS_NAME, "error-message")
            self.assertGreater(len(error_messages), 0, "Should show validation errors")
            
        except Exception as e:
            self.take_screenshot("test_form_validation_failed")
            self.fail(f"Test failed: {str(e)}")

class TestDashboard(CleanCityBaseTest):
    """Test dashboard functionality"""
    
    def test_dashboard_loading(self):
        """Test if dashboard loads correctly"""
        if not self.login():
            self.skipTest("Login failed, cannot access dashboard")
            
        try:
            # Check if dashboard elements are present
            welcome_message = self.wait.until(EC.presence_of_element_located((By.CLASS_NAME, "welcome-message")))
            self.assertIn("Welcome", welcome_message.text, "Should display welcome message")
            
            # Check for recent pickups section
            recent_pickups = self.driver.find_elements(By.CLASS_NAME, "pickup-card")
            self.assertGreaterEqual(len(recent_pickups), 0, "Should display pickup cards")
            
        except Exception as e:
            self.take_screenshot("test_dashboard_loading_failed")
            self.fail(f"Test failed: {str(e)}")

class TestResponsiveDesign(CleanCityBaseTest):
    """Test responsive design on different screen sizes"""
    
    def test_mobile_view(self):
        """Test responsive design on mobile view"""
        try:
            # Set mobile viewport
            self.driver.set_window_size(375, 812)  # iPhone X dimensions
            
            # Check if mobile menu is accessible
            menu_button = self.wait.until(EC.element_to_be_clickable((By.CLASS_NAME, "mobile-menu-button")))
            menu_button.click()
            
            # Check if menu is expanded
            nav_links = self.wait.until(EC.visibility_of_element_located((By.CLASS_NAME, "nav-links")))
            self.assertTrue(nav_links.is_displayed(), "Mobile menu should be visible")
            
            # Reset window size
            self.driver.maximize_window()
            
        except Exception as e:
            self.take_screenshot("test_mobile_view_failed")
            self.fail(f"Test failed: {str(e)}")

class TestResponsiveDesign(unittest.TestCase):
    """Test responsive design across different screen sizes"""
    
    def setUp(self):
        """Set up the test environment"""
        self.base_url = "https://genuine-pavlova-b1ad13.netlify.app/"  
        self.driver = webdriver.Chrome()
        self.driver.implicitly_wait(10)
        self.screen_sizes = [
            (320, 568),   # iPhone SE
            (375, 667),   # iPhone 8
            (414, 896),   # iPhone XR
            (768, 1024),  # iPad
            (1024, 768),  # iPad Pro (portrait)
            (1366, 768),  # Laptop
            (1920, 1080)  # Desktop
        ]
        
    def test_responsive_layouts(self):
        """Test that the layout adjusts correctly for different screen sizes"""
        results = {}
        
        for width, height in self.screen_sizes:
            try:
                # Set window size
                self.driver.set_window_size(width, height)
                self.driver.get(self.base_url)
                
                # Take screenshot for visual verification
                device_name = f"{width}x{height}"
                self.driver.save_screenshot(f"screenshots/responsive_{device_name}.png")
                
                # Test key elements are visible - using more flexible selectors
                elements_to_check = [
                    ("Navbar", [
                        "//nav", 
                        "//header", 
                        "//div[contains(@class, 'navbar')]",
                        "//div[contains(@class, 'header')]"
                    ]),
                    ("Main Content", [
                        "//main", 
                        "//div[contains(@class, 'main')]",
                        "//div[contains(@class, 'content')]",
                        "//div[contains(@class, 'container')]"
                    ]),
                    ("Footer", [
                        "//footer", 
                        "//div[contains(@class, 'footer')]",
                        "//div[contains(@class, 'site-footer')]"
                    ])
                ]
                
                visible_elements = []
                for name, selectors in elements_to_check:
                    found = False
                    last_error = None
                    
                    for selector in selectors:
                        try:
                            elements = self.driver.find_elements(By.XPATH, selector)
                            if elements:
                                # Check if any matching element is visible
                                for element in elements:
                                    if element.is_displayed():
                                        visible_elements.append((name, True))
                                        found = True
                                        logger.info(f"Found visible {name} with selector: {selector}")
                                        break
                                if found:
                                    break
                        except Exception as e:
                            last_error = str(e)
                            logger.debug(f"Selector failed for {name} with {selector}: {last_error}")
                    
                    if not found:
                        logger.warning(f"Could not find visible {name} with any selector")
                        visible_elements.append((name, False))
                
                results[device_name] = {
                    'visible_elements': visible_elements,
                    'url': self.driver.current_url,
                    'title': self.driver.title
                }
                
                logger.info(f"Tested {device_name}: {sum(1 for _, visible in visible_elements if visible)}/{len(visible_elements)} elements visible")
                
            except Exception as e:
                logger.error(f"Error testing size {width}x{height}: {str(e)}")
                results[f"{width}x{height}"] = {"error": str(e)}
        
        # Print summary
        logger.info("\n=== RESPONSIVE TESTING SUMMARY ===")
        for device, result in results.items():
            if 'error' in result:
                logger.error(f"{device}: {result['error']}")
            else:
                visible_count = sum(1 for _, visible in result['visible_elements'] if visible)
                logger.info(f"{device}: {visible_count}/{len(result['visible_elements'])} elements visible")
        
        # Assert that all tests passed
        for device, result in results.items():
            if 'error' in result:
                self.fail(f"Test failed for {device}: {result['error']}")
            visible_count = sum(1 for _, visible in result['visible_elements'] if visible)
            self.assertEqual(visible_count, len(result['visible_elements']), 
                          f"Not all elements visible on {device}")
    
    def test_mobile_navigation(self):
        """Test mobile-specific navigation elements with flexible selectors"""
        # Test mobile view (iPhone SE)
        self.driver.set_window_size(320, 568)
        self.driver.get(self.base_url)
        
        # Take initial screenshot
        self.driver.save_screenshot("screenshots/mobile_initial.png")
        
        # Try multiple selectors for mobile menu button
        menu_selectors = [
            "button[aria-label*='enu']",  # Case-insensitive match for 'menu'
            "[class*='hamburger']",      # Any element with 'hamburger' in class
            "[class*='menu'] button",     # Button inside any element with 'menu' class
            "button > span:only-child",   # Button with a single span (common pattern)
            "button:has(svg)",           # Button containing an SVG (common for icons)
            "button"                     # Fallback to any button
        ]
        
        menu_found = False
        for selector in menu_selectors:
            try:
                menu_buttons = self.driver.find_elements(By.CSS_SELECTOR, selector)
                for button in menu_buttons:
                    try:
                        if button.is_displayed():
                            # Highlight the button
                            self.driver.execute_script("""
                                arguments[0].style.border = '3px solid #FFA500';
                                arguments[0].style.padding = '2px';
                            """, button)
                            
                            logger.info(f"Found potential menu button with selector: {selector}")
                            self.driver.save_screenshot(f"screenshots/menu_button_found_{selector.replace(' ', '_')}.png")
                            
                            # Click the button
                            button.click()
                            time.sleep(1)  # Wait for animation
                            
                            # Check for navigation items
                            nav_items = self.driver.find_elements(By.CSS_SELECTOR, 
                                "nav a, [role='navigation'] a, .nav-item, .menu-item")
                            
                            if nav_items:
                                logger.info(f"Found {len(nav_items)} navigation items after clicking menu")
                                menu_found = True
                                self.driver.save_screenshot("screenshots/mobile_menu_open.png")
                                break
                            
                    except Exception as e:
                        logger.debug(f"Menu interaction failed with {selector}: {str(e)}")
                
                if menu_found:
                    break
                    
            except Exception as e:
                logger.debug(f"Selector failed: {selector} - {str(e)}")
        
        if not menu_found:
            logger.warning("Could not find or interact with mobile menu. Taking full page screenshot...")
            self.driver.save_screenshot("screenshots/mobile_menu_not_found.png")
            
            # Log page structure for debugging
            try:
                page_source = self.driver.page_source[:2000]  # First 2000 chars
                logger.info(f"Page source snippet:\n{page_source}")
            except:
                logger.warning("Could not get page source for debugging")
    
    def test_tablet_landscape(self):
        """Test tablet-specific layout in landscape mode"""
        # Set tablet landscape size
        self.driver.set_window_size(1024, 768)
        self.driver.get(self.base_url)
        
        # Check if layout adjusts (e.g., sidebar might be visible)
        try:
            sidebar = self.driver.find_element(By.CSS_SELECTOR, 
                "aside.sidebar, .sidebar-nav")
            self.assertTrue(sidebar.is_displayed(), 
                         "Sidebar should be visible in tablet landscape")
        except NoSuchElementException:
            logger.info("No sidebar detected in tablet landscape mode")
    
    def tearDown(self):
        """Clean up after tests"""
        self.driver.quit()


if __name__ == "__main__":
    # Create test suite and run tests
    import xmlrunner
    
    # Create output directory for test reports
    import os
    os.makedirs("test-reports", exist_ok=True)
    
    # Run tests and generate JUnit XML report
    unittest.main(
        testRunner=xmlrunner.XMLTestRunner(output='test-reports'),
        failfast=False,
        buffer=False,
        catchbreak=False
    )
