# Vinny's Vaccine Finder

# Scrapes data from vaxfinder.mass.gov and texts you the results

import time
import random
from os import path

import vaccine
import credentials

ZIP = '02122'       # zip code to search
RUNNING_TIME = 10   # running time in minutes
MIN_SLEEP = 25      # minimum sleep time between searches, in seconds
MAX_SLEEP = 65      # maximum sleep time between searches, in seconds


# set up 'skip' locations as specified in 'ignore.txt'
# skip key = location to skip
#      time = locations are reported if found at least 10 minutes
#             after this time

start = time.time()
skips = {}
if path.exists('ignore.txt') :
    with open('ignore.txt') as f :
        lines = f.readlines()
        skips = {l.strip():start*2 for l in lines}


# run for RUNNING_TIME minutes
while time.time() - start < RUNNING_TIME*60 :
    
    # check availability and send message
    vax = vaccine.check_availability(ZIP, skips)
    vaccine.send_msg(credentials.sender, credentials.to, vax.msg, credentials.password)

    # sleep
    r = random.randint(MIN_SLEEP, MAX_SLEEP)
    time.sleep(r)

