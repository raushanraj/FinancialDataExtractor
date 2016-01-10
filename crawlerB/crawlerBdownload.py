#download pdf crawlerB

from DatabaseHandler import *
from pdf_downloader import *

items=database().show_all()
reports_to_download=[]
if items:
	for item in items:
		url=item['url']
		company_name=item['company_name']
		year=item['year']
		reports_to_download.append([company_name,url,year])
		

to_update_status=download_all(reports_to_download)

for company in to_update_status:
	company_name=company[0]
	flag=company[1]
	status="yes"
	if flag==0:
		status="no"
		
	database().update_download_status(company_name,flag)
				
				
			
			
			



