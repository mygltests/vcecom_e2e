#from atexit import register

import time, sys, random, pickle

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC



# Read data from config file: base_url, user cred., ...
info = pickle.load( open( "config/config", "rb" ) )

base_url = info["url"]
valid_email = info["username"]
valid_password = info["password"]

driver = webdriver.Chrome()

driver.implicitly_wait(1)

#register(driver.quit)

driver.maximize_window()

driver.get(base_url)

#time.sleep(1)

try:
	banner_button = driver.find_element_by_css_selector(".cc-compliance > a[aria-label='dismiss cookie message']")
	banner_button.click()  
except:
	print('Cannot find button on the banner!')

#time.sleep(1)

try:
	email_field = driver.find_element_by_css_selector("#input25")
	email_field.clear()
	email_field.send_keys(valid_email)  
except:
	print('Cannot find email text field!')

#time.sleep(1)

try:
	password_field = driver.find_element_by_css_selector("#input32")
	password_field.clear()
	password_field.send_keys(valid_password)
except:
	print('Cannot find password text field!')

#time.sleep(1)

try:
	signin_button = driver.find_element_by_css_selector("input[type='submit']")
	signin_button.click()
except:
	print('Cannot find SIGN IN button!')

time.sleep(1)
	
# Welcome message
try:
	hello_message = driver.find_element_by_css_selector("div.row.summary-info > div.col-12.col-md-5 > h2:nth-child(2)")
	print('User is signed in!')
except:
	print('Cannot find welcome message!')

# time.sleep(2) 

# Visit Meeting rooms page

try:
	meeting_rooms_button = driver.find_element_by_css_selector('ul>li>a[href="/meeting-rooms"]')
	meeting_rooms_button.click()
except:
	print('Cannot find "Meeting rooms" button!')
	
assert driver.current_url == (base_url + '/meeting-rooms')

# Get number of rooms available
try:
	meeting_rooms = driver.find_elements_by_css_selector("app-filled-room")
	rooms_number = len(meeting_rooms)
	print("number of meeting rooms created: ", rooms_number)
except:
	print("Can't find meeting room box")

if rooms_number > 3:
	assert rooms_number <= 3
#elif:
#	rooms_number == 3:
# TODO: Add code to delete room first in this case!

try:
	create_room_button = driver.find_element_by_css_selector("app-empty-room p")
	create_room_button.click()
except: 
	print("Can't find Create Room button")
	
try:
	new_room_name_input = driver.find_element_by_css_selector("app-empty-room form input#newRoomName")
	new_room_name_input.clear()
	new_room_name_input.send_keys("Just created 1")
except:
	print("Can't find NewRoomName input")

###

# Get NEW number of rooms available
try:
	new_meeting_rooms = driver.find_elements_by_css_selector("app-filled-room")
	new_rooms_number = len(meeting_rooms)
	print("NEW number of meeting rooms created: ", new_rooms_number)
except:
	print("Can't find meeting room box")

if new_rooms_number > 3:
	assert rooms_number <= 3
elif new_rooms_number != rooms_number + 1:
	assert new_rooms_number == rooms_number + 1

# TODO: Add code to check if created room is available 




# # Visit User Management page
# try:
	# meeting_rooms_button = driver.find_element_by_css_selector('ul>li>a[href="/user-management"]')
	# meeting_rooms_button.click()
# except:
	# print('Cannot find "User Management" button!')

# # # # Visit Analytics page -- Commented, switch to new window is not handled yet
# # # try:
	# # # meeting_rooms_button = driver.find_element_by_css_selector('ul>li>a[target="_blank"]')
	# # # meeting_rooms_button.click()
# # # except:
	# # # print('Cannot find "Analytics" button!')

	
# # Visit Plan details page
# try:
	# meeting_rooms_button = driver.find_element_by_css_selector('ul>li>a[href="/upgrade-plan"]')
	# meeting_rooms_button.click()
# except:
	# print('Cannot find "Plan details" button!')

	
	


	
	
