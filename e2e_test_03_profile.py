###### Test steps ########
# Sign in
# Navigate to Profile page
# Verify Email field is not editable
# update user info
# Navigate to Organization page via dropdown
# Navigate to Profile via Sidebar
# Get user info - updated
# Log out
##########################

from atexit import register

import time, sys, random, pickle, string
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains

import login

# Read data from config file: base_url, user cred., ...
info = pickle.load( open( "config/config", "rb" ) )

base_url = info["url"]
valid_email = info["username"]
valid_password = info["password"]
adminFirstName = info["firstName"]
adminLastName = info["lastName"]

driver = webdriver.Chrome()
driver.implicitly_wait(1)

#register(driver.quit) # close browser at the end

driver.get(base_url)
driver.maximize_window()

##### SIGN IN PAGE #####
try:
	banner_button = driver.find_element_by_css_selector("a[aria-label='dismiss cookie message']")
	banner_button.click()
except:
	print('Cannot find button on the banner!')

# Signing in
login.log_in(driver, valid_email, valid_password)

time.sleep(1)

# Navigate to Profile page #
try:
    myAccount_button = driver.find_element_by_css_selector("#dropdownMenuLink")
    action = ActionChains(driver)
    action.move_to_element(myAccount_button).perform()
    organization_link = driver.find_element_by_css_selector(".dropdown-menu div[routerlink='my-account/profile'] a")
    organization_link.click()
    print("Profile page is opened!")
except:
    print('Failed to find My Account/Organization button')

assert driver.current_url == (base_url + '/my-account/profile')

# Check if Email is editable
try:
    email_input = driver.find_element_by_css_selector("input#email")
    assert email_input.is_enabled() == False
except:
    print("Failed to find Email input!")

try:
    adminFirstName_input = driver.find_element_by_css_selector("input#FirstName")
    adminFirstName = adminFirstName_input.get_attribute("value")
    adminFirstName_input.send_keys(" edited")
    adminLastName_input = driver.find_element_by_css_selector("input#lastName")
    adminLastName = adminLastName_input.get_attribute("value")
    adminLastName_input.send_keys(" edited")
    submit_button = driver.find_element_by_css_selector("button.submit-button")
    submit_button.click()
    print("Updated user info successfully")
except:
    print("Failed to update profile info")

time.sleep(1)

try:
    left_organization_button = driver.find_element_by_css_selector("div[routerlink='organization']")
    left_organization_button.click()
    print("Navigated to Organization page!")
except:
    print("Failed to find Organization button")

assert driver.current_url == base_url + "/my-account/organization"

try:
    left_profile_button = driver.find_element_by_css_selector("div[routerlink='profile']")
    left_profile_button.click()
    print("Navigated to Profile page!")
except:
    print("Failed to find Profile button")

assert driver.current_url == base_url + "/my-account/profile"

try:
    adminFirstName_input = driver.find_element_by_css_selector("input#FirstName")
    adminLastName_input = driver.find_element_by_css_selector("input#lastName")
    assert adminFirstName_input.get_attribute("value") == adminFirstName + ' edited'
    assert adminLastName_input.get_attribute("value") == adminLastName + ' edited'
    print("Check for user info update PASSED")
except:
    print("Failed to check  profile info update")

print(adminLastName)

# Rollback to initial user info
try:
    adminFirstName_input = driver.find_element_by_css_selector("input#FirstName")
    adminFirstName_input.clear()
    adminFirstName_input.send_keys("admin 100")
    adminLastName_input = driver.find_element_by_css_selector("input#lastName")
    adminLastName_input.clear()
    adminLastName_input.send_keys("user")
    submit_button = driver.find_element_by_css_selector("button.submit-button")
    submit_button.click()
    print("Updated user info successfully")
except:
    print("Failed to rollback profile info")

# Log out
time.sleep(2)
try:
	my_account_button = driver.find_element_by_css_selector("#dropdownMenuLink")
	my_account_button.click()
	print('Account menu is opened!')
except:
	print('Failed to find "My Account" button!')

time.sleep(1)
try:
	logout_button = driver.find_element_by_css_selector("a.dropdown-item.last-it")
	logout_button.click()
	print('Logged out!')
except:
	print('Failed to find "Logout" button!')