from datetime import datetime
import pymongo
from pymongo import MongoClient
from crawlerC import *

connection=MongoClient('mongodb://raushan:raushan123@kahana.mongohq.com:10006/financialcrawler')
database=connection.financialcrawler
report=database.report_info_crawlerC_final

class database:
	def __init__(self):
		pass
	
	#@readError
	def upsert(self,*args,**kwargs):
		to_insert_update=args[0]
		condition=args[1]
		query={"$set":to_insert_update}
		report.update(condition,query,upsert=True)
		print "updated"
		
	def update(*args,**kwargs):
		pass
		
		
	def insert(*args,**kwargs):
		pass
	
	def delete(*args,**kwargs):
		pass
		
	def show_company(self,company_name):
		#print
		return[item for item in report.find({"company_name":company_name})]
		
		
	def show_all(self,*args):
		return [item for item in report.find()]
		
	def show_specific(*args,**kwargs):
		pass
	
	def get_pdf_of_company(self,*args):
		pass
	
	def update_download_status(self,*args,**kwargs):
		company_name=args[0]
		status=args[1]
		report.update({'company_name':company_name},{'download_status':status},{'download_time':datetime.now()})

		
		
		
	
	
