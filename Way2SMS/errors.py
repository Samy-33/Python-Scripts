"""
LoginError, MessageLengthExceeded, Way2SMSError

"""

class LoginError(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message
    
class MessageLengthExceeded(Exception):
    
    def __init__(self, max_length, current_length):
        self.max_length = max_length
        self.current_length = current_length
        
    def __str__(self):
        return f'Maximum length allowed is {self.max_length}, yours is {self.current_length}'
    
class Way2SMSError(Exception):
    
    def __init__(self, message):
        self.message = message
        
    def __str__(self):
        return self.message