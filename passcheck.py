#Password checker 

import requests #we use this library to connect to an API
import hashlib #we use this library to do SHA1 hashing
import sys #We will use this library to be able to give how many passwords we want to check as a input

def request_api_data(query_char): #Basically this will connect to the API server and query_char will be the first 5 hashed characters of the password
 url = 'https://api.pwnedpasswords.com/range/' + query_char #This connects to the api and adds the 5 hashed chars we input
 res = requests.get(url)
 if res.status_code != 200: #This says, if the response to the API is not 200 OK, we will raise this error
  raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again')
 return res

def get_password_leaks_count(hashes, hash_to_check):
 hashes = (line.split(':') for line in hashes.text.splitlines())
 for h, count in hashes:
  if h == hash_to_check:
   return count
 return 0

def pwned_api_check(password):
 sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper() #Basically this will first encode the password that we input into UTF-8, then it's going to be converted to SHA1, we are going to use hexdigest to return it into only HEXADECIMAL values, and finally we are going to make everything upper case

 first5_char, tail = sha1password[:5], sha1password[5:] #This basically will access only the first 5 characters of the password, and the tail is going to access the rest of it

 response = request_api_data(first5_char) #We use this to work only with the first 5 characters  return get_password_leaks_count(response, tail)

def main(args):
 for password in args:
  count = pwned_api_check(password)
  if count:
   print(f'{password} was found {count} times... you should probably change your password!')
  else:
   print(f'{password} was NOT found. Great job!')
 return 'done!'
if _name_ == '_main_':
 sys.exit(main(sys.argv[1:]))