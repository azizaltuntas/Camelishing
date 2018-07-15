import os ,sys,subprocess
from messagebox import Message

class Agent(object):

    def __init__(self,specfile,null):

        spec = specfile

        cmd = 'pyinstaller --onefile %s' %spec

        compiles = os.system(cmd)

        esc = os.getcwd() + '\\dist\\'
        esc2 = os.listdir(esc)

        if os.path.isfile(esc + null + '.exe'):
            Message("Success","Agent Create Successful !","Info")
        else:
            Message("Error", "Agent Create Unsuccessful..", "Info")