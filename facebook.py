#!/usr/bin/python

from bs4 import BeautifulSoup as bs
import requests as rq
import getpass


class colors:
    HEADER = '\033[95m'
    OKBLUE = '\033[94m'
    OKGREEN = '\033[92m'
    WARNING = '\033[93m'
    FAIL = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'

s = rq.Session()

s.headers.update({"User-Agent": "Mozilla/5.0 (X11; Linux x86_64; rv:43.0) Gecko/20100101 Firefox/43.0 Iceweasel/43.0.4", "Accept-Language": "en-US,en;q=0.5", "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"})

url = "https://m.facebook.com"
log_url = "https://m.facebook.com/login.php?"


#Logging in facebook
def login(usr_name, passwd):
    print('Opening Facebook....')
    try:
        r = s.get(url)
        soup = bs(r.text, 'html.parser')
        form = soup.find(id="login_form")
        inputs = form.find_all('input')
        data = {}
        for inp in inputs:
            if(str(inp.get('type')) == 'hidden'):
                data[str(inp.get('name'))] = inp.get('value')
        data['email'] = usr_name
        data['pass'] = passwd
        data['login'] = 'Log In'
        print 'Logging in.........',
        r = s.post(log_url, data=data)
        print '........'
        r = s.get(url)
        soup = bs(r.text, 'html.parser')
        if(soup.title.string == 'Facebook'):
            return r
        print 'Invalid combination of username and password!'
        exit(0)
    except:
        print "Connection problem!!!"
        r = False
    
#to Post a new update on our own profile    
def newPost(r):
    soup = bs(r.text, 'html.parser')
    form = soup.find_all('form', {'method': 'post'})[0]
    inputs = form.find_all('input', {'type' : 'hidden'})
    data = {}
    for inp in inputs:
        data[str(inp.get('name'))] = inp.get('value')
    msg = raw_input('Type in your post! (When you finish hit return.)\n>')
    data['view_post'] = 'Post'
    data['xc_message'] = msg
    r = s.post(url+'/composer/mbasic/?', data=data)

    
#To show the profile text posted
def showProfileDetail(r):
    soup = bs(r.text, 'html.parser')
    
    print 'It gives only text not anything else so don\'t expect photos to pop up in terminal -_-'
    divs = soup.find('div',id='structured_composer_async_container').find_all('p')
    for p in divs:
        print str(p.string) + '\n*********\n\n'
    
    ch = raw_input('Wanna post something? [Y/N]')
    if ch == 'Y':
        newPost(r)
    else:
        print('as you wish')
 
#to show the unread messages   
def showMessageDetails(r):
    #print 'Only getting unread messages to you\n--------------------\n'
    soup = bs(r.text, 'html.parser')
    messages = soup.find_all('table', {'class': 'bn'})
    #check = soup.find_all('table', {'class': 'f'})
    #print check
    #print '\n\n' + str(messages)
    #if (messages == check):
    #    print 'No new message'
    #    return
    ind = 1
    for msg in messages:
        i = 1
        for st in msg.strings:
            if i == 1:
                print str(ind) + '.\n'
                print '\033[93m' + str(st) + '\033[0m \n'
            else:
                print st
            i+=1
        ind += 1
    ch = raw_input("Want to reply? [Y/N]")
    if(ch == 'Y'):
        m = int(raw_input('Choose the number\n> '))
        messages = list(messages)
        link = str(messages[m-1].find('a').get('href'))
        r = s.get(url+link)
        soup = bs(r.text, 'html.parser')
        print(soup.title)
        divs = soup.find_all('div', {'class': 'bs'})
        #divs = divs.find_all('div')
        print 'New message by ' + str(soup.title.string) + '->\n'
        for fivs in divs:
            for div in fivs:                
                for st in div.strings:
                    print st
                print '--------\n'
        print '***********'
        msg = raw_input('Enter your reply (hit return when you are done)->\n> ')
        data = {}
        inputs = soup.find('form', id="composer_form").find_all('input', {'type': 'hidden'})
        for inp in inputs:
            data[str(inp.get('name'))] = inp.get('value')
        data['body'] = msg
        data['send'] = 'Send'
        r = s.post(url + '/messages/send/?', data=data)
        if(bs(r.text, 'html.parser').title.string in soup.title.string):
            print('message sent Succesfully!')
        else:
            print('couldn\'t send the message some problem occured.')
    else:
        print('Ok as you wish!\n\n')
        
#Function to display the menu
def getMenu(r):
    soup = bs(r.text, 'html.parser')
    #print(soup.title.string)
    div = soup.find('div', {'class': 'bb'})
    if div == None:
        div = soup.find('div', {'class': 'bc'})
    #print(div)
    print'-------------------------------------'
    print 'Choose any number: \n'
    i = 0
    data = []
    for string in div.strings:
        if( not i):
            i += 1
            continue
        print str(i)+ '. ' + string
        data.append(string)
        i = i+1
    print str(i) + '. Refresh'
    print str(i+1) + '. Logout and Exit'
    print'-------------------------------------'
    
    return i
    
    
def showOnline(r):
    soup = bs(r.text, 'html.parser')
    div = soup.find('div', id='root')
    if 'Turn on chat to see who\'s online' in div.strings:
        print 'Chat is Off, want to turn it on?[Y/N]\n> '
        ch = raw_input()
        if ch == 'Y':
            a = soup.find('a', {'class': ['bk', 'bl']})
            
            r = s.get(url+str(a.get('href')))
            """soup = bs(r.text, 'html.parser')
            divs = soup.find_all('a', {'class': 'bv'})
            if divs == None:
                print 'No online friends'
                return
            for div in divs:
                for string in div.strings:
                    print string
                print ''"""
        else:
            print '\nAs you wish\n'
            return
    else:
        divs = soup.find_all('a', {'class': 'bv'})
        if divs == None:
            print 'No online friends'
        else:
            for div in divs:
                for string in div.strings:
                    print string
                print ''
        ch = raw_input('wanna turn off the chat? [Y/N]\n> ')
        if(ch == 'Y'):
            a = soup.find('a', {'class': ['bz', 'ca']})
            r = s.get(url+str(a.get('href')))
            print 'done!!'
            
    
def showNots(r):
    soup = bs(r.text, 'html.parser')
    divs = soup.find_all('div', {'class': 'bu'})
    if divs == None:
        print 'No new notifications'
        return
    for div in divs:
        for string in div.strings:
            print string
        print ''
    
    
#Two small functions just error and good bye
def err():
    print 'Connection Error'

def bye():
    print('Thank You for using Facebook. See you later :)')


#This function selects an option from the menu
def menu(r):
    choice = 0
    i = 1000
    while(choice != i+1):
        i = getMenu(r)
        #i = 8
        #print(data[8])
        #while(data[i] != 'Refresh'):
        #    i += 1;
        choice = int(raw_input('> '))
        if(choice == 1):
            try:
                r = s.get(url)
            except:
                err()
        elif(choice == 2):
            try:
                r = s.get(url+'/me')
                showProfileDetail(r)
            except:
                err()
        elif(choice == 3):
            try:
                r = s.get(url+'/messages')
                showMessageDetails(r)
            except:
                err()
        elif(choice == 4):
            try:
                r = s.get(url+'/notifications')
                showNots(r)
            except:
                err()
        elif(choice == 5):
            try:
                r = s.get(url+'/buddylist')
                showOnline(r)
            except:
                err()
        elif(choice == 6):
            try:
                r = s.get(url +'/friends/center/requests/')
                showFriendReqs(r)
            except:
                err()
        elif(choice == 7 or choice == 8):
            print 'Sorry this service is not yet available'
        elif(choice == i):
            print('Refreshing.....')
        elif(choice == i+1):
            try:
                r = s.get(url+'/logout')
            except:
                err()
            bye()
            exit(0)
        else:
            print('Invalid choice. Choose again. (If it is the new message than go to messages) :)')
        try:
            r = s.get(url+'/home.php?')
        except:
            err()

#main function
def main():
    print "Enter your username"
    usr_name = raw_input("> ")

    #print "Enter your password\n> "
    passwd = getpass.getpass()
    r = login(usr_name, passwd)
    if( not r):
        print "##########\nCan't login... try again later!\n###########"
        exit(0)
    menu(r)
                
if __name__ == '__main__':
    main()
        
        
#
