# main.py

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


def main_function():
    header()
    date_timestamp, the_date = date_times()
    no_isam_found = []
    isam_has_no_messages = []
    isam_has_messages = []
    environment, hops, domain, check_class, message, worksheet = setup(
        train_operators)

    # Setup Chrome Browser
    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-ssl-errors=yes')
    options.add_argument('--ignore-certificate-errors')

    driver = webdriver.Chrome(options=options)  # Put your webdriver into PATH
    # I like smaller windows, ** Don't make it too small though
    driver.set_window_size(600, 700)

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

            # Page 1
            # Catch exception when there are no Messages from the Device
            try:
                tagged = driver.find_element_by_class_name(
                    'displayTagTable').text

                # Create datestamped folders
                dir = path.join(my_path, the_date)
                if not path.exists(dir):
                    mkdir(dir)

            except NoSuchElementException:
                isam_has_no_messages.append(isam_x)

            # For no Device Number Found
            if len(no_isam_found) > 0:  # Where All Devices are not found' file created
                no_searchs_filename = path.join(
                    dir, (x + ' ' + 'Device Numbers with No Messages ' + ' ' + date_timestamp + '.txt'))
                with open(no_searchs_filename, 'w') as f:
                    f.write(str(no_isam_found))

            # Ensures no_isam_found is not on isam_has_no_messages list
            isam_has_no_messages = list(
                set(isam_has_no_messages) - set(no_isam_found))

            if len(isam_has_messages) > 0:
                isam_has_messages_filename = path.join(
                    dir, (x + ' ' 'ISAM Numbers Tested ' + ' ' + date_timestamp + '.txt'))
                with open(isam_has_messages_filename, 'w') as f:
                    f.write(str(isam_has_messages))
            length_countdown -= 1
            header()
            print(f'TOC - {x}')
            print(f'{length_countdown} ISAM to be checked on {x}')
    header()
    print('Task Complete')
    driver.quit()


if __name__ == '__main__':
    main_function()
