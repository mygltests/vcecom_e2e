import time, sys, random, pickle, string


def log_in(driver, valid_email, valid_password):
    try:
        email_field = driver.find_element_by_css_selector("#input25")
        email_field.clear()
        email_field.send_keys(valid_email)
    except:
        print('Cannot find email text field!')

    # time.sleep(1)

    try:
        password_field = driver.find_element_by_css_selector("#input32")
        password_field.clear()
        password_field.send_keys(valid_password)
    except:
        print('Cannot find password text field!')

    # time.sleep(1)

    try:
        signin_button = driver.find_element_by_css_selector("input[type='submit']")
        signin_button.click()
    except:
        print('Cannot find SIGN IN button!')

    time.sleep(1)

    ##### HOME PAGE #####
    # Welcome message
    try:
        hello_message = driver.find_element_by_css_selector(
            "div.row.summary-info > div.col-12.col-md-5 > h2:nth-child(2)")
        print('User is signed in!')
    except:
        print('Cannot find welcome message!')

    # time.sleep(2)