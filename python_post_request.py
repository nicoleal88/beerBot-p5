# importing the requests library 
import requests 
import json
import random
import time
from datetime import datetime
endpoint = "http://ec2-13-58-79-243.us-east-2.compute.amazonaws.com:3001/data"
# endpoint = "http://localhost:3000/data"

t1 = 20
t2 = 20
t3 = 20

while True:
    t1 += random.random()*2-1
    t2 += random.random()*2-1
    t3 += random.random()*2-1
    # current date and time
    now = datetime.now()
    timestamp = int(datetime.timestamp(now)*1000)

    payload = {'timestamp' : timestamp, 't1': t1, 't2': t2, 't3': t3}

    # sending post request and saving response as response object 
    r = requests.post(url = endpoint, json = payload) 

    # extracting response text 
    resp = r.text
    status = r.status_code 
    print(payload)
    print(resp, status) 
    time.sleep(5)