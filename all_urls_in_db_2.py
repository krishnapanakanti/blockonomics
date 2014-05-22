import requests
import re
import sys
import sqlite3
from urllib2 import urlopen




url=sys.argv
conn = sqlite3.connect('test2.db')




def insert(href_tag):
	cursor = conn.execute("SELECT URL FROM URL WHERE URL = '%s'"%(href_tag))
	if cursor.rowcount == -1:
		try:
			#print href_tag
			conn.execute("INSERT INTO URL(URL) VALUES ('%s');"%(href_tag))
		except sqlite3.IntegrityError:
			pass
		#print "Inserted values successfully !"




def get_url(href_tag):
	
	print "get_url"
	cursor2 = conn.execute("SELECT URL FROM URL WHERE URL = '%s'"%(href_tag))
	if cursor2.rowcount != -1:
		print "Url already exists in data base"
		return
	insert(href_tag)
	try:
		
		response =  requests.get(href_tag)
	except requests.exceptions.MissingSchema, ValueError :
		print "Invalid url"
		return
	if href_tag == '#':
		print "Invalid url"
		return
        page = str(response.content)
	
	l = len(page)
	s = "<a"
	p = "href=\"https://bitcointalk.org/index.php?"
	x = '"'
	c = 0
	b = 0
	while c != -1:
		c = page.find(s,b,l)
		#print "value of c " +`c`
		a = c+2
		if (a>l):
			break
		y = page.find(p,a,l)
		if (y == -1):
			break
		q = y+6
		q1 = y+40
		if (q >l):
			break
		z = page.find(x,q,l)
		b = z
		#print "value of b " +`b`
		p1 = page[q:b]
		p2 = str(p1)
                print p2
		#print list1
		list1.append(p2)
		b = b+2
		if (b >= l):
			break
		'''for row in list1:
			get_url(row)'''



def main():
	global url
	global response
	global page
	global conn
	global list1
	list1 = []

	conn.execute('''CREATE TABLE IF NOT EXISTS URL(URL TEXT PRIMARY KEY NOT NULL);''')
	
	get_url(url[1])
	#print list1
    		
	conn.commit()
	conn.close()





if __name__ == "__main__":
	main()
