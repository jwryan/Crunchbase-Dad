#import modules for dealing with http, csvwriting and rate limiting
import requests #requires requests library from http://docs.python-requests.org/en/latest/
import csv
import json
from time import sleep

#set paramaters to send
apikey = '9bwsmefb9ya289dguvw7xf2y'
query = 'LED lighting'
page = 1
namespace = 'company'
payload = {'api_key': apikey, 'query': query, 'page': str(page)}
search = 'http://api.crunchbase.com/v/1/search.js'

#open output file inside with to close nicely on error
with open('e:/coding/test/test.csv', 'wb') as outfile:

    #make initial request to determine structure and payload
    r = requests.get(search, params = payload)
    output = r.json(strict=False)
    
    #clean up json
    #output = json.dumps(output)
    #output = json.loads(output.replace('\r\n', '\\r\\n'))
    
    writer = csv.writer(outfile)
    
    headers = ['name', 'category_code', 'description', 'crunchbase_url', 'homepage_url', 'overview']
    #headers = []

    #create a header row with all result fields
    #for key in output['results']:
    #    headers.append(key)

    writer.writerow(headers)

    #find size of result set
    pages = output['total']/10 + 1
    
    sleep(1) #to avoid rate limit

    #get all results from result set and add them to csv
    counter = 0
    #for currentpage in range(1,pages+1):
    for currentpage in range(1,pages+1):
        print str(currentpage) +'/' + str(pages)
        payload['page'] = currentpage
        r = requests.get(search, params = payload)
        output = r.json(strict=False)
        results = output['results']
        counter += 1
        if counter == 10:
            counter = 0
            sleep(1)
        for entities in results:
            if entities['namespace'] == namespace:
                row = []
                for header in headers:
                    if entities[header]:
                        row.append(str(entities[header].encode('utf-8')))
                    else:
                        row.append(str(''.encode('utf-8')))
                writer.writerow(row)

print('Done!')
