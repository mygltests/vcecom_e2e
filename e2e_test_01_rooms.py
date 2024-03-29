###### Test steps ########
# Sign in
# Navigate to Org page
# CRUD rooms
# Log out
##########################

from atexit import register

import time, sys, random, pickle, string
from datetime import datetime

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC

import login


class LoginPage:
	username = (By.CSS_SELECTOR, '.sdfg')

# Read data from config file: base_url, user cred., ...
info = pickle.load( open( "config/config", "rb" ) )

base_url = info["url"]
valid_email = info["username"]
valid_password = info["password"]

driver = webdriver.Chrome()
driver.implicitly_wait(1)

register(driver.quit) # close browser at the end

driver.get(base_url)
driver.maximize_window()

#time.sleep(1)

def get_rooms_names(driver):
	# get all rooms names, returns a list of rooms names
	try:
		meeting_rooms_names = [el.get_attribute("value") for el in
							   driver.find_elements_by_css_selector('input[id^="roomName-"')]
		#print(meeting_rooms_names)
		return meeting_rooms_names
	except:
		print("Can't fetch rooms names")

def create_room(driver, new_room_name):
	# Create new room 'EditMe. Created <timestamp>'
	try:
		create_room_button = driver.find_element_by_css_selector("app-empty-room p")
		create_room_button.click()
	except:
		print("Failed to find Create Room button")

	try:
		new_room_name_input = driver.find_element_by_css_selector("app-empty-room form input#newRoomName")
		new_room_name_input.clear()
		new_room_name_input.send_keys(new_room_name + Keys.ENTER)
		print("New room has been created")
	except:
		print("Failed to find NewRoomName input")

def randomString(stringLength=10):
    """Generate a random string of fixed length """
    letters = string.ascii_lowercase
    return ''.join(random.choice(letters) for i in range(stringLength))


##### SIGN IN PAGE #####
try:
	banner_button = driver.find_element_by_css_selector("a[aria-label='dismiss cookie message']")
	banner_button.click()  
except:
	print('Cannot find button on the banner!')

# Signing in
login.log_in(driver, valid_email, valid_password)

time.sleep(1)

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
rooms_number = len(get_rooms_names(driver))

if rooms_number > 3:
	assert rooms_number <= 3
elif rooms_number == 3:
	try:
		delete3rd_room_name = driver.find_element_by_css_selector("#roomName-2").get_attribute("value")
		delete_room_button = driver.find_element_by_css_selector("app-filled-room:last-child p[class='small'") 	# !!!
		delete_room_button.click()
	except:
		print("Failed to find Delete button for 3rd room")
	time.sleep(1)
	try:
		yes_btn = driver.find_element_by_xpath("//div[@class='modal-body']//button[@class='btn btn-success']")
		yes_btn.click()
		print("3rd room has been deleted")
	except:
		print("Failed to find YES button on confirmation modal")

	time.sleep(1)
	assert delete3rd_room_name in get_rooms_names(driver)

# Edit default room
try:
	default_room = driver.find_element_by_css_selector("#roomName-0")
	default_room.clear()
	default_room_name_edited = "Default room. Edited " + datetime.now().strftime("%d/%m/%Y %H:%M")
	default_room.send_keys(default_room_name_edited + Keys.ENTER)
	print("Edited default room name successfully")
except:
	print("Failed to edit default room")

# Check if def room name edited
time.sleep(2)
assert default_room_name_edited in get_rooms_names(driver)

# Create new room
new_room_name = "EditMe. Created " + datetime.now().strftime("%d/%m/%Y %H:%M")
create_room(driver, new_room_name)

time.sleep(2)
assert new_room_name in get_rooms_names(driver)

# Edit EditMe room
try:
	editMe_room_name = driver.find_element_by_xpath("(//input[starts-with(@value, 'EditMe')])[1]").get_attribute("value") # get room-to-delete name
	editMe_room = driver.find_element_by_xpath("(//input[starts-with(@value, 'EditMe')])[1]")
	editMe_room.clear()
	editMe_room_name_edited = "DeleteMe. Edited " + datetime.now().strftime("%d/%m/%Y %H:%M")
	editMe_room.send_keys(editMe_room_name_edited + Keys.ENTER)
	print("Edited default room name successfully")
except:
	print("Failed to edit EditMe room")

# Check if def room name edited
time.sleep(2)
assert editMe_room_name_edited in get_rooms_names(driver)

# Delete room 'DeleteMe. Edited <timestamp>'
# Find room to delete
try:
	deleteMe_room_name = driver.find_element_by_xpath("//input[starts-with(@value, 'DeleteMe')]").get_attribute("value") # get room to delete name
	delete_room_button = driver.find_element_by_xpath("//input[contains(@value, 'DeleteMe')]//ancestor::app-filled-room//p[@class='small']")
	delete_room_button.click()
	print("Confirm room deletion")
except:
	print("Failed to find Delete button")

time.sleep(1)
# Click Cancel on confirmation modal
try:
	cancel_btn = driver.find_element_by_xpath("//div[@class='modal-body']//button[@class='no-styling']")
	cancel_btn.click()
	print("Room deletion canceled")
except:
	print("Failed to find Cancel button on confirmation modal")

try:
	deleteMe_room_name = driver.find_element_by_xpath("//input[starts-with(@value, 'DeleteMe')]").get_attribute("value") # get room to delete name
	delete_room_button = driver.find_element_by_xpath("//input[contains(@value, 'DeleteMe')]//ancestor::app-filled-room//p[@class='small']")
	delete_room_button.click()
	print("Confirm room deletion")
except:
	print("Failed to find Delete button")

time.sleep(2)
# Click YES on confirmation modal
try:
	yes_btn = driver.find_element_by_xpath("//div[@class='modal-body']//button[@class='btn btn-success']")
	yes_btn.click()
	print("Room has been deleted successfully")
except:
	print("Failed to find YES button on confirmation modal")

time.sleep(1)
assert deleteMe_room_name not in get_rooms_names(driver)

# Create room to check link availability
new_room_name='CheckRoomLink'
create_room(driver, new_room_name)

assert new_room_name in get_rooms_names(driver)

try:
	check_link_room_name = driver.find_element_by_xpath("//input[starts-with(@value, 'CheckRoomLink')]").get_attribute("value") # get room to delete name
	room_link = driver.find_element_by_xpath("//input[contains(@value, 'CheckRoomLink')]//ancestor::app-filled-room//a[contains(text(),'https://')]")
	room_link_text = driver.find_element_by_xpath("//input[contains(@value, 'CheckRoomLink')]//ancestor::app-filled-room//a[contains(text(),'https://')]").text
	print("Room link extracted")
except:
	print("Failed to find/extract Delete button")

try:
	room_link.click()
except:
	print("Failed to click the room link")

time.sleep(3)
for handle in driver.window_handles:
	driver.switch_to.window(handle)
	if driver.current_url == room_link_text:
		time.sleep(1)
		try:
			join_meeting_page = driver.find_element_by_xpath("//div[contains(text(), 'How would you prefer to join the call?')]")
			print("I am on Join meeting page")
		except:
			print("Failed to find Join meeting page")
		break

driver.close()

for handle in driver.window_handles:
	driver.switch_to.window(handle)
	if driver.current_url == base_url + "/meeting-rooms":
		break

assert driver.current_url == base_url + "/meeting-rooms"

time.sleep(1)
# Visit User Management page
try:
	user_management_button = driver.find_element_by_css_selector('a[href="/user-management"]')
	user_management_button.click()
	print('User Management page is opened!')
except:
	print('Failed to find "User Management" button!')

assert driver.current_url == (base_url + '/user-management')

time.sleep(1)
# Visit Plan details page
try:
	plan_details_button = driver.find_element_by_css_selector('a[href="/upgrade-plan"]')
	plan_details_button.click()
	print('Plan details page is opened!')
except:
	print('Failed to find "Plan details" button!')

assert driver.current_url == (base_url + '/upgrade-plan')

time.sleep(1)
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

time.sleep(1)
driver.back()

time.sleep(1)
assert driver.current_url == (base_url + '/login-widget')

assert driver.find_element_by_css_selector("#okta-sign-in") != None
