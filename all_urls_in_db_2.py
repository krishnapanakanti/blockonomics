import requests
import re
import sys
import sqlite3

url=sys.argv
response =  requests.get(url[1])
page = str(response.content)
conn = sqlite3.connect('test2.db')


def insert(href_tag):
	cursor = conn.execute("SELECT URL FROM URL WHERE URL = '%s'"%(href_tag))
	
	if cursor.rowcount == -1:
		try:
			conn.execute("INSERT INTO URL(URL) VALUES ('%s');"%(href_tag))
		except sqlite3.IntegrityError:
			pass
		print "Inserted values successfully !"

def get_url(href_tag):
	print "get_url"
	l = len(href_tag)
	d = str(l)
	s = "<a"
	p = "href=\""
	x = '"'
	c = 0
	b = 0
	while c != -1:
		c = page.find(s,b,l)
		a = c+2
		y = page.find(p,a,l)
		q = y+6
		z = page.find(x,q,l)
		b = z
		p1 = page[q:b]
		p2 = str(p1)
		insert(p2)
		b = b+2
	cursor = conn.execute("SELECT * FROM URL")
        for row in cursor:
                get_url(row[0])

def main():
	global url
	global response
	global page
	global conn
	
	conn.execute('''CREATE TABLE IF NOT EXISTS URL(URL TEXT PRIMARY KEY NOT NULL);''')
	get_url(page)
    		
	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
