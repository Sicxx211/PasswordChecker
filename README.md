# Password checker


# Why I wrote the code

I decided to write this app in order for everyone to be able to check if their password was present in a databreach or not.You may be wondering, but hey haveibeenpwned does the same thing on the web right?Yes it does, but the only problem that it has, everything that you type in there to check is going to be stored in another database, and in case of a breach even if your current password wasn't leaked, it may be after the incident.So I used their API to check if the password was leaked or not, but if you are going to use this app, everything that you may type is going to be stored inside your computer's memory not on their database.So it's an extra layer of security, fast and reliable.


# How I wrote the code 

 
import requests #we use this library to connect to an API <br>
import hashlib #we use this library to do SHA1 hashing <br> 
import sys #We will use this library to be able to give how many passwords we want to check as a input <br>

def request_api_data(query_char): #Basically this will connect to the API server and query_char will be the first 5 hashed characters of the password <br>
 url = 'https://api.pwnedpasswords.com/range/' + query_char #This connects to the api and adds the 5 hashed chars we input <br>
 res = requests.get(url) <br>
 if res.status_code != 200: #This says, if the response to the API is not 200 OK, we will raise this error <br>
  raise RuntimeError(f'Error fetching: {res.status_code}, check the api and try again') <br>
 return res  <br>
<br>
def get_password_leaks_count(hashes, hash_to_check): <br>
 hashes = (line.split(':') for line in hashes.text.splitlines()) <br>
 for h, count in hashes: <br>
  if h == hash_to_check: <br>
   return count <br>
 return 0 <br>
<br>
def pwned_api_check(password):
 sha1password = hashlib.sha1(password.encode('utf-8')).hexdigest().upper() #Basically this will first encode the password that we input into UTF-8, then it's going to be converted to SHA1, we are going to use hexdigest to return it into only HEXADECIMAL values, and finally we are going to make everything upper case <br>
<br>
 first5_char, tail = sha1password[:5], sha1password[5:] #This basically will access only the first 5 characters of the password, and the tail is going to access the rest of it <br>
<br>
 response = request_api_data(first5_char) #We use this to work only with the first 5 characters  return get_password_leaks_count(response, tail) <br>
<br>
def main(args): <br>
 for password in args: <br> 
  count = pwned_api_check(password) <br>
  if count: <br>
   print(f'{password} was found {count} times... you should probably change your password!') <br>
  else: <br>
   print(f'{password} was NOT found. Great job!') <br>
 return 'done!' <br>
if _name_ == '_main_': <br>
 sys.exit(main(sys.argv[1:])) <br>
