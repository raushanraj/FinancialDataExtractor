# run crawlerC

from crawlerC import *
from InputReader import *
from multiprocessing.dummy import Pool as ThreadPool


input_file="company.xlsx"     
files=[]         
               
#read xlsx 

print "reading ..............input xlsx file"

files=xlsxreader().read("company.xlsx")
print len(files)
if files==[]:
	print "Nothing is returned check the program"


def downloadpic(files):
	 pool=ThreadPool(100)
	 results=pool.map(extractAndSave,files)
	 pool.close()
	 pool.join()
	 

def extractAndSave(details):
	Ticker=details[0]
	Company_name=details[1]
	erev=details[2]
	Base_url=details[3]
	try:
		#print "Looking for Details of : "+erev
		crawlerC(Company_name,Ticker,erev,Base_url).getAllReportLinks(erev)
	except:
		print "Error Occured may be network problem"
			

downloadpic(files)
'''
print "company_not"
print company_not
print len(company_not)
print "\n company not validated",len(company_validation)
print company_validation

print "company keyword error",len(company_keyword)
print company_keyword
print "\n"
print "invalid comp \n",len(invalid_comp)
print invalid_comp

print "number of valid : ",crawlerC.num
'''
