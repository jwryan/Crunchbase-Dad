from cbaseAPIRequests import getAllInfo
import json
import csv
import pickle

print 'Starting'

##Put search query in to getAllInfo argument
##Comment out if loading pre-saved results
##Set maxpages to -1 to get all pages
result = getAllInfo('LED Lighting', startpage = 1, maxpages = -1).results
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
#result = pickle.load(open(r'results.pk','rb'))
#print 'Pickle file loaded'

#Write to csv
filename = r'results.csv'
properties = ['name', 'category_code', 'description', 'crunchbase_url', 'homepage_url', 'overview']
with open(filename, 'wb') as outfile:
    headers = properties
    writer = csv.writer(outfile)
    writer.writerow(headers)
    companies = result['company']
    for company in companies.iterkeys():
        row = []
        for header in headers:
            if type(companies[company][header]) is int:
                row.append(str(str(companies[company][header]).encode('UTF-8')))
            elif companies[company][header]:
                row.append(str(companies[company][header].encode('UTF-8')))
            else:
                row.append(''.encode('UTF-8'))
        writer.writerow(row)
print 'CSV written'

print 'Done!'
