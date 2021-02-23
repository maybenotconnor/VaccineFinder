#!/usr/bin/env python
# coding: utf-8

from bs4 import BeautifulSoup
import requests

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

import time

class vaxfinder :
    """ Object to store results of vaccine search, which includes:
        now: the time.time() when the search was done
        skips: dictionary of current skip locations
        msg: the message to send out based on the search
    """
    
    def __init__(self, now, skips, msg):
        self.now = now
        self.skips = skips
        self.msg = msg
    def __str__(self) :
        return str(self.skips) + '\n' + self.msg
        

def check_availability(myzip, skips) :

    """Checks vaccine availability from vaxfinder.mass.gov. 
       myzip: the zip code to check availability against
       skips: a dictionary of locations to skip, with key being the location
              and the value a time in seconds. Locations are reported when
              the current time is at least 10 minutes later than this value
              
       Returns a vaxfinder object
    """

    # the value of "User-Agent" should be set appropriately
    headers = {"User-Agent": "VinnyVaccineFinder/1.0"}
    
    myurl = 'https://vaxfinder.mass.gov/?zip_or_city='+myzip+'&vaccines_available=on&q='
    page = requests.get(myurl, headers)
    
    now = time.time()
    
    if page.status_code != requests.codes.ok :
        print("Request was not successful, status code:", page.status_code)
        print("Hit enter to continue...")
        input()
        return vaxfinder(now, skips, '')
        
    # Parse page using BeautifulSoup
    soup = BeautifulSoup(page.content, 'html.parser')
    print('\n\nPage title:', soup.title.string.strip())
    
    tt = soup.find('div', class_  = 'locations-table')
    
    if not tt :
        print('no results found')
        return vaxfinder(now, skips, '')
    
    
    print('skips:')
    for sk in skips :        
        diff = round((10*60 - (now - skips[sk])) / 60,2)        
        if diff > 700000 :
            diff = 'IGNORE'
        else :
            diff = str(diff) + ' minutes remaining'
        print(sk + ': ' + diff)
    
    msg = ''
    count = 0
    for row in tt.find_all('tr')[1:] :
        count += 1
        loc = row.find(True, class_ = 'location-summary__title')
        loc = loc.get_text(strip = True)
        dist = row.find(True, class_ = 'location-distance')
        dist = dist.get_text(strip = True)
        
        if loc in skips :
            if now - skips[loc] < 10*60 :                
                break
            
        skips[loc] = time.time()
        
        if count < 3: 
            msg += loc + ', ' + dist + '\n'
    
    if count >= 3 :
        msg += '(and more)'
       
    
    if msg != '' :
        msg += '\n' + myurl
    
    
    return vaxfinder(now, skips, msg)
    

def send_msg(sender, receiver, msg, password) :
    """ Sends an sms message from 'sender' to 'receiver' from the gmail sender account """
    
    if msg == '' :
        return
    
    # Establish a secure session with gmail's outgoing SMTP server using your gmail account
    server = smtplib.SMTP( "smtp.gmail.com", 587 )

    server.starttls()

    server.login( sender, password )

    body = msg
    msg = MIMEMultipart()
    msg['From'] = sender    
    msg['To'] = ', '.join(receiver)
    # Make sure you add a new line in the subject
    msg['Subject'] = "Vaccine alert"
    # Make sure you also add new lines to your body
    # and then attach that body furthermore you can also send html content.
    msg.attach(MIMEText(body, 'plain'))

    sms = msg.as_string()

    server.sendmail(sender,receiver,sms)

