# this script is meant to harvest part, or all, of the entities in the Europeana Entity API. 
# it linearly iterates over possible entries in the Europeana entity API, so it is predicated on the assumption that entities are added by #id linearly starting from 1 and counting up.
# find documentation for the Entity API here: https://pro.europeana.eu/page/entity
import requests
import json
from time import sleep
from urllib import parse

# choose which entity API URL to call to: you can change 'agent' to 'concept', 'place' or 'timespan'
baseurl = 'https://api.europeana.eu/entity/timespan/base/'
# change key to your API key
append = '.json?wskey=apidemo'
fetchedrecords = 0

# initialise file you will write entities to
with open('timespan.csv', '+a') as file:
    # define range of ints you want to iterate over
    for i in range(30):
        print ('making request #'+str(i))
        r=requests.get(baseurl+str(i)+append)
        print ("request status: ", r.status_code)
        # request validation
        if r.status_code == 404:
            print (r.status_code)
        elif r.raise_for_status() == None:
            data = r.json()
            print ("request successful!\n record #"+str(fetchedrecords))
            # catching errors, warning: this will skip the record if it finds a KeyError or EncodeError
            try:
                preflabel = data["prefLabel"]["en"]
            except (KeyError, UnicodeEncodeError):
                print('encoding error')
                pass
            try:
                file.write (data["id"])
                file.write ("; ")
                file.write (preflabel)
                file.write("\n")
                print(data["id"]+"; "+preflabel+"\n")
            except (KeyError, UnicodeEncodeError):
                print('wrote nothing')
                pass
            fetchedrecords += 1
            # be kind to the servers
            sleep(0.04)
