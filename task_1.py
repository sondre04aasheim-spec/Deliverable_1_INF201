import requests 
import pandas as pd
from dotenv import load_dotenv
import os

#RUN ""python -m pip install requests"" AND ""python -m pip install dotenv"" 

#Get's the data from .env file where you have CLIENT_ID=YOUR_CODE do not use "" nor space
#Also very important to make sure .env is saved on your computer to make sure it works. so if it fails,
# ctrl + s
load_dotenv() 
client_id = os.getenv("CLIENT_ID")

# Define endpoint and parameters
endpoint = 'https://frost.met.no/observations/v0.jsonld'
parameters = {
    'sources': 'SN18700,SN90450',
    'elements': 'mean(air_temperature P1D),sum(precipitation_amount P1D),mean(wind_speed P1D)',
    'referencetime': '2010-04-01/2010-04-03',
}

# Issue an HTTP GET request
r = requests.get(endpoint, parameters, auth=(client_id,''))
# Extract JSON data
json = r.json()


# IMPORTANT!!! the following can be changed or removed as you see fit. as it's not important for the task

# Check if the request worked, print out any errors
if r.status_code == 200:
    data = json['data']
    print('Data retrieved from frost.met.no!')
else:
    print('Error! Returned status code %s' % r.status_code)
    print('Message: %s' % json['error']['message'])
    print('Reason: %s' % json['error']['reason'])  



# This will return a Dataframe with all of the observations in a table format
df = pd.DataFrame()
rows = []


# Organising the data
for i in range(len(data)):
    row = pd.DataFrame(data[i]['observations'])
    row['referenceTime'] = data[i]['referenceTime']
    row['sourceId'] = data[i]['sourceId']
    rows.append(row)


df= pd.concat(rows, ignore_index=True)
df = df.reset_index()
print(df.head())

# These additional columns will be kept
columns = ['sourceId','referenceTime','elementId','value','unit','timeOffset']
df2 = df[columns].copy()
# Convert the time value to something Python understands
df2['referenceTime'] = pd.to_datetime(df2['referenceTime'])

print(df2.head())