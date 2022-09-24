import os
import time

import gspread
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
import pathlib

# Setting the chrome_options
from selenium.webdriver.common.by import By

chrome_options = Options()
scriptDirectory = pathlib.Path().absolute()
chrome_options.add_argument("--start-maximized")
chrome_options.add_argument("--user-data-dir=chrome-data")
chrome_options.add_argument('--profile-directory=Profile 8')
prefs = {"profile.default_content_setting_values.notifications": 2}
chrome_options.add_experimental_option("prefs", prefs)
chrome_options.add_argument('disable-infobars')
chrome_options.add_experimental_option("useAutomationExtension", False)
chrome_options.add_experimental_option("excludeSwitches", ["enable-automation"])
chrome_options.add_argument("user-data-dir=chrome-data")
chrome_options.add_argument(f"user-data-dir={scriptDirectory}\\userdata")

driver = webdriver.Chrome("chromedriver.exe", chrome_options=chrome_options)
driver.get("https://facebook.com")


def login():
    try:
        # I use environment variable  base on this tutorials https://www.youtube.com/watch?v=IolxqkL7cD8
        username = os.environ.get('facebook_email')
        password = os.environ.get('facebook_pass')
        driver.find_element(By.NAME, "email").send_keys(username)
        driver.find_element(By.NAME, "pass").send_keys(password)
        driver.find_element(By.NAME, "login").click()

        print(input("Login work Successfully Press any Key: "))
    except:
        pass


login()


def open_group_list(index=0):
    # with open('postList.txt') as file:
    with open('TextFile/groupList.txt') as file:
        lines = file.readlines()
        print("We have to work with " + str(len(lines)) + " link")

    for groupLinkList in lines:
        driver.get(groupLinkList)
        print(groupLinkList + "link")
        time.sleep(2)
        driver.implicitly_wait(4)

        # Automatically click join button
        if driver.find_elements(By.XPATH, "//span[contains(text(),'Joined')]"):
            join_button_object = driver.find_element(By.XPATH, "//span[contains(text(),'Joined')]")
            print(join_button_object)
            join_button_object.click()

            # print(input("Stop :"))
            url = driver.current_url
            print(url)

            # TODO: Write in a googleSheet
            """
            Documentation :
            https://docs.gspread.org/en/v5.4.0/oauth2.html#oauth-client-id          
            """
            gc = gspread.service_account('studentfindergspreed-aa5ba05c0365.json')
            spreadsheet = gc.open("StudentFinder")
            worksheet = spreadsheet.worksheet("PythonFacebookGroupList")
            index += 1
            worksheet.update_cell(index, 1, url)

            # Write in a Text File
            with open('TextFile/joinedGroupList.txt', 'a') as the_file:
                the_file.write(f'{url}\n')

        # print(input("Visit Next : "))


open_group_list()
