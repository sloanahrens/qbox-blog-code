FILE_URL = "http://apps.sloanahrens.com/qbox-blog-resources/kaggle-titanic-data/test.csv"

ES_HOST = {"host" : "localhost", "port" : 9200}

INDEX_NAME = 'titanic'
TYPE_NAME = 'passenger'

ID_FIELD = 'passengerid'

import csv
import urllib2

response = urllib2.urlopen(FILE_URL)
csv_file_object = csv.reader(response)
 
header = csv_file_object.next()
header = [item.lower() for item in header]

bulk_data=[] 

print(header)