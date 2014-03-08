from cbaseAPIRequests import getAllInfo
import json

#query = 'testing' #raw_input('Enter search: ')

result = getAllInfo('LED Lighting').results
with open('results.json', 'w') as outfile:
    json.dump(result, outfile)
