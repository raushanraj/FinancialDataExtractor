#page crawler  N235140030074788

from QueryResult import *
import urllib
import re
from bs4 import BeautifulSoup as bs
import urllib2
from DatabaseHandler import *

class scraper:
	def __init__(self,url):
		self.url=url
		
	@readError
	def getsource(self):
		sock=urllib.urlopen(self.url)
		pagesource=sock.read()
		return pagesource
	
	def get_report_links(self):
		src=self.getsource()
		soup=bs(src)
		links=soup.findAll('a',text=re.compile("report",re.IGNORECASE))
		#print self.check_link_pdf(links[len(links)-2].get('href'))
		return links
		
		
	def check_link_fileformat(self,link,file_format="pdf"):
		flag=False
		try:
			u=urllib2.urlopen(link)
			meta=u.info()
			file_type=meta.getheaders("Content-Type")[0]
			if file_format=="pdf":
				if file_type=="application/pdf":
					flag=True
		except Exception,e:
			print "Error exist" + str(e)
			flag=False
		return flag
		
	def links_to_download(self,report_year="2012",report_type="annual"):
		final_links=[]
		links=self.get_report_links()
		
		for link in links:
			text=link.text
			#print text
			href=link.get('href')
			#print href
			try:
				text=str(text)
				href=str(href)
			except:
				href=href.encode('ascii','ignore')
				text=text.encode('ascii','ignore')
			if self.check_link_fileformat(href) and text.lower().find(report_year)!=-1 and text.lower().find(report_type)!=-1:   #use regex for complex pattern 
				final_links.append((href,text))
		return final_links
				
		
	
	def get_all_pdf(self):
		pass
	



#l=scraper("http://phx.corporate-ir.net/phoenix.zhtml?c=90402&p=irol-reportsannual").links_to_download()

#print l
#print check_link_pdf(l[len(l)-1].get('href'))
	



class crawlerB:
	site="http://phx.corporate-ir.net/phoenix.zhtml"
	irhome="irol-irhome"
	irreport="irol-reportsannual"
	
	#report_year="2013",report_format="pdf",language="en",num_of_pages=1
	
	def __init__(self,*args,**kwargs):
		
		self.report_year=kwargs['report_year']
		self.report_format=kwargs['report_format']
		self.report_language="lang_"+kwargs['report_language']
		self.report_type=kwargs['report_type']
		self.num_of_pages=kwargs['num_pages']
		self.company_name=args[0]
		self.company_ticker=args[1]
		self.company_erev=args[2]
		self.company_url=args[3]
		self.inurl=self.company_name
		self.query=""
		self.code=""
		
	@readError
	def getConfidenceLevel(self):
		url="http://phx.corporate-ir.net/phoenix.zhtml?c="+self.code+"&p=irol-irhome"
		source=scraper(url).getsource()
		source=source.lower()
		count=0
		for i in range(len(source)):
			index=source.find(self.company_ticker.split()[0].lower())
			if index!=-1:
				count=count+1
				i=index+len(self.company_ticker)
		value=0
		if count>8:
			value=count
		if count<8:
			value=0.5
		if count==0:
			value=count
		return value
	@readError
	def getReportPageGoogle(self):
		query_strict="site:"+crawlerB.site+"  "+self.company_erev + " "+crawlerB.irreport
		#above query will filter the result by checking the company_name or company_erev in title
		
		#query_strict="site:"+crawlerB.site+" "+self.company_erev+" "+crawlerB.irreport
		self.query=query_strict
		
		params=urllib.urlencode({'q':query_strict,'lr':self.report_language,'key':search_key,'cx':search_engine_id})
		#other parameters like exactTerms and excludeTerms can also be included
		
		links=queryExtractor(params).GoogleAPIExtractor()
		print "My link is"
		#print links
		if links=="Error":
			print "Cant' Extract error inside getReportPageGoogle"
			return "Error"
		link_details=[]
		if "items" in links.keys():
			links=links['items']
			for link in links:
				link_details.append((link['link'],link['title'],link['snippet']))
			return link_details
		else:
			print "No link inside getReportPageGoogle"
			return "Error"
	
	@readError
	def getReportPageSimple(self):
		
		query_strict="site:"+crawlerB.site+" intitle:"+self.company_erev + " "+crawlerB.irreport
		self.query=query_strict
		
		params=urllib.urlencode({'q':query_strict})
		#other parameters like exactTerms and excludeTerms can also be included
		
		link_details=[]
		links=queryExtractor(params).SimpleExtractor()
		
		#print "my links : =--------  ccc"
		#print links
		
		if links=="Error":
			print "Cant' Extract"
			return "Error"
		
		
		if "results" in links.keys():
			links=links["results"]
			#print links
			for link in links:
				try:
					unescapedUrl=link['unescapedUrl']
					c=''
					x=unescapedUrl.find("c=")
					if x!=-1:
						y=unescapedUrl.find("&p=")
						if y!=-1:
							c=unescapedUrl[x+2:y]
					self.code=c
					#print c
					
					#print link['url']
					#print link['url'],link['titleNoFormatting'],link['content']
					content=re.sub('<[^<]+?>','',link['content'])
					#print "content is :---"+content
					link_details.append((link['url'],link['titleNoFormatting'],content))
				except:
					print "error in link field"
			return link_details
		else:
			print "No link"
			return "Error"
			
			
	#@readError
	def extractReport(self):
		report_info={}
		all_links=[]
		link_report={}
		link_details=self.getReportPageSimple()       # change here for google api 
		
		#print "this is what google extractor give " 
		#print link_details
		#print "-----------------------------------------"
		#print "here is the result"
		#print link_details
		if link_details=="Error" or link_details==[]:
			print "can't get the link"
			return "Error"
		else:
			num=len(link_details)
			if num>self.num_of_pages:
				link_details=link_details[0:self.num_of_pages]
			    #print link_details
				
			for item in link_details:
				try:
					url=item[0]
					title=item[1]
					content=item[2]
					scraperB=scraper(url)
					all_links.append(scraperB.links_to_download(self.report_year,self.report_type))
					#print all_links
					
				except:
					print "can't get link inside extract annual report"
					continue
			i=0
			for item in all_links:
				for links in item:
					link_info={}
					
					url=links[0]
					name=links[1]
					link_info['name']=name
					link_info['company_name']=self.company_name
					link_info['ticker']=self.company_ticker
					link_info['url']=url
					#link_info['c']=
					value=0
					try:
						value=crawlerB.getConfidenceLevel()
					except:
						value=0
					#print value
					link_info['confidence_level']=value
					link_info['type']=self.report_type
					link_info['year']=self.report_year
					link_info['format']=self.report_format
					link_info['download_status']=""
					link_info['download_error']=""
					link_info['download_time']=""
					link_info['priority']=i
					link_info["company_erev"]=self.company_erev
					link_info["company_url"]=self.company_url
					link_info["crawler"]="crawlerB"
					link_info["query"]=self.query
					link_info["code"]=self.code
					print link_info
					database().upsert(link_info,{"url":url})
				i=i+1
				
					
			
		
		

l=crawlerB("avon","avon","avon","abc",report_language="en",report_year="2012",report_format="pdf",report_type="annual",num_pages=1).extractReport()
print l

'''	
self.report_year=kwargs['report_year']
		self.report_format=kwargs['report_format']
		self.report_language="lang_"+kwargs['report_language']
		self.report_type=kwargs['report_type']
		self.num_of_page=kwargs['num_pages']
		self.company_name=args[0]
		self.company_ticker=args[1]
		self.company_erev=args[2]
		self.company_url=arg[3]
		self.inurl=self.company_name
			
print "we call the method"		
a=crawlerB("Avon").extractAnnualReport()
print "end here"

'''
		
		
		
	
	
	
	
