import os
import time
from selenium import webdriver
from datetime import datetime

driver = None


def make_directory_name():
    now = datetime.now()
    year = str(now.year)

    if len(str(now.month)) == 1:
        month = "0" + str(now.month)
    else:
        month = str(now.month)

    if len(str(now.day)) == 1:
        day = "0" + str(now.day)
    else:
        day = str(now.day)

    directory_name = year + month + day

    return directory_name


def driver_setting(jira_site):
    global driver

    driver = webdriver.Chrome("./chromedriver.exe")
    driver.implicitly_wait(3)
    driver.get(jira_site)


def login(id, pw):
    global driver

    driver.find_element_by_id("login-form-username").send_keys(id)
    driver.find_element_by_id("login-form-password").send_keys(pw)
    driver.find_element_by_xpath('//*[@id="login-form-submit"]').click()


def network_delay_protect():
    time.sleep(4)


def set_area_code(area_code):
    global driver

    driver.find_element_by_xpath('//*[@id="ghx-manage-boards-filter"]/div[2]/input').send_keys(area_code)
    network_delay_protect()


def get_page_number():
    global driver

    page_number = driver.find_element_by_xpath('//*[@id="pagination-container"]/ol')
    page_number = int(page_number.text.split()[-2])

    return page_number


def get_person_data():
    global driver

    person_data = list()

    for page_num in range(get_page_number()):
        for person_count in range(1, 26):
            try:
                person_sprint_number_and_name = driver.find_element_by_xpath('//*[@id="boards-table"]/table/tbody/tr[' + str(person_count) + ']')
                data = person_sprint_number_and_name.text.split()
                sprint_number = data[0]

                if data[4] == "어드민":
                    name = data[3]
                else:
                    name = data[4]

                person_sprint_link = driver.find_element_by_xpath('//*[@id="boards-table"]/table/tbody/tr[' + str(person_count) + ']/td[1]/a')
                link = person_sprint_link.get_attribute("href").split("&")[0]

                person_data.append(tuple((sprint_number, name, link)))
            except Exception:
                break

        try:
            driver.find_element_by_xpath('//*[@id="pagination-container"]/ol/li[5]/a').click()
        except Exception:
            break

    return person_data


def sprint_backlog_capture(person_data):
    global driver

    today_directory_name = make_directory_name()
    os.makedirs(today_directory_name)
    os.chdir(today_directory_name)

    for person in person_data:
        sprint_number = person[0]
        person_name = person[1]
        sprint_link = person[2]

        person_file_name = sprint_number + "_" + person_name

        os.makedirs(person_file_name)
        os.chdir(person_file_name)

        driver.get(sprint_link)
        driver.save_screenshot(person_file_name + ".png")

        os.chdir("../")
        time.sleep(2)



def main():
    # Set information
    id = "id"
    pw = "pw"
    area_code = "S02P11C1"
    jira_site = "https://jira.ssafy.com/secure/ManageRapidViews.jspa"

    driver_setting(jira_site)
    login(id, pw)
    set_area_code(area_code)
    sprint_backlog_capture(get_person_data())


if __name__ == '__main__':
    main()
