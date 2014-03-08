from cbaseAPIRequests import getAllInfo
import json
import csv
import pickle

##Put search query in to getAllInfo argument
##Comment out if loading pre-saved results
result = getAllInfo('LED Lighting').results
print 'Results succesfully retrieved'

##Save search results in a python specific format (pickle) for converting to CSV later.
with open(r'results.pk', 'wb') as outfile:
    pickle.dump(result, outfile)
    print 'Pickle file saved'

##Save results in JSON as well (had some issues reading the JSON back in correctly thus
##only supporting loading in pickle files for now
with open(r'results.json', 'wb') as outfile:
    json.dump(result, outfile)
    print 'JSON file saved'
    
##Open a previously saved pickle file to parse
#with open(r'results.pk', 'rb') as infile:
#    result = pickle.loads(infile)
#result = pickle.load(open(r'results.pk','rb'))
#print 'Pickle file loaded'

#Write to csv
filename = r'<PUT FILEPATH HERE (leaving current quotes and not adding new one)>'
properties = ['name', 'category_code', 'description', 'crunchbase_url', 'homepage_url', 'overview']
with open(filename, 'wb') as outfile:
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
Print 'CSV written'
