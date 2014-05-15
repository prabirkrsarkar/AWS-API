#!/usr/local/bin/python2

# We are uploading a file object to the S3 bucket named redshift_emr_lex with PUT REST API call.
# Hashed Message Auth is as defined by Amazon API documentation.
# Note that message encoding in UTF-8 is a strict requirement.
# Works with Python 2.x. HMAC module in python 3.x expects byte array and this hmac syntax won't work.
# Author: prasarkar@lexmark.com

import requests
import time
import hashlib
from hmac import new as hmac
import os
import keyring
#import httplib
#httplib.HTTPConnection.debuglevel = 1

timetsign=time.strftime("%a, %d %b %Y %H:%M:%S GMT")
key_str = str(keyring.get_password('AWS_keyring','psarkar'))
message = "PUT\n\ntext/plain\n\nx-amz-date:"+timetsign+"\n/redshift_emr_lex/secretcode"

# Calculate Signature.
signature = hmac(key_str, message.encode('UTF-8'), hashlib.sha1).digest().encode('base64')[:-1]

url = "https://s3.amazonaws.com/redshift_emr_lex/secretcode"
headers = {'Host': 's3.amazonaws.com',
'x-amz-date': timetsign ,'Authorization': 'AWS AKIAJC2GCK43PBPTP7QQ:'+signature,
'Content-Type': 'text/plain', 'Content-Length':''+str(os.path.getsize('./secretcode')) }

filepath = './secretcode'
with open(filepath) as fh:
   mydata = fh.read()

   response = requests.put(url, data=mydata, headers=headers)

   #Check for HTTP codes other than 200
   if response.status_code != 200:
      print('Status:', response.status_code, 'Problem with the request. Exiting.')
         print('Body:',response.content)
	 exit()
