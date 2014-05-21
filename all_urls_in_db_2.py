import requests
import re
import sys
import sqlite3
from django import forms
from django.forms.util import ValidationError
from Crypto.Hash import SHA256



'''pre'''


url=sys.argv
#response =  requests.get(url[1])
#page1 = response
conn = sqlite3.connect('test.db')
abc1 = 0
abc2 = 0





'''insert function'''



def insert(href_tag):
        #print href_tag
        
	cursor = conn.execute("SELECT URL FROM URL WHERE URL = '%s'"%(href_tag))
	if cursor.rowcount == -1:
		try:
			conn.execute("INSERT INTO URL(URL) VALUES ('%s');"%(href_tag))
			
		except sqlite3.IntegrityError:
			pass
		#print "Inserted values successfully !"



'''get_url function'''



def get_url(href_tag):
                print href_tag
        
                #conn.execute("INSERT INTO URL2(URL) VALUES ('%s');"%(href_tag))
          	#print "get_url"
                response1 =  requests.get(href_tag)
                page2 = str(response1.content)
                l = len(href_tag)
                d = str(l)
                s = "<a"
                p = "href=\""
                x = '"'
                global abc1
                global abc2
                while abc1 != -1:
                        abc1 = page2.find(s,abc2,l)
                        a = abc1+2
                        y = page2.find(p,a,l)
                        q = y+40
                        q1 = y+6
                        z = page2.find(x,q1,l)
                        abc2 = z
                        p1 = page2[q1:abc2]
                        print p1
                        p2 = str(p1)
                        insert(p2)
                        abc2 = abc2+2
                ''' c1 = conn.execute("SELECT * FROM URL")
                for row in c1:

                       c2 = conn.execute("SELECT URL FROM URL WHERE URL = '%s'"%(row))
                       if c2.rowcount == -1:
                              r = str(row[0])
                              print r
                              get_url(r)
                       else:
                              break'''
        



    
def main():
	global url
	global response
	global page
	global conn
        global abc1
        global abc2
        global page1

        abc1 = 0
        abc2 = 0

	conn.execute('''CREATE TABLE IF NOT EXISTS URL(URL TEXT PRIMARY KEY NOT NULL);''')
        conn.execute('''CREATE TABLE IF NOT EXISTS URL2(URL TEXT PRIMARY KEY NOT NULL);''')
        conn.execute('''CREATE TABLE IF NOT EXISTS USER_ADDRESS
       (USER_NAME TEXT NOT NULL,BTC_ADDRESS TEXT PRIMARY KEY NOT NULL);''')
        #print page1
	get_url(url[1])
        ''' c1 = conn.execute("SELECT * FROM URL")
        for row1 in c1:
                r1 = str(row1)
                check_url(r1)'''
    		
	conn.commit()
	conn.close()

if __name__ == "__main__":
	main()
