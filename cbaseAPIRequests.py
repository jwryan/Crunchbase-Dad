from time import sleep
import requests
apikey = '9bwsmefb9ya289dguvw7xf2y'

#call Crunchbase API and return request as a dict
def cbaseRequest(baseurl, payload):
        request = requests.get(baseurl, params = payload)
        retries = 0
        waittime = 10
        while request.status_code <> requests.codes.ok and retries < 10:
                print ('Bad response from API service, error code '
                        + str(request.status_code) +
                       '. Will retry in ' + str(waittime) +'s')
                sleep(waittime)
                waittime += 10
                print 'Retrying'
                request = requests.get(baseurl, params = payload)
                retries += 1
        if request.status_code == requests.codes.ok:
                return request.json(strict=False)
        else:
                request.raise_for_status()

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
	
def getAllInfo(query, startpage = 1, maxpages = -1, namespaces = ['company']):
    firstpage = cbaseSearch(query, startpage)
    resultset = ResultSet(namespaces)
    pages = firstpage['total']/10 + 1
    if maxpages == -1 or pages < maxpages:
    	pages = pages + 1
    else:
    	pages = maxpages + 1
    resultset.addAllEntities(firstpage)
    sleep(1)
    callcount = 0
    for currentpage in range(startpage+1, pages):
        if callcount > 9:
            callcount = 0
            sleep(1)
        resultset.addAllEntities(cbaseSearch(query, currentpage))
        callcount += 1
    sleep(1)
    print 'Retrieving entity info'
    callcount = 0
    for namespace in iter(resultset.results):
        for entity in iter(resultset.results[namespace]):
            if callcount > 9:
                callcount = 0
                sleep(1)
            resultset.updateEntity(namespace, entity)
            callcount += 1
    return resultset

class ResultSet:
    def __init__(self, namespaces):
        self.results = {}
        self.namespaces = namespaces
        for name in self.namespaces:
            self.results[name] = {}
            
    def addAllEntities(self, response):
        for result in response['results']:
            self.addEntity(result)
            
    def addEntity(self, result):
        if result['namespace'] in self.namespaces:
            self.results[result['namespace']][result['permalink']] = {}

    def updateEntity(self, namespace, permalink):
        self.results[namespace][permalink] = cbaseEntityInformation(namespace, permalink)
