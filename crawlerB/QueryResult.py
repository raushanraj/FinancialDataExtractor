import urllib
import json

search_key="AIzaSyCgXqhvOM1rHtC-hNAhOe_SHfLmtUE4Rj4"
search_engine_id="002610714264905976253:hs0wh_m3og8"


def readError(func):
	def wrapper(*args):
		try:
			results=func(*args)
			#print results
			return results
		except Exception,e:
			print str(e)
			return "Error"
	return wrapper


class queryExtractor:
    
    def __init__(self,params):
        self.params=params

    @readError
    def GoogleAPIExtractor(self):
        '''extract result using google paid api with 100 free queries per day,results contains items where
           results[item][link],results[item]item[snippet],results[item]also params will contain the exact
           query like "filetype:pdf search term year etc".item["title"]gives url,small snippet and title.'''
        
        custom_search_link="https://www.googleapis.com/customsearch/v1?&%s"
        query=custom_search_link % self.params
        search_response=urllib.urlopen(query)
        search_results=search_response.read().decode("utf-8")
        results = json.loads(search_results)
        return results
    
    @readError
    def SimpleExtractor(self):
        '''this uses simple ajax search google easily block this extractor'''
        
        simple_search_link="http://ajax.googleapis.com/ajax/services/search/web?v=1.0&%s"
        query=simple_search_link % self.params
        search_response=urllib.urlopen(query)
        search_results=search_response.read().decode("utf-8")
        results = json.loads(search_results)['responseData']
        # check for results key in this.results and then iterate 
        return results





'''
query="site:http://phx.corporate-ir.net/phoenix.zhtml intitle:Avon inurl:irol-reportsannual"
lang="lang_en"
params=urllib.urlencode({'q':query,'lr':lang,'key':search_key,'cx':search_engine_id})
q=queryExtractor(params).SimpleExtractor()
print q
#print q['results'][0]
'''



