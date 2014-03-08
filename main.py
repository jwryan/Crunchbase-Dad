from cbaseAPIRequests import getAllInfo
import json
import csv
import pickle

##Put search query in to getAllInfo argument
##Comment out if loading pre-saved results
result = getAllInfo('LED Lighting').results

##Save search results in a python specific format (pickle) for converting to CSV later.
with open('results.pk', 'wb') as outfile:
    pickle.dump(result, outfile)

##Save results in JSON as well (had some issues reading the JSON back in correctly thus
##only supporting loading in pickle files for now
with open('results.json', 'wb') as outfile:
    json.dump(result, outfile)
    
##Open a previously saved pickle file to parse
#with open('results.pk', 'rb') as infile:
#    result = pickle.loads(infile)
#result = pickle.load(open('results.pk','rb'))

#Write
filename = ''
properties = ['name', 'category_code', 'description', 'crunchbase_url', 'homepage_url', 'overview']
with open(r'D:\Test Ing\test.csv', 'wb') as outfile:
    headers = properties
    writer = csv.writer(outfile)
    writer.writerow(headers)
    companies = result['company']
    for company in companies.iterkeys():
        row = []
        for header in headers:
            if companies[company][header]:
                row.append(str(companies[company][header].encode('UTF-8')))
            else:
                row.append(''.encode('UTF-8'))
        writer.writerow(row)
