# main.py
'''
    Determine which ISAM from a list have commuicated with their HOPS.
    ISAM List supplied and filter to just TOC and ISAM Number
    variables.py holds a list of the TOCs to be checked in the list.
    For each TOC a list of all ISAM tested is compared with a sub list of those that
    have not communicated in the date/time set in the variables.py.
    Those ISAM that have communicated are documented in a list for investigation
'''

import pandas as pd
from sys import exit

from selenium import webdriver
from selenium.common.exceptions import NoSuchElementException

from threading import Event
from os import remove, system, path, mkdir
from auth import my_user, my_path, hops_pass

from variables import train_operators, date_stamp
from art import header, logo
from setup import setup, date_times
from data_management import remove_no_message_isam


def main_function():
    header()
    no_isam_found = []
    isam_has_no_messages = []
    isam_has_messages = []
    date_timestamp, the_date = date_times()
    environment, hops, domain, check_class, message, worksheet = setup(
        train_operators)

    # Setup Chrome Browser
    options = webdriver.ChromeOptions() # Do you have the correct version webdriver?
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Remember is your webdriver in PATH?
    # I like smaller windows, ** Don't make it too small though
    driver.set_window_size(600, 700)

    # ***** Na atharraich dad nas fhaide an seo ******
    # Filter to the sheet
    df = pd.read_excel(environment, sheet_name=worksheet)
    # Filter the columns
    toc_isam = df[['TOC', 'IIN ISAM ID']]
    toc_isam.columns = toc_isam.columns.str.replace(' ', '')

    # Filter to a TOC
    for x in train_operators:
        toc_x = toc_isam[(toc_isam.TOC == x)]
        isam_list = toc_x['IINISAMID'].tolist()
        length_countdown = len(isam_list)
        no_isam_found = []
        isam_has_messages = []
        header()
        print(f'TOC - {x}')
        print(f'{length_countdown} ISAM to be checked on {x}')
        # Create the server url path here from the dict
        y = hops[x]

        domain_url = 'https://' + y + domain
        driver.get(domain_url)

        # Use Authorisation module
        driver.find_element_by_name("username").send_keys(my_user)
        driver.find_element_by_name("password").send_keys(hops_pass)
        driver.find_element_by_name("submit").click()
        Event().wait(2)
        # Iterate through ISAM list
        for isam_x in isam_list:
            # Enter Device Number and Date
            driver.find_element_by_link_text("Messaging").click()
            driver.find_element_by_link_text("Message Search").click()
            driver.find_element_by_name("fromDate").click()
            driver.find_element_by_name("fromDate").clear()
            driver.find_element_by_name("fromDate").send_keys(date_stamp)
            driver.find_element_by_id("MessageSearch_originator").click()
            driver.find_element_by_id("MessageSearch_originator").clear()
            driver.find_element_by_id(
                "MessageSearch_originator").send_keys(isam_x)
            # Check box for Class of message, value +1 to the Class being checked
            driver.find_element_by_id(check_class).click()
            driver.find_element_by_id("MessageSearch_search").click()
            Event().wait(2)

            # Catch when the Device is not on that Server
            try:
                driver.find_element_by_link_text("Detail")
            except NoSuchElementException:
                print(f'There is no "C{message} Message From" ISAM {isam_x}')
                no_isam_found.append(isam_x)
            Event().wait(2)
            isam_has_messages.append(isam_x)

            # Catch by exception when there are no Messages from the Device
            try:
                tagged = driver.find_element_by_class_name(
                    'displayTagTable').text

                # Create datestamped folders
                dir = path.join(my_path, the_date)
                if not path.exists(dir):
                    mkdir(dir)
            except NoSuchElementException:
                isam_has_no_messages.append(isam_x)

            # Console Display Information
            length_countdown -= 1
            if length_countdown > 0:
                header()
                print(f'TOC - {x}')
                print(f'{length_countdown} ISAM to be checked on {x}')
            else:
                header()
                break

        # Data Management
        if len(isam_has_messages) > 0 and len(no_isam_found) > 0:
            isam_with_comms = []
            isam_with_comms = remove_no_message_isam(
                isam_has_messages, no_isam_found)
            print(type(isam_with_comms))
            if isam_with_comms:
                isam_has_messages_filename = path.join(
                    dir, (x + ' ISAM With Comms ' + date_timestamp + '.txt'))
                with open(isam_has_messages_filename, 'w') as f:
                    f.write(str(isam_with_comms))
                print(f'{x} has no ISAM that communicated')
            else:
                isam_has_messages_filename = path.join(
                    dir, (x + ' Has No ISAM With Comms ' + date_timestamp + '.txt'))
                with open(isam_has_messages_filename, 'w') as f:
                    f.write(str(isam_with_comms))
    # Exit message to user
    header()
    print('Task Complete')
    driver.quit()


if __name__ == '__main__':
    main_function()
