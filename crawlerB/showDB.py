""" if you want to view stored data you have to run find query of mongodb"""

# this will show all the data of all the reports

from DatabaseHandler import *

#print database().show_all()  

#uncomment above to show all the companies in database


"""enetr company name  LIKE "GOOGLE INC-CL A" to get the result"""

while True:
	company_name=raw_input("Enter company name").strip()
	items =database().show_company(company_name)
	for item in items:
		print item
		print "\n"


