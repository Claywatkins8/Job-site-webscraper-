from asyncio.format_helpers import _format_callback_source
import json
import os
import smtplib
import requests
from urllib.request import Request, urlopen
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.action_chains import ActionChains
from datetime import datetime
from email.message import EmailMessage
import time

log = ""
url = "https://www.ayahealthcare.com/travel-nursing/travel-nursing-jobs/"

def check_availiblity():
    global log
    try:
        DRIVER_PATH = '/usr/local/bin/chromedriver'
        
        options = Options()
        options.headless = True
        options.add_argument("--window-size=1920x1080")
        options.add_argument('--no-sandbox')
        options.add_argument('--disable-gpu')
        driver = webdriver.Chrome(executable_path=DRIVER_PATH, options=options)
        driver.get(url)
 
        # driver = webdriver.Chrome(executable_path=DRIVER_PATH)
        # driver.get(url)

        driver.execute_script("window.scrollTo(0, 900)") 
        time.sleep(2)
        # Set profession to RN
        a = ActionChains(driver)
        profession = driver.find_element_by_class_name("selection")
        profession.click()
        nursing = driver.find_element_by_class_name("item")
        a.move_to_element(nursing).perform()
        regNurse = driver.find_element_by_xpath("//div[@class='item' and text()='Registered Nurse']")
        a.move_to_element(regNurse).perform()
        time.sleep(1)
        regNurse.click()
        time.sleep(1)

        # Set Specialty to ICU
        specialty = driver.find_element_by_class_name("specialties-dropdown")
        specialty.click()
        time.sleep(1)

        icu = driver.find_element_by_xpath("//div[@class='item filter-specialty' and text()='ICU']")
        icu.click()
        time.sleep(1)

        # Input city,state
        location = driver.find_element_by_class_name("locations-dropdown")
        location.click()
        time.sleep(1)
        city = driver.find_element_by_xpath("//div[@class='item filter-location' and text()='Bend, OR']")
        city.click()
        time.sleep(1)

        # hit search button
        button = driver.find_element_by_class_name("search-jobs")
        button.click()
        time.sleep(1)
                
        # Check text
        string = "Doh!"
        pageSource = driver.page_source

        if string in pageSource:
            return False 
        return True

    except:
        log += "Error parsing the website - "

def main():
    global log
    phrase = "Doh!"
    available = check_availiblity()
   
    logfile = open('log.txt', 'r+')
    
    sucessmessage = "Job has been found in bend - "
    if sucessmessage in logfile.read():
        print("Job already found in Bend. Ending script")
        return
    
    if available:
        log += sucessmessage
        try:
            with open('config.json') as file:
                config = json.load(file)
                username = config['username']
                password = config['password']
                fromAddress = config['fromAddress']
                toAddress = config['toAddress']
            # username = os.environ.get('username')
            # password = os.environ.get('password')
            # fromAddress = os.environ.get('fromAddress')
            # toAddress = os.environ.get('toAddress')
        except:
            log += "Error with the credentials file - "
            
        msg = EmailMessage()
        msg['Subject'] = "New job opening in BEND!"
        msg['From'] = fromAddress
        msg['To'] = toAddress      
        msg.set_content("It looks like there is a job opening in Bend availible at: \n" + url  + "\nThis site requires you to search ICU and Bend,OR again after clicking the link.")
        
        try:
            server = smtplib.SMTP('smtp.gmail.com', 587)
            server.ehlo()
            server.starttls()
            server.login(username, password)
            
            server.send_message(msg)
            server.quit()
            log += "Message sent! "
        except:
            log += "Error sending message "
    
    else:
        log += "No job available at this time - "
    
    logfile.write(str(datetime.now()) + " " + log + "\n")
    logfile.close()
        
if __name__ == '__main__':
        main()