from atexit import register

import time, sys, random, pickle, string
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import login

# Read data from config file: base_url, user cred., ...
info = pickle.load( open( "config/config", "rb" ) )

base_url = info["url"]
valid_email = info["username"]
valid_password = info["password"]

driver = webdriver.Chrome()
driver.implicitly_wait(1)

# register(driver.quit) # close browser at the end

driver.get(base_url)
driver.maximize_window()

#time.sleep(1)

# def randomString(stringLength=10):
#     """Generate a random string of fixed length """
#     letters = string.ascii_lowercase
#     return ''.join(random.choice(letters) for i in range(stringLength))

##### SIGN IN PAGE #####
try:
	banner_button = driver.find_element_by_css_selector("a[aria-label='dismiss cookie message']")
	banner_button.click()
except:
	print('Cannot find button on the banner!')

# Signing in
login.log_in(driver, valid_email, valid_password)

time.sleep(1)

##### User management page #####

try:
	user_management_button = driver.find_element_by_css_selector('a[href="/user-management"]')
	user_management_button.click()
	print('User Management page is opened!')
except:
	print('Failed to find "User Management" button!')

assert driver.current_url == (base_url + '/user-management')

#%%%%% PASS %%%%%

try:
	admin_email_field = driver.find_element_by_xpath("//tbody//td[contains(text(), 'stbm-100@amail.club')]")
	print("SUCCESS!")
except:
	print("Failed to find admin's email in the table")
