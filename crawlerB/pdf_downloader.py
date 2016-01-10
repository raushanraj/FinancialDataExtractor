
from multiprocessing.dummy import Pool as ThreadPool
import urllib2
import os
from mimetypes import guess_extension
#from dbhandler import *
import uuid
def downloader(pdf_set):
	flag=1
	year=pdf_set[2]
	company_name=pdf_set[0]
	url=pdf_set[1]
	try:
		
	#url="http://media.avoncompany.com/file.php/185873/2013-Avon-Annual-Report.pdf"
	#file_name = url.split('/')[-1]
		
		print company_name
		u = urllib2.urlopen(url)
		meta = u.info()
		extension=guess_extension(meta.getheaders("Content-Type")[0])
		if extension:
			file_name=company_name+"_"+str(year)+"_"+str(uuid.uuid4())[0:6]+extension
			file_name=file_name.replace("/","")
		else:
			file_name=url.split('/')[-1].replace("/","")
		print file_name
		
		directory="output/"+year+"/"+company_name+"/"
		if not os.path.exists(directory):
			os.makedirs(directory)
		f = open("output/"+year+"/"+company_name+"/"+file_name, 'wb')
		
		#print (meta)
		file_size = int(meta.getheaders("Content-Length")[0])
		print ("Downloading: %s Bytes: %s" % (file_name, file_size))
	
		file_size_dl = 0
		block_sz = 8192
		while True:
		    buffer = u.read(block_sz)
		    if not buffer:
		        break
		
		    file_size_dl += len(buffer)
		    f.write(buffer)
		    status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
		    status = status + chr(8)*(len(status)+1)
		    print (file_name+": "+status)
		f.close()
	except Exception,e:
		print str(e)
		print("Downloading Error: "+company_name)
		flag=0
	
	return (company_name,flag)

'''
def pdf_downloader(url):
	#file_name=url.split('/')[-1]
	k=urllib.URLopener()
	m=k.retrieve (url, "a.pdf")
	print m
'''

def download_all(pdf_list):
	#meta_data=meta
	#print (meta_data)
	pool=ThreadPool(16)
	results=pool.map(downloader,pdf_list)
	pool.close()
	pool.join()
	return results



