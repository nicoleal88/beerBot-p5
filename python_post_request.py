# importing the requests library 
import requests 
import json
from datetime import datetime
# endpoint = "http://ec2-13-58-79-243.us-east-2.compute.amazonaws.com:3001/data"
endpoint = "http://localhost:3000/data"

# current date and time
now = datetime.now()
timestamp = datetime.timestamp(now)

payload = {'t1': 28.2, 't2': 27.4, 't3': 25.4, 'timestamp' : timestamp}

# sending post request and saving response as response object 
r = requests.post(url = endpoint, json = payload) 

# extracting response text 
resp = r.text
status = r.status_code 
print(resp, status) 
