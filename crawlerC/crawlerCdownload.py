#download pdf crawlerC

from DatabaseHandler import *
from pdf_downloader import *

items=database().show_all()
reports_to_download=[]
if items:
	for item in items:
		report_links=item['report_links']
		company_name=item['company_name']
		if report_links.keys():
			for year in report_links.keys():
				report_link=report_links[year]
				for link in report_link:
					reports_to_download.append([company_name,link,year])
		

to_update_status=download_all(reports_to_download)
				
for company in to_update_status:
	company_name=company[0]
	flag=company[1]
	status="yes"
	if flag==0:
		status="no"
		
	database().update_download_status(company_name,flag)			
			
			
			


