'''
Created on 03.10.2015

@author: Kai
'''
def show_info(message):
    ''' print the info message
    @param message: the message
    @type message: str
    '''
    print "[Info:", message, "]"

def show_warn(message):
    ''' print the warn message
    @param message: the message
    @type message: str
    '''
    print "[Warn:", message, "]"

def show_summary(message):
    ''' print the summary message
    @param message: the message
    @type message: str
    '''
    print "[Summary:", message, "]"

def show_error(message):
    ''' print the Error message
    @param message: the message
    @type message: str
    '''
    print "[Error:", message, "]"
    print "[Error: System exits]"
    # exit the program
    exit(0)

if __name__ == "__main__":
    # test
    show_info("test info message,%d" % 5)
    show_info("'s has no id,name:%s,id:%s" % ("123", "456"))
    show_warn("test warn message")
    show_error("test info message")
