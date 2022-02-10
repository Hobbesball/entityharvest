# this script is meant to harvest part, or all, of the entities in the Europeana Entity API. 
# it linearly iterates over possible entries in the Europeana entity API, so it is predicated on the assumption that entities are added by #id linearly starting from 1 and counting up.
# find documentation for the Entity API here: https://pro.europeana.eu/page/entity
from tkinter.font import names
import requests
import json
from time import sleep
from urllib import parse

#this is the base entity API url
baseurl = 'https://api.europeana.eu/entity/'
namespaces = {'concept','place','timespan','agent'}
#allow user to choose namespace. This will result in different methods being called later down the line
#this is mostly because the data for 'place' entities is structured differently than for timespans, agents or concepts
while True:
    namespace = input('choose a namespace: enter \'concept\', \'place\', \'timespan\' or \'agent\'')
    if namespace in(namespaces):
        break
    else:
        print('this is not a valid namespace, try again')
# change key to your API key
append = '.json?wskey=apidemo'
fetchedrecords = 0

# initialise file you will write entities to
with open('output.csv', '+a') as file:
    # define range of ints you want to iterate over
    for i in range(100):
        print ('making request #'+str(i))
        r=requests.get(baseurl+namespace+"/base/"+str(i)+append)
        print (baseurl+namespace+"/base/"+str(i)+append)
        print ("request status: ", r.status_code)
        # request validation
        if r.status_code == 404:
            print (r.status_code)
        elif r.raise_for_status() == None:
            data = r.json()
            print ("request successful!\n record #"+str(fetchedrecords))
            # catching errors, warning: this will skip the record if it finds a KeyError or EncodeError
            try:
                if namespace == 'concept' or namespace == 'timespan' or namespace == 'agent':
                    preflabel = data["prefLabel"]["en"]
                elif namespace == 'place':
                    preflabel = data["prefLabel"][""]
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
