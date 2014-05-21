import requests
import re
import sys
import sqlite3

url=sys.argv

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
	response =  requests.get(href_tag)
        page = str(response.content)
	l = len(page)
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
		cursor2 = conn.execute("SELECT URL FROM URL")
		for row in cursor2:
                        r = str(row)
                        print r
                        get_url(row)


def main():
	global url
	global response
	global page
	global conn
	
	conn.execute('''CREATE TABLE IF NOT EXISTS URL(URL TEXT PRIMARY KEY NOT NULL);''')
	get_url(url[1])
    		
	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
