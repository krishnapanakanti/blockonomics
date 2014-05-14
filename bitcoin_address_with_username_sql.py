#
# DJango field type for a Bitcoin Address
#
import requests
import re
import sys
from django import forms
from django.forms.util import ValidationError
from Crypto.Hash import SHA256
import sqlite3


class BCAddressField(forms.CharField):
  default_error_messages = {
    'invalid': 'Invalid Bitcoin address.',
    }

  def __init__(self, *args, **kwargs):
    super(BCAddressField, self).__init__(*args, **kwargs)

  def clean(self, value):
    value = value.strip()
    if re.match(r"[a-zA-Z1-9]{27,35}$", value) is None:
      raise ValidationError(self.error_messages['invalid'])
    version = get_bcaddress_version(value)
    if version is None:
      raise ValidationError(self.error_messages['invalid'])
    return value

import math

__b58chars = '123456789ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz'
__b58base = len(__b58chars)

def b58encode(v):
  """ encode v, which is a string of bytes, to base58.                                                                                                               
  """

  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += (256**i) * ord(c)

  result = ''
  while long_value >= __b58base:
    div, mod = divmod(long_value, __b58base)
    result = __b58chars[mod] + result
    long_value = div
  result = __b58chars[long_value] + result

  # Bitcoin does a little leading-zero-compression:                                                                                                                  
  # leading 0-bytes in the input become leading-1s                                                                                                                   
  nPad = 0
  for c in v:
    if c == '\0': nPad += 1
    else: break

  return (__b58chars[0]*nPad) + result

def b58decode(v, length):
  """ decode v into a string of len bytes                                                                                                                            
  """
  long_value = 0L
  for (i, c) in enumerate(v[::-1]):
    long_value += __b58chars.find(c) * (__b58base**i)

  result = ''
  while long_value >= 256:
    div, mod = divmod(long_value, 256)
    result = chr(mod) + result
    long_value = div
  result = chr(long_value) + result

  nPad = 0
  for c in v:
    if c == __b58chars[0]: nPad += 1
    else: break

  result = chr(0)*nPad + result
  if length is not None and len(result) != length:
    return None

  return result

def get_bcaddress_version(strAddress):
  """ Returns None if strAddress is invalid.  Otherwise returns integer version of address. """
  addr = b58decode(strAddress,25)
  if addr is None: return None
  version = addr[0]
  checksum = addr[-4:]
  vh160 = addr[:-4] # Version plus hash160 is what is checksummed                                                                                                    
  h3=SHA256.new(SHA256.new(vh160).digest()).digest()
  if h3[0:4] == checksum:
    
    return ord(version)
  return None

def main():
    url=sys.argv
    print url
    response =  requests.get(url[1])
    page = str(response.content)
    p = re.split(r'\W',page)
    
    l = len(p)
    print l
    l1 = len(page)
    d1 = str(l1)
    s1 = "title=\"View the profile of "
    s2 = "<div class=\"signature "
    x1 = '"'
    x2 = '</div>'
    c1 = 0
    b1 = 0
    print "the length of the string is : " +d1
    conn = sqlite3.connect('test.db')
    
    conn.execute('''CREATE TABLE IF NOT EXISTS USER_ADDRESS
       (USER_NAME TEXT NOT NULL,BTC_ADDRESS TEXT PRIMARY KEY NOT NULL);''')
    while c1 != -1:
        c1 = page.find(s1,b1,l1)
        a1 = c1 + 27
        y1 = page.find(x1,a1,l1)
        b1 = y1
	f1 = page.find(s2,b1,l1)
	g1 = f1 + 24
	f2 = page.find(x2,g1,l1)
	h1 = f2
        p3 = page[a1:b1]
        p1 = page[g1:h1]
        p2 = re.split(r'\W',p1)
        for i in p2:
            s = str(i)
            leg = len(s)
            if leg >= 33:
                if leg <=35:
                    a = get_bcaddress_version(s)
                    if a == 0:
                        p31 = str(p3)
			try:
				conn.execute("INSERT INTO USER_ADDRESS(USER_NAME,BTC_ADDRESS) VALUES ('%s','%s');"%(p31,s))
			except sqlite3.IntegrityError:
				pass
			
    conn.commit()
    conn.close();


if  __name__ =="__main__":
    
    main()
