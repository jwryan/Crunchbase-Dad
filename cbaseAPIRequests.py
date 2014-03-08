import requests
apikey = '9bwsmefb9ya289dguvw7xf2y'

#call Crunchbase API and return request as a dict
def cbaseRequest(baseurl, payload):
	return requests.get(baseurl, params = payload).json(strict=False)

def cbaseSearch(query, page = 1):
	payload = {
		'api_key': apikey
		,'query': query
		,'page': str(page)
		}
	baseurl = 'http://api.crunchbase.com/v/1/search.js'
	return cbaseRequest(baseurl, payload)
	
def cbaseEntityInformation(namespace, permalink):
	payload = {
		'api_key': apikey
		}
	baseurl = ('http://api.crunchbase.com/v/1/'
                   + namespace + '/' + permalink + '.js')
	return cbaseRequest(baseurl, payload)
