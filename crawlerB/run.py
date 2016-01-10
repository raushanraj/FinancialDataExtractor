#crawlerB running
from crawler import *
from DatabaseHandler import *
from QueryResult import *
from InputReader import *


print "All the details are hardcoded here run.py you can change it"

type_of_report="annual" # for crawlerb use keyword annual/financial
year_of_report="2013"
language_of_report="en" # use language code here
format_of_report="pdf" # you can change it to doc
number_of_pages=1 # number of pages you want to grab from the google search results for crawlerb 1 is required 
               # you can check it  by changing the numbers
input_file="company.xlsx"     
files=[]         
               
#read xlsx 

print "reading ..............input xlsx file"

files=xlsxreader().read("company.xlsx")
if files==[]:
	print "Nothing is returned check the program"
else:
	print "start extracting report and saving it in database"
	for details in files:
		Ticker=details[0]
		Company_name=details[1]
		erev=details[2]
		Base_url=details[3]
		try:
			# you can change behaviour of extract report behaviour by using google api crawler or simple crawler in extractReport() function
			crawlerB(Company_name,Ticker,erev,Base_url,report_language=language_of_report,report_year=year_of_report,report_format=format_of_report,report_type=type_of_report,num_pages=number_of_pages).extractReport()
		except:
			print "Error Occured may be google tos voilated"
			continue
	print "All Data Stored"		














#l=crawlerB("bank","avon","av","abc",report_language="en",report_year="2012",report_format="pdf",report_type="annual",num_pages=1).extractReport()



