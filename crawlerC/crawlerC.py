#annualreports.com

import urllib
import urllib2,sys
from bs4 import BeautifulSoup as bs
import re
from tld import get_tld
import requests

from DatabaseHandler import *


company_not=[]
company_validation=[]
company_keyword=[]
invalid_comp=[]


def readError(func):
    def wrapper(*args):
        try:
            results=func(*args)
            return results
        except Exception,e:
          print str(e)
          return "Error"
    return wrapper

class scraper:
    def __init__(self,url):
        self.url=url
		
    @readError
    def getsource(self):
        sock=urllib.urlopen(self.url)
        pagesource=sock.read()
        try:
            pagesource=str(pagesource)
        except:
            pagesource=pagesource.encode('ascii','ignore')
        return pagesource
	
	
			

class crawlerC:
    num=0
    def __init__(self,company_name,ticker,erev,company_url):
        self.base_url="http://www.annualreports.com"
        self.seed="http://annualreports.com/Companies?"
        self.company_name=company_name
        self.company_ticker=ticker
        self.company_url=company_url
        self.company_erev=erev
        
    def validate_link(self,company_site_url,link_text):
        flag=0
        try:
            company_url=self.company_url
            #hdr={'User-Agent':'Mozilla/5.0'}
            #req=urllib2.Request(company_site_url,headers=hdr)
            #a=urllib2.urlopen(req)
            
            if company_url.find("http")==-1:
                    company_url="http://"+company_url
            if company_site_url.find("http")==-1:
                    company_site_url="http://"+company_url
             
            a=requests.get(company_site_url)
            b=requests.get(company_url)
            company_site_url=a.url
            company_url=b.url
            company_url=get_tld(str(company_url),fail_silently=True,as_object=True)
            company_site_url=get_tld(str(company_site_url),fail_silently=True,as_object=True)
            #print "url is : ",company_url,company_site_url
            #print company_url.domain,company_site_url.domain
            if company_url.domain==company_site_url.domain:
                flag=1
            else:
                if company_site_url.domain=="annualreports":
                    m=link_text.lower()
                    
                    m=''.join(e for e in m if e.isalnum())
                    n=self.company_name.lower()
                    n=''.join(e for e in n if e.isalnum())
                    #print m,n
                    if m.find(n)!=-1 or n.find(m.lower())!=-1:
                        flag=1
                 
        except Exception,e:
            print "validation error" +str(e)+self.company_erev
            company_validation.append((self.company_erev,company_site_url,self.company_url))
            flag=0
        
        #print flag
        return flag
			
			

    @readError
    def getSearchResults(self,keyword):
      url=self.seed+urllib.urlencode({"search":keyword})
      #print url
      links_detail=[]
      source=scraper(url).getsource()		
      soup=bs(source)
      table=soup.find("table",attrs={"class":"resultsTable"})
      if not table:
          #print "keyword does'nt exist : "+self.company_erev
          company_keyword.append(self.company_erev)
          return links_detail
      else:
          all_links=table.findAll("a")
          for link in all_links:
              link_id=''
              try:
                  link_href=link.get('href')
                  re_result=re.search(r'\d+',link_href)
                  if re_result:
                      link_id=re_result.group()
                      #print link_id
              except Exception,e:
                  #print str(e)
                  continue
              links_detail.append((link.get('href'),link.text,link_id))
          #print links_detail
          return links_detail
        
    @readError
    def getAllReportLinks(self,keyword):
        all_reports={}
        to_append="http://www.annualreports.com/Company/"
        links=self.getSearchResults(keyword)
        #print links
        if links!="Error" and links!=[]:
            for link in links:
                try:
					pattern=r'(201)\d'
					report_links=[]
					reports={}
					years={}
					link_href=link[0]
					link_text=link[1]
					link_id=link[2]
					link_to_reports=to_append+link_id
					src=scraper(link_to_reports).getsource()
					soup=bs(src,'html.parser')
					div=soup.find("div",attrs={"class":"content ar"})
					div_links=div.ul.findAll("a")
					#print div_links
					for report_link in div_links:
						#print report_link
						#print "hello"
						report_link_href=report_link.get("href")
						report_link_text=report_link.text
						report_link_url=self.base_url+report_link_href
						try:
							report_link_url=requests.get(report_link_url).url
						except:
							report_link_url=self.base_url+report_link_href
							
						#apply check for annual report and year 2012,2013,2014  here 
						is_year=re.search(pattern,report_link_text)
						if is_year:
							year=is_year.group()
							if report_link_text.lower().find("annual")!=-1:
								if year not in years.keys():
									years[year]=[report_link_url]
								else:
									years[year].append(report_link_url)
					  
						#report_links.append({report_link_text:report_link_url})
						reports["keyword_searched"]=keyword
						reports["company_name"]=self.company_name
						reports["company_page_onsite"]=self.base_url+link_href
						reports["company_site_text"]=link_text
						reports["company_site_id"]=link_id
						reports["crawler"]="crawlerC"
						reports["report_links"]=years
						reports["company_ticker"]=self.company_ticker
						reports["company_erev"]=self.company_erev
						reports["company_url"]=self.company_url
						reports["download_status"]=""
						reports["download_time"]=""
						reports["download_error"]=""
					company_site_url=self.base_url+"/CompanyClick/"+link_id
					reports["company_site_url"]=company_site_url
					if self.validate_link(company_site_url,link_text)==1:
						print reports
						database().upsert(reports,{"company_site_id":link_id})
					#crawlerC.num=crawlerC.num+1
					else:
						invalid_comp.append((self.company_erev,self.company_name,self.company_url,company_site_url))
                            #print reports
                            
                    #print reports
                except Exception,e:
                    company_not.append(self.company_erev)
                    print str(e)+" error  :" +self.company_erev
                    #print "error inside : " + self.company_erev
                    continue
              
				    
			    
			    
			    
#crawlerC("amazon","","amazon","www.amazon.com").getAllReportLinks("amzn")

			    
			    
			    
			    
			    
			    
			    
			    
			    
			    
			    

