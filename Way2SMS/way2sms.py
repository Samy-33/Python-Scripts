from constants import (MAIN_URL, MSG_URL)
from errors import (LoginError,
                    MessageLengthExceeded,
                    Way2SMSError)
from getpass import getpass
import requests as r
import re
import sys


class Way2SMS:
    
    def __init__(self, username, password):
        
        self.login_info = {
            'username': username,
            'password': password,
        }
        self.session = r.session()
        self.session.headers.update({
            'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/57.0.2987.110 Safari/537.36',
            'Content-Type': 'application/x-www-form-urlencoded',
            'Accept': '*/*',
            'Connection': 'keep-alive',
        })
        self.url = MAIN_URL
        
    def login(self):
        print(f'[ ] Logging you in as: {self.login_info["username"]}')
        response = self.session.post(MAIN_URL, data=self.login_info)
        
        name = re.search('(?<=flt uname"\>).*?(?=<\/span)', response.text)
        
        if not name:
            raise LoginError("Invalid Credentials.")
            sys.exit()
        print(f'[X] Successfully logged in as {name.group(0)}')
        
        self.url = response.url
        
    def send_msg(self, to: str, message: str):
        
        print('[X] Got your message.')
        
        if len(message) >= 130:
            raise MessageLengthExceeded(130, len(message))
        
        print('[ ] Extracting the token from url')
        token = re.search('(?<=n=).*?(?=&)', self.url).group(0)
        
        if not token:
            raise Way2SMSError('Token not found. Try again.')
            sys.exit()

        print(f'[X] Successfully extracted the token: {token}')

        message_data = {
            'ssaction': 'ss',
            'Token': token,
            'mobile': to,
            'message': message,
            'msgLen': str(140-len(message)),
        }
        
        response = self.session.post(MSG_URL, data=message_data)
        
        success = 'Message has been submitted successfully'
        if success in response.text:
            print('[X] Message sent successfully :)')
        
        else:
            print('[*] Message couldn\'t be sent, try again.')
            sys.exit()
            

def main():
    user = input('Mobile Number: ')
    passwd = getpass()
    way_object = Way2SMS(user, passwd)
    
    way_object.login()
    print('Message Information:')
    to_ = input('\nTo: ')
    message = input('\nBody: <In a single line>\n')
    
    way_object.send_msg(to_, message)
    
    print('\nNow Exitting...')  
    
if __name__ == '__main__':
    main()