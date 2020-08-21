# importing the requests library 
import requests 
import json
from datetime import datetime
# endpoint = "http://ec2-13-58-79-243.us-east-2.compute.amazonaws.com:3001/data"
endpoint = "http://localhost:3000/data"

# current date and time
now = datetime.now()
timestamp = int(datetime.timestamp(now)*1000)

payload = {'timestamp' : timestamp, 't1': 26.2, 't2': 18.4, 't3': 19.4}

# sending post request and saving response as response object 
r = requests.post(url = endpoint, json = payload) 

# extracting response text 
resp = r.text
status = r.status_code 
print(resp, status) 
