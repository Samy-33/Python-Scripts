#!/usr/bin/python
"""
: Uses Python 2.7
"""

from bs4 import BeautifulSoup as bs
import requests as rq
import getpass
import random

s = rq.Session()
s.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8', 'Accept-language': 'en-US,en;q=0.5'})

url = 'https://m.facebook.com'
log_url = 'https://m.facebook.com/login.php?'



def login(user, passwd):
	r = s.get(url)
	soup = bs(r.text, 'html.parser')
	form = soup.find(id='login_form')
	inputs = form.find_all('input', {'type': 'hidden'})
	data = {}
	for inp in inputs:
		data[str(inp.get('name'))] = inp.get('value')
	data['email'] = user
	data['pass'] = passwd
	data['login'] = 'Log In'
	r = s.post(log_url, data=data)
	r = s.get(url+'/events/birthdays?')
	if(bs(r.text, 'html.parser').title.string == 'Birthdays'):
		return r
	return False
	

def wishBirthdays(r):
	soup = bs(r.text, 'html.parser')
	print 'Getting List of birthdays\n-----------------'
	div = soup.find('div', {'title': 'Today\'s Birthdays'})
	if div == None:
		print 'There is no birthday today\n----------------'
		return
	names = div.find_all('div', {'class' : ['bw', 'cc']})

	for x in names:
		for string in x.strings:
			print string
	wish = ['Many many happy returns of the day :) A very happy birthday ;)',
			'Happy Birthday :) Enjoy your day...',
			'I wish you a very happy and prosperous birthday... Cheers :)',
			'May this birthday bring you everything that you wish to achieve. A very happy birthday to you',
			'Happy birhtday to you... Happy bithday to you... Enjoy your day... Cheers',
			]
	forms = div.find_all('form', {'method': 'post'})
	inputs = forms[0].find_all('input', {'type': 'hidden'})
	data = {}
	for inp in inputs:
		data[str(inp.get('name'))] = inp.get('value')
	
	
	for form in forms:
		if form.parent.get('style') == None:
			data['user_id'] = form.find('input', {'name': 'user_id'}).get('value')
			data['message'] = wish[random.randrange(0, len(wish))]
			r = s.post(url+'/birthdays/inline/', data=data)
			print '*wished*'
			#else:
			#	print 'Already wished'
		else:
		#	r = s.post(url+'/birthdays/inline/', data=data)
			print '*Already wished*'
	print 'Done!'

def main():
	usr_name = raw_input('Enter your Username\n> ')
	passwd = getpass.getpass()
	r = None
	print "logging in...\n----------------"
	try:
		r = login(usr_name, passwd)
		print "Logged in successfully!\n------------------------"
	except e:
		print 'Error is: '+str(e)
		exit(0)
	try:
		wishBirthdays(r)
	except:
		print "Error... Try again!"
		exit(0)
	s.get(url+'/logout')
	print "Logged out Successfully!\n------------------"



if __name__ == '__main__':
	main()
