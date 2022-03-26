import json
import os
import smtplib
import requests
from bs4 import BeautifulSoup
from datetime import datetime
from email.message import EmailMessage

log = ""

def check_availiblity(url, phrase):
    global log
    try:
        page = requests.get(url)
        doc = BeautifulSoup(page.text, "html.parser")
        if phrase in doc:
            return False 
        return True
    except:
        log += "Error parsing the website - "

def main():
    global log
    url = "https://www.ayahealthcare.com/travel-nursing/travel-nursing-jobs/?profession=1&specialty=16&city=Bend,%20OR"
    phrase = "have anything that matches your search at the moment."
    available = check_availiblity(url, phrase)
   
    logfile = open('log.txt', 'r+')
    
    sucessmessage = "Job has been found in bend - "
    if sucessmessage in logfile.read():
        print("Job already found in Bend. Ending script")
        return
    
    if available:
        log += sucessmessage
        try:
            # with open('config.json') as file:
            #     config = json.load(file)
            #     username = config['username']
            #     password = config['password']
            #     fromAddress = config['fromAddress']
            #     toAddress = config['toAddress']
            username = os.environ.get('username')
            password = os.environ.get('password')
            fromAddress = os.environ.get('fromAddress')
            toAddress = os.environ.get('toAddress')
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