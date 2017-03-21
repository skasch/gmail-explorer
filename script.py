# -*- coding: utf-8 -*-
"""
Created on Tue Mar 21 15:58:33 2017

@author: rmondoncancel
"""

from oauth2client import client
import webbrowser
import httplib2
import socks
import json
import requests
import base64

flow = client.flow_from_clientsecrets('client_id.json',
                                      scope='https://www.googleapis.com/auth/gmail.readonly',
                                      redirect_uri='urn:ietf:wg:oauth:2.0:oob')

auth_uri = flow.step1_get_authorize_url()
webbrowser.open_new(auth_uri)

code = ''
socks.wrapmodule(httplib2)
http = httplib2.Http()
credentials = flow.step2_exchange(code, http = http)

http_auth = credentials.authorize(httplib2.Http())
messages = http_auth.request('https://www.googleapis.com/gmail/v1/users/me/messages?q=has:attachment')
messagesJson = json.loads(messages[1].decode('utf-8'))
messageId = messagesJson['messages'][0]['id']
message = http_auth.request('https://www.googleapis.com/gmail/v1/users/me/messages/' + messageId)
messageJson = json.loads(message[1].decode('utf-8'))
attachmentId = messageJson['payload']['parts'][1]['body']['attachmentId']
params = {'access_token': credentials.access_token, 'alt': 'json'}
r = requests.get('https://www.googleapis.com/gmail/v1/users/me/messages/' + messageId + '/attachments/' + attachmentId, params=params)
file_data = base64.urlsafe_b64decode(json.loads(r.content.decode('utf-8'))['data'])
with open('test.pdf', 'wb') as f:
    f.write(file_data)