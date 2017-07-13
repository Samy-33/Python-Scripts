#!/usr/bin/python

"""
: Uses Python 2.7
"""

import requests as rq
from bs4 import BeautifulSoup as bs
import os
import json

s = rq.Session()

def main():
	song = raw_input('Enter the song name...\n> ').lower()
	singer = raw_input('Enter singer name (if don\'t know then just enter Nulll)...\n> ').lower()
	if singer == 'Nulll':
		singer = ' '
	code = '+'.join(song.split(' '))
	#song = '+'.join(code)
	r = s.get('https://www.youtube.com/results?search_query=%s' % song)
	if r.status_code != 200:
		print 'failed...'
		exit(0)
	soup = bs(r.text, 'html.parser')
	links = soup.find_all('h3')
	i = 0
	for link in links:
		if link.a == None:
			continue
		title = link.a.get('title').lower()
		if song in title and singer in title:
			code = link.a
			break
	if(code == '+'.join(song.split(' '))):
		print 'Sorry no song found!!!'
		exit(0)
	print 'Got the link for the song now going to youtubeinmp3...'
	link = 'https://www.youtube.com%s' % code.get('href')
	print link
	#link = 'http://www.youtubeinmp3.com/fetch/?video=%s' % link
	namelink = 'http://www.youtubeinmp3.com/fetch/?format=JSON&video=%s' % link
	#r = rq.get(link)
	#soup = bs(rq.get(namelink).text, 'html.parser')
	#soup = soup.body
	r = s.get(namelink)
	j = json.loads(r.content)
	name = j['title']
	if os.path.exists('/root/Music/%s'%name):
		print 'It is already downloaded you piece of shit'
		exit(0)
	print 'Creating Directory "%s"' % ('/root/Music/%s' % name)
	os.makedirs('/root/Music/%s'%name)
	print('Downloading...')
	try:
		r = s.get(link)
		print 'creating the mp3 file'
		fil = open(name+'.mp3', 'w')
		fil.write(r.content)
		fil.close()
		print 'Saving file to the location...'
		if '"' not in name:
			os.system('mv "%s" "%s"' % (name+'.mp3', 'root/Music/%s' % name))
		if "'" not in name:
			os.system('mv \'%s\' \'%s\'' % (name+'.mp3', 'root/Music/%s' % name))
		print 'Done :)'
	except Exception as e:
		print 'Problem Occured...-->' + str(e) 
		os.system('rm -r %s' %('root/Music/%s' % name))
		exit(0)
	
if __name__ == '__main__':
	main()
	
#
