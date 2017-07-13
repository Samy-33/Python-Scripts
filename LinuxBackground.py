import os

"""
: Uses Python 2.7
"""

fil = open("slideshow.xml", "w")

string = "<background>\n  <starttime>\n <hour>0</hour>\n   <minute>00</minute>\n    <second>01</second>\n  </starttime>\n\n"
os.chdir("/home/sam/Pictures")

files = os.popen("ls").read().split("\n")
files.remove('')

for i in range(0, len(files)):
	string += '<static>\n<duration>600.0</duration>\n<file>/home/sam/Pictures/%s</file>\n</static>\n\n' %files[i]
	string += '<transition type="overlay"><duration>5.0</duration><from>/home/sam/Pictures/%s</from><to>/home/sam/Pictures/%s</to></transition>\n\n' % (files[i], files[(i+1)%len(files)])

string += "</background>\n"
fil.write(string)

fil.close()
os.system("sudo mv slideshow.xml /usr/share/backgrounds/gnome/")
