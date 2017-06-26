import os
print os.getcwd()
print os.path.join(os.getcwd(),'..','static')
print os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
