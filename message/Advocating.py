"""
We test our advocacy in this page : https://www.facebook.com/groups/341334433330410/permalink/1266678044129373/
"""
import random

from selenium.webdriver import ActionChains, Keys
from selenium.webdriver.common.by import By
from message.message_text import MessageText
from datetime import datetime
import time
from driver.driver import Driver
from googlesheet.connection import Connection
from login.login import Login
import re


massage_list = ["Are you using broadband internet ?",
                "Are you using a PC for programming?",
                "What is your PC configuration ?",
                "What is your timezone?"]

# message = random.choice(massage_list)
# print(message)

# print(input("Testing Message :"))


driver = Driver().driver
action = ActionChains(driver)
driver.get("https://facebook.com")


Login().login(driver)

driver.get("https://www.facebook.com/groups/ProgrammingForBeginners/permalink/1220644232066258/")

driver.implicitly_wait(10)
top_comments = driver.find_element(By.XPATH, "//span[contains(.,'Top comments')]")
print(top_comments)
top_comments.click()

driver.implicitly_wait(10)
all_comments = driver.find_element(By.XPATH, "//span[normalize-space()='All comments']")
print(all_comments)
all_comments.click()

driver.implicitly_wait(10)
previous_comments = driver.find_element(By.XPATH, "//span[contains(text(),'previous comments')]")
print(previous_comments)
previous_comments.click()

time.sleep(5)
driver.implicitly_wait(10)
main_comments = driver.find_elements(By.XPATH, "//div[@role='article']")
print(len(main_comments))

main_comments_reply_button = driver.find_elements(By.XPATH, "//div[@role='button'][normalize-space()='Reply']")
print(len(main_comments_reply_button))

comment_index = []
for comment in main_comments:
    comment_index.append(comment)
    print(f"Index : {len(comment_index)}")

    # TODO: We can implement a natural language processor here
    print(comment.text)
    # Base on regular expression create condition
    index = []
    for m in re.finditer(r"\binterested\b", comment.text):
        if m.group(0):
            index.append(m)
            print("Present")

    if len(index) != 0:
        print("Total " + str(len(index)) + " 'interested' Word Found")
        action.move_to_element(comment).click(comment).perform()
        main_comments_reply_button[len(comment_index) - 1].click()
        action.send_keys(random.choice(massage_list)).send_keys(Keys.ENTER).perform()
        print(input("Press any Key: "))
    else:
        print("No 'interested' Word Found")

    print("......................")

print(input("Comment Done :"))
time.sleep(60)

driver.implicitly_wait(10)
