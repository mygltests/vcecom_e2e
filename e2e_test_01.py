###### Test steps ########
# Sign in
# Navigate to Meeting Rooms page
# CRUD rooms
# Log out
##########################

#from atexit import register

import time, sys, random, pickle
from datetime import datetime

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

driver.get(base_url)
driver.maximize_window()

#time.sleep(1)

def get_rooms_names(driver):
	# get all rooms names, returns a list of rooms names
	try:
		meeting_rooms_names = [el.get_attribute("value") for el in
							   driver.find_elements_by_css_selector('input[id^="roomName-"')]
		print(meeting_rooms_names)
		return meeting_rooms_names
	except:
		print("Can't fetch rooms names")

def create_room(driver):
	# Create new room 'EditMe. Created <timestamp>'
	try:
		create_room_button = driver.find_element_by_css_selector("app-empty-room p")
		create_room_button.click()
	except:
		print("Can't find Create Room button")

	try:
		new_room_name_input = driver.find_element_by_css_selector("app-empty-room form input#newRoomName")
		new_room_name_input.clear()
		new_room_name_input.send_keys("EditMe. Created" + datetime.now().strftime("%d/%m/%Y %H:%M") + Keys.ENTER)
		print("New room has been created")
	except:
		print("Can't find NewRoomName input")

##### SIGN IN PAGE #####
try:
	banner_button = driver.find_element_by_css_selector("a[aria-label='dismiss cookie message']")
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


##### HOME PAGE #####
# Welcome message
try:
	hello_message = driver.find_element_by_css_selector("div.row.summary-info > div.col-12.col-md-5 > h2:nth-child(2)")
	print('User is signed in!')
except:
	print('Cannot find welcome message!')

# time.sleep(2) 

##### MY MEETINGS ROOM PAGE #####
# Visit Meeting rooms page
try:
	meeting_rooms_button = driver.find_element_by_css_selector('a[href="/meeting-rooms"]')
	meeting_rooms_button.click()
	print('Meeting rooms page is opened!')
except:
	print('Cannot find "Meeting rooms" button!')
	
assert driver.current_url == (base_url + '/meeting-rooms')

# Get number of rooms available

if len(get_rooms_names(driver)) > 3:
	assert rooms_number <= 3
#elif rooms_number == 3:

# Edit default room (done)
try:
	default_room = driver.find_element_by_css_selector("#roomName-0")
	default_room.clear()
	default_room_name_edited = "Default room. Edited " + datetime.now().strftime("%d/%m/%Y %H:%M")
	default_room.send_keys(default_room_name_edited + Keys.ENTER)
	print("Edited default room name successfully")
except:
	print("Can't find default room")

# Check if def room name edited
assert default_room_name_edited in get_rooms_names(driver)

create_room(driver)

# Delete room 'DeleteMe. Edited <timestamp>'
# Find room to delete
try:
	deleteMe_room_name = driver.find_element_by_xpath("//input[starts-with(@value, 'DeleteMe')]").get_attribute("value")
	delete_room_button = driver.find_element_by_xpath("//input[contains(@value, 'DeleteMe')]//ancestor::app-filled-room//p[@class='small']")
	delete_room_button.click()
	print("@@@@@@@@@@@@@@@@@@@@@@", deleteMe_room_name)
except:
	print("Can't find Create Room button")

# try:
# 	yes_btn = driver.find_element_by_css_selector(".btn btn-success")
# 	yes_btn.click()
# 	print("Room deleted !!!")
# except:
# 	print("Failed to find YES button on confirmation modal")
#
# time.sleep(1)

# assert deleteMe_room_name not in get_rooms_names(driver)

# try:
# 	new_room_name_input = driver.find_element_by_css_selector("app-empty-room form input#newRoomName")
# 	new_room_name_input.clear()
# 	new_room_name_input.send_keys("EditMe. Created" + datetime.now().strftime("%d/%m/%Y %H:%M") + Keys.ENTER)
# 	print("New room has been created")
# except:
# 	print("Can't find NewRoomName input")





## INFO
# date and time string
# datetime.now().strftime("%d/%m/%Y %H:%M")
# DeleteMe. Edited <time>
# EditMe. Created <time>





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

	
