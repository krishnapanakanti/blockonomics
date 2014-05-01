import requests
import re
import sys
url=sys.argv
print url
page=str(url[1])
response =  requests.get(url[1])
page = str(response.content)

fa = re.split(r'\W' , page)
for i in fa:
	fb = re.findall(r"[a-zA-Z1-9]", i)
	if len(fb) >=33:
		if len(fb) <=35:
			print i
