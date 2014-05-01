import requests
import re
import sys
url=sys.argv
print url
page=str(url[1])
response =  requests.get(url[1])
page = str(response.content)

fa = re.split(r'\W' , page)
l = len(fa)
for i in fa:
	if len(i) >= 33:
		if len(i) <= 35:
			print i
